# Drawing style window
# Derek Fujimoto
# July 2018

from tkinter import *
from tkinter import ttk
import webbrowser

# ========================================================================== #
class drawstyle_popup(object):
    """
        Popup window for setting drawing options. 
    """

    # ====================================================================== #
    def __init__(self,parent):
        self.parent = parent
        
         # make a new window
        self.win = Toplevel(parent.mainframe)
        self.win.title('Set Marker and Line Styles')
        frame = ttk.Frame(self.win,relief='sunken',pad=5)
        
        # initialize 
        self.entry_list = []
        self.label_list = []
        self.text_list = []
        self.key_list = list(parent.style.keys())
        self.key_list.sort()
        
        # add entries
        for i,key in enumerate(self.key_list):
            
            # create objects
            self.label_list.append(ttk.Label(frame,text=key,pad=5,justify=LEFT))
            self.text_list.append(StringVar())
            self.entry_list.append(ttk.Entry(frame,
                    textvariable=self.text_list[-1],width=20,justify=RIGHT))
            self.entry_list[-1].insert(0,parent.style[key])
            
            # grid objects
            self.label_list[-1].grid(column=0,row=i,sticky=W)
            self.entry_list[-1].grid(column=1,row=i,columnspan=2)
          
        # add buttons
        set_button = ttk.Button(frame,text='Set',command=self.set)
        close_button = ttk.Button(frame,text='Cancel',command=self.cancel)
        help_button = ttk.Button(frame,text='Help',command=self.help)
        set_button.grid(column=0,row=i+1)
        help_button.grid(column=1,row=i+1)
        close_button.grid(column=2,row=i+1)
            
        # grid frame
        frame.grid(column=0,row=0)

    # ====================================================================== #
    def help(self):
        webbrowser.open('https://matplotlib.org/api/_as_gen/matplotlib.lines.'+\
                        'Line2D.html#matplotlib.lines.Line2D')

    # ====================================================================== #
    def set(self):
        """Set entered values"""
        for k,t in zip(self.key_list,self.text_list):
            
            val = t.get()
            
            if 'width' in k or 'size'in k:
                val = float(val)
            
            self.parent.style[k] = val
        self.win.destroy()
        
    # ====================================================================== #
    def cancel(self):
        self.win.destroy()