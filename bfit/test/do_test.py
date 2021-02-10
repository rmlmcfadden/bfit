import sys

# functions
# ~ import bfit.test.functions as fn
# ~ fn.test_lorentzian()
# ~ fn.test_bilorentzian()
# ~ fn.test_gaussian()
# ~ fn.test_quadlorentzian()
# ~ fn.test_pulsed_exp()
# ~ fn.test_pulsed_strexp()

# least squares
# ~ import bfit.test.leastsquares as ls
# ~ ls.test_no_errors()
# ~ ls.test_dy()
# ~ ls.test_dx()
# ~ ls.test_dxdy()
# ~ ls.test_dya()
# ~ ls.test_dxa()
# ~ ls.test_dx_dya()
# ~ ls.test_dxa_dy()
# ~ ls.test_dxa_dya()

# minuit
# ~ import bfit.test.minuit as mnt
# ~ mnt.test_start()
# ~ mnt.test_name()
# ~ mnt.test_error()
# ~ mnt.test_limit()
# ~ mnt.test_fix()

# global fitting
# ~ import bfit.test.global_fitter as gf
# ~ gf.test_constructor()
# ~ gf.test_fitting()

# inspect tab
# ~ import bfit.test.tab_fileviewer as tfview
# ~ tfview.test_fetch(40123, 2020, '20')
# ~ tfview.test_fetch(40033, 2020, '1f')
# ~ tfview.test_fetch(40037, 2020, '1w')
# ~ tfview.test_fetch(40011, 2020, '1n')
# ~ tfview.test_fetch(45539, 2019, '2h')
# ~ tfview.test_fetch(40326, 2019, '2e')
# ~ tfview.test_draw(40123, 2020, '20')
# ~ tfview.test_draw(40033, 2020, '1f')
# ~ tfview.test_draw(40037, 2020, '1w')
# ~ tfview.test_draw(40011, 2020, '1n')
# ~ tfview.test_draw(45539, 2019, '2h')
# ~ tfview.test_draw(40326, 2019, '2e')
# ~ tfview.test_autocomplete()
# ~ tfview.test_draw_mode()
# ~ bfit.do_close_all()

# fetch tab
import bfit.test.tab_fetch_files as tfetch
# ~ tfetch.test_fetch()
# ~ tfetch.test_remove()
tfetch.test_checkbox()
# ~ tfetch.test_draw()

# calculator nmr rf attenuation
# ~ import bfit.test.calculator_nmr_atten as calc_nmr_atten
# ~ calc_nmr_atten.test_calc()

# calculator nmr B1
# ~ import bfit.test.calculator_nmr_B1 as calc_nmr_b1
# ~ calc_nmr_b1.test_calc()

# calculator nqr B0
# ~ import bfit.test.calculator_nqr_B0 as calc_nqr_b0
# ~ calc_nqr_b0.test_calc()

