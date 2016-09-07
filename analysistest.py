import pandas
import pylab
from itertools import cycle
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import ttest_ind



df = pandas.read_pickle('full_merged_atlas.p')

focus = df[['PCT_DIABETES_ADULTS10', 'LACCESS_POP10', '2010 Census Population', 'SUPERC12', 'SPECS12', 'FMRKT13']]

focus = focus[np.isfinite(focus['PCT_DIABETES_ADULTS10'])]

access_lower_q = focus.quantile(q=0.25, axis=0)['LACCESS_POP10']
superc_lower_q =  focus.quantile(q=0.25, axis=0)['SUPERC12']
spec_lower_q =  focus.quantile(q=0.25, axis=0)['SPECS12']
market_lower_q =  focus.quantile(q=0.25, axis=0)['FMRKT13']

access_upper_q = focus.quantile(q=0.75, axis=0)['LACCESS_POP10']
superc_upper_q =  focus.quantile(q=0.75, axis=0)['SUPERC12']
spec_upper_q =  focus.quantile(q=0.75, axis=0)['SPECS12']
market_upper_q =  focus.quantile(q=0.75, axis=0)['FMRKT13']

focus = focus[focus['LACCESS_POP10'] >= access_lower_q]

plt.figure(1)

plt.subplot(211)
#test = focus[focus['FMRKT13'] >= market_upper_q]
test = focus[focus['SPECS12'] >= spec_upper_q]
#test = test[test['SUPERC12'] <= superc_lower_q]

test['PCT_DIABETES_ADULTS10'].hist()

plt.subplot(212)
#test2 = focus[focus['FMRKT13'] <= market_lower_q]
#test2 = focus[focus['SPECS12'] <= spec_lower_q]
#test2 = test2[test2['SUPERC12'] >= superc_upper_q]
test2 = focus[focus['SUPERC12'] >= superc_upper_q]
test2['PCT_DIABETES_ADULTS10'].hist()

plt.show()

print ttest_ind(test['PCT_DIABETES_ADULTS10'], test2['PCT_DIABETES_ADULTS10'])