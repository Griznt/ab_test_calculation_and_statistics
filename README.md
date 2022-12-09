# ab test calculations and statistic

author: <a href="mailto:akramovmv@gmail.com">akramovmv@gmail.com</a>

[https://t.me/akramovmv](https://t.me/akramovmv)


#### Required imports:
* import pandas as pd
* import numpy as np
* import matplotlib.pyplot as plt
* from scipy.stats import ttest_ind, mannwhitneyu, probplot
* from tqdm.notebook import tqdm
* import pylab  

#### This library contains next functions:
* compare_distributions - calculates p-values with bootstrap and shows difference between two dataframes
* get_change - calculates change for specified features
* check_t_test_applicability - checks applicability of T-test for data.
* calculate_power - calculates Power for specified data first for T-test, and then for MannWhitneyu test
* calculate_pval - calculates p-value for specified data and test
* get_statistics - big function, that combines all listed methods can be uses for quick analysis and contains:
  - data change calculation
  - power calculation
  - p-value calculation
  - small conclusions in the end.