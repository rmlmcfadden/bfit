from tkinter import *
from tkinter import ttk, messagebox
from functools import partial
import logging

import numpy as np

from bfit import logger_name
import bfit.backend.colors as colors

class InputLine(object):
    """
        Stores one line of inputs: 
            'p0', 'blo', 'bhi', 'res', 'dres-', 'dres+', 'chi', 'fixed', 'shared'
        as well as the frames and variables        
        
        bfit: bfit object
        data: fitdata object
        entry: dict[col] = entry or checkbutton object
        fitline: fitline object
        frame: ttk.Frame
        label: ttk.label, parameter name
        logger: logger
        pname: string, name of parameter for this line
        variable: dict[col] = variable (StringVar or BooleanVar)            
    """
    
    width = 13
    width_chi = 7
    columns = ['p0', 'blo', 'bhi', 'res', 'dres-', 'dres+', 'chi', 'fixed', 'shared']

    # ======================================================================= #
    def __init__(self, frame, bfit, fitline, show_chi=False):
        """
            frame: frame in which line will grid (first row is 1)
            show_chi: if true, grid the chi parameter
        """
        
        # get logger
        self.logger = logging.getLogger(logger_name)
        self.logger.debug('Initializing')
        
        # assign inputs and defaults
        self.pname = ''
        self.bfit = bfit
        self.fitline = fitline
        self.data = fitline.data
        
        self.frame = frame
        self.label = ttk.Label(self.frame, text=self.pname, justify='right')
        
        self.variable = {   'p0': StringVar(),
                            'blo': StringVar(),
                            'bhi': StringVar(),
                            'res': StringVar(),
                            'dres-': StringVar(),
                            'dres+': StringVar(),
                            'chi': StringVar(),
                            'fixed': BooleanVar(),
                            'shared': BooleanVar(),                            
                        }
        
        self.entry = {}
        for key, var in self.variable.items():
        
            # stringvar
            if key not in ('fixed', 'shared'):
                
                if key == 'chi':
                    width = self.width_chi
                else:
                    width = self.width
                
                self.entry[key] = Entry(self.frame, 
                                          textvariable=self.variable[key], 
                                          width=width)
        
            # booleanvar
            else:
                self.entry[key] = ttk.Checkbutton(self.frame, 
                                                  text='', 
                                                  variable=self.variable[key], 
                                                  onvalue=True, 
                                                  offvalue=False)
        
            # set colors and state
            if key in ('res', 'dres-', 'dres+', 'chi'):
                self.entry[key]['state'] = 'readonly'
                self.entry[key]['foreground'] = colors.foreground
        
        # disallow fixed and shared variables
        self.variable['shared'] = self._set_trace(self.variable['shared'],
                                                  'unfix', self._unfix)
        self.variable['fixed'] = self._set_trace(self.variable['fixed'],
                                                 'unshare', self._unshare)
      
        # set modify all synchronization
        for k in ('p0', 'blo', 'bhi', 'fixed'):

            # set new trace callback
            self.variable[k] = self._set_trace(self.variable[k], 
                                               'modify_all', 
                                               partial(self._modify_all, col=k))
                            
    # ======================================================================= #
    def _modify_all(self, *args, col):
        """
            Do modify all synchronization. Make other lines of the same id equal 
            in value
        """
        
        # check if enabled
        if not self.bfit.fit_files.set_as_group.get():
            return 
        
        # disable trace
        self.variable[col], tr = self._pop_trace(self.variable[col], 'modify_all')
                
        # set 
        self.bfit.fit_files.set_lines(pname=self.pname, 
                                      col=col, 
                                      value=self.variable[col].get(), 
                                      skipline=self)
                                      
        # re-enable trace
        self.variable[col] = self._set_trace(self.variable[col], 'modify_all', tr)
    
    # ======================================================================= #
    def _pop_trace(self, var, name):
        """
            Remove and return trace function
        """
        
        # check if variable has trace dict
        if not hasattr(var, 'trace_id') or name not in var.trace_id.keys():
            return (var, None)
            
        # pop
        tr = var.trace_id[name]
        var.trace_remove("write", tr[0])
        del var.trace_id[name]
        
        # return 
        return (var, tr[1])
        
    # ======================================================================= #
    def _set_trace(self, var, name, function):
        """
            Set the trace functions
        """
        
        # no input
        if function is None:
            return var
        
        # check if variable has trace dict
        if not hasattr(var, 'trace_id'):
            var.trace_id = {}
            
        # check if trace exists
        self._pop_trace(var, name)
        
        # add trace
        var.trace_id[name] = (var.trace_add("write", function), function)
            
        return var
        
    # ======================================================================= #
    def _unfix(self, *args):
        """
            disallow fixed shared parameters
        """
        if self.variable['shared'].get():
            self.variable['fixed'].set(False)
    
    # ======================================================================= #
    def _unshare(self, *args):
        """
            disallow fixed shared parameters
        """
        if self.variable['fixed'].get():
            self.variable['shared'].set(False)

    # ======================================================================= #
    def assign_inputs(self):
        """
            Make sure the inputs are saved to fitdata.fitpar DataFrame
        """        
        
        # check if valid
        if not self.pname:
            return
            
        # assign
        gen = self.data.gen_set_from_var
        for k in ('p0', 'blo', 'bhi', 'fixed'):

            # set new trace callback
            self.variable[k] = self._set_trace(self.variable[k], 
                                               'sync_fitpar', 
                                               gen(self.pname, k, self.variable[k]))
            
    # ======================================================================= #
    def assign_shared(self):
        """
            Link the shared values
        """        
        
        # no key
        if not self.pname:
            return

        # get dict of shared boolean var
        share_var = self.bfit.fit_files.share_var
        
        # check if key is present
        if self.pname not in share_var.keys():
            share_var[self.pname] = self.variable['shared']
            
        # assign key
        else:
            self.variable['shared'] = share_var[self.pname]
        
        # set trace to uncheck fixed box
        self.variable['shared'] = self._set_trace(self.variable['shared'], 
                                                  'unfix', self._unfix)
                
        # link to checkbox
        self.entry['shared'].config(variable=self.variable['shared'])
        
    # ======================================================================= #
    def degrid(self):
        """
            Remove the entries
        """
        self.label.destroy()
        
        for i, key in enumerate(self.columns):
            self.entry[key].destroy()
            
    # ======================================================================= #
    def disable(self):
        """
            Prevent editing
        """        
        for k, e in self.entry.items():
            if k not in ('chi',):
                e.configure(state='disabled')
        
    # ======================================================================= #
    def enable(self):
        """
            Allow editing
        """        
        for k, e in self.entry.items():
            if k in ('res', 'dres+', 'dres-', 'chi'):
                e.configure(state='readonly')
            else:
                e.configure(state='normal')
                
    # ======================================================================= #
    def get(self, col):
        """
            get values
        
            col: str, name of column to get
        """
        
        # wildcards
        if col == '*':
            return {c:self.get(c) for c in self.columns}
        
        # get single value
        if col in self.variable.keys():
            v = self.variable[col].get()
            
        if type(v) is str:
            
            if v == '':
                return np.nan
            
            try:
                v = float(v)
            except ValueError as errmsg:
                self.logger.exception("Bad input.")
                messagebox.showerror("Error", str(errmsg))
                raise errmsg
                
        return v

    # ======================================================================= #
    def grid(self, row):
        """
            Grid the entries
        """
        self.label.grid(column=0, row=row, sticky='e')
        
        for i, key in enumerate(self.columns):
            
            if not row == 2 and key == 'chi':
                pass
            elif key == 'chi':
                self.entry[key].grid(column=i+1, row=row, rowspan=100, padx=5)
            else:
                self.entry[key].grid(column=i+1, row=row, padx=5)     
        
    # ======================================================================= #
    def set(self, pname=None, **values):
        """
            set values
        
            pname: string, parameter name (ex: 1_T1)
            values: keyed by self.columns, the numerical or boolean values for each 
                    column to take
        """
                
        # label
        if pname is not None:
            self.pname = pname
            self.label.config(text=pname)     
            
            # assign inputs
            self.variable['shared'] = BooleanVar()
            self.assign_shared()
            self.assign_inputs()
            
            # check if line is constrained
            if pname in self.data.constrained:
                self.disable()
            else:
                self.enable()
                
        # set values
        for k, v in values.items():
            
            # disable traces
            self.variable[k], tr = self._pop_trace(self.variable[k], 'modify_all')
            
            # don't set
            if str(v) == 'nan':
                pass
                
            # set boolean
            elif type(v) is bool:
                self.variable[k].set(v)
            
            # set string
            elif type(v) is str:
                self.variable[k].set(v)
            
            # set float
            else:
                
                v = float(v)
                
                if k == 'chi':
                    
                    # set number decimal places
                    n_figs = 2
                    
                    # set color
                    if v > self.bfit.fit_files.chi_threshold:
                        self.entry['chi']['readonlybackground']='red'
                    else:
                        self.entry['chi']['readonlybackground']=colors.readonly
            
                else:
                    n_figs = self.bfit.rounding
                    
                # round to n_figs significant figures decimal places
                try:
                    v_decimal = v - int(v)
                    v_decimal = float('{:.{p}g}'.format(v_decimal, p=n_figs))
                    v = int(v) + v_decimal
                except OverflowError:
                    pass
                self.variable[k].set('{:.{p}g}'.format(v, p=8))
                
            # set traces
            self.variable[k] = self._set_trace(self.variable[k], 'modify_all', tr)
            self.variable[k] = self._set_trace(self.variable[k], 'sync_fitpar', 
                                                self.data.gen_set_from_var(self.pname, 
                                                                           k, 
                                                                           self.variable[k]))
