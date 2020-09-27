#    Creating synethic financial time-series data based on a continuously autoregressive signal
#    a.k.a "Big Data" time series for performance testing analytics functions of scalable database systems.
#    Author : Brandon Harris / brandon.harris@gmail.com
#

#     ----CREDIT AND THANKS---
#     Base python code Eduardo A @ QuasarDB - https://gist.github.com/edouarda/a79ee1fd00bfe38d731870373359a304
#     Synthetic Time Series - J. R. Maat, A. Malali, and P. Protopapas,
#     “TimeSynth: A Multipurpose Library for Synthetic Time Series in Python,” 2017. [Online].
#     Available: http://github.com/TimeSynth/TimeSynth


import timesynth as ts
import pandas as pd
import numpy as np
import multiprocessing as mp
from functools import partial
import time


def ts_data_gen(start_val, sig_val, err_std_dev, n_points):
    time_sampler = ts.TimeSampler(stop_time=n_points)
    reg_time_samples = time_sampler.sample_regular_time(num_points=n_points)

    # Initializing CAR signal
    data_signal = ts.signals.CAR(start_value=start_val, sigma=sig_val) #50/28

    # White noise process
    white_noise = ts.noise.GaussianNoise(std=err_std_dev) #2.6

    # Initializing TimeSeries class with the signal and noise objects
    timeseries = ts.TimeSeries(data_signal, noise_generator=white_noise)

    # Sampling using the irregular time samples
    samples, signals, errors = timeseries.sample(reg_time_samples)
    return samples.round(decimals=2)


def _gen_df(per_chunk, step, out, i):
    print("generating df " + str(i) + " with " + str(per_chunk) + " rows..")


    start_time = np.datetime64('1990-01-01', 'ns') + np.timedelta64(i * per_chunk, step)
    idx = np.array([(start_time + np.timedelta64(i, step))
                    for i in range(per_chunk)]).astype('datetime64[ns]')

    df = pd.DataFrame(index=idx,
                      data={'LMWI': ts_data_gen(50, 28, 2.6, n_points=per_chunk),
                            'CJHA': ts_data_gen(150, 8, 1.85, n_points=per_chunk),
                            'BCTD': ts_data_gen(210, 8, 7.85, n_points=per_chunk),
                            'DNUL': ts_data_gen(1150, 38, 31.35, n_points=per_chunk),
                            'HEQB': ts_data_gen(600, 8, 13.25, n_points=per_chunk),
                            'AOGT': ts_data_gen(450, 8, 12.85, n_points=per_chunk),
                            'ELHW': ts_data_gen(29, 3, 3.85, n_points=per_chunk),
                            'QIMJ': ts_data_gen(311, 12, 2.85, n_points=per_chunk),
                            'ADFI': ts_data_gen(103, 8, 4.85, n_points=per_chunk),
                            'EIWV': ts_data_gen(227, 4, 5.85, n_points=per_chunk),
                            'IGXG': ts_data_gen(62, 3, 1.85, n_points=per_chunk),
                            'HRCS': ts_data_gen(31, 2, 4.85, n_points=per_chunk),
                            'PLFI': ts_data_gen(49, 12, 1.85, n_points=per_chunk),
                            'QYUY': ts_data_gen(880, 38, 11.85, n_points=per_chunk),
                            'SNUM': ts_data_gen(130, 11, 6.65, n_points=per_chunk),
                            'WRBA': ts_data_gen(1250, 44, 44.45, n_points=per_chunk),
                            'UOFC': ts_data_gen(1510, 38, 14.22, n_points=per_chunk),
                            })

    outfile = out + str(i).zfill(4) + ".csv"
    df.to_csv(outfile, header=False)

total = 1600000 #1e10
chunks = 16 #1000
per_chunk = int(total/chunks)
step = 's' # each new row moves ahead 1 step as defined here / m=minute, s=second, ms=mili / reference - https://numpy.org/doc/stable/reference/arrays.datetime.html
output_dir = 'data/'
start_time = np.datetime64('1990-01-01', 'ns')

with mp.Pool(mp.cpu_count()) as pool:
    t0 = time.time()
    results = pool.map_async(partial(_gen_df, per_chunk, step, output_dir), range(chunks), 1)

    pool.close()
    pool.join()
    t1 = time.time()
    total_n = t1 - t0
    print("duration: " + str(total_n))


