#!/usr/bin/python3

# Test of the numeric integration used when calculating the pulsed stretched
# exponential function. Specifically, check how well the result converges to the
# analytic solution when the stretching exponent beta = 1.

# Ryan M. L. McFadden
# 2021-02-21


import numpy as np
import pandas as pd
import bdata as bd
from bfit.fitting.functions import pulsed_strexp, pulsed_exp


# constants appropriate for most β-NMR data taken at TRIUMF
nuclear_lifetime = bd.life["Li8"]
pulse_duration = 3.0 * nuclear_lifetime

# create the SLR functions
fcn_exp = pulsed_exp(nuclear_lifetime, pulse_duration)
fcn_strexp = pulsed_strexp(nuclear_lifetime, pulse_duration)

# number of points to try
n_samples = 1000

# generate random values for the SLR fit function parameters that are uniformly
# distributed between typical bounds for real data
relaxation_rates = np.random.uniform(
    1e-2 * nuclear_lifetime, 1e2 * nuclear_lifetime, n_samples
)
amplitudes = np.random.uniform(0.00, 0.15, n_samples)

# stretching exponent
beta = 1.0

# assign an upper limit for an acceptable absolute deviation between results
tolerance = 1e-6

# machine precision for floating point values
epsilon = np.finfo(float).eps

# create an empty DataFrame to hold all of the results
df = pd.DataFrame(
    columns=[
        "Time (s)",
        "Amplitude",
        "Rate (1/s)",
        "Difference",
        "Absolute Difference",
        "Tolerance",
        "Tolerance Exceeded",
        "Epsilon",
        "Epsilon Exceeded",
    ]
)

# loop over the random function parameters
for rate, amplitude in zip(relaxation_rates, amplitudes):

    # generate series of random times to evaluate the SLR fit functions that are
    # uniformly distributed between typical bounds for real data
    time = np.random.uniform(0.0, pulse_duration + 10 * nuclear_lifetime, n_samples)

    # evaluate the difference
    difference = fcn_exp(time, rate, amplitude) - fcn_strexp(
        time, rate, beta, amplitude
    )

    # fill the DataFrame row-by-row
    # https://stackoverflow.com/a/42837693
    for t, d in zip(time, difference):
        df = df.append(
            {
                "Time (s)": t,
                "Amplitude": amplitude,
                "Rate (1/s)": rate,
                "Difference": d,
                "Absolute Difference": np.abs(d),
                "Tolerance": tolerance,
                "Tolerance Exceeded": np.abs(d) > tolerance,
                "Epsilon": epsilon,
                "Epsilon Exceeded": np.abs(d) < epsilon,
            },
            ignore_index=True,
        )


# print a summary of the results
print("")
print("-------")
print("Summary")
print("-------")
print("")
print("Tolerance        = %g" % tolerance)
print("Machine Epsilon  = %g" % epsilon)
print("")
print("Absolute Difference:")
print(" - Max  = %g" % df["Absolute Difference"].max())
print(" - Min  = %g" % df["Absolute Difference"].min())
print(" - Mean = %g" % df["Absolute Difference"].mean())
print("")
print(df["Tolerance Exceeded"].value_counts())
print("")
print(df["Epsilon Exceeded"].value_counts())
print("")
