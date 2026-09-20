import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
data = pd.read_csv('multiply_times.csv')
plot = sns.relplot(data=data, kind='line', x='n', y='time', hue='algorithm', marker='o')
plot.set(xscale='log', yscale='log')
plot.savefig('multiply_times.png')

import numpy as np
for name, group in data.groupby('algorithm'):
    group = group[group.time > 0]
    slope = np.polyfit(np.log(group.n), np.log(group.time), 1)[0]
    print(f'{name}: measured exponent ~= {slope:.2f}')