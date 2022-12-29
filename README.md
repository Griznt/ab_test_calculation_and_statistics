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
  
#### P.S. самые полезные функции:
1. compare_distributions - позволяет с помощью bootastrap сравнить распределения по заданным метрикам. Для A/A теста значения p-value, которые меньше уровня значимости 5% (0.05) должны быть не более 5% (0.05). Это можно проверить передав одно и тоже распределение на вход функции. Когда мы случайным образом берем подвыборки из одного и того же распределения, чисто могут попадаться p-value, которые меньше уровня значимости 0.05. Это говорит о том, что чисто случайно могут получаться различия даже в одном распределении.
Для разных распределений результат будет стремиться к 100% (1), так как для разных распределений доля p-value, которые меньше 0.05 будет больше (на то они и разные распределения) и другими словами, для разных распределений функция покажет мощность. (отдельно есть метод для вычисления мощности)

2. get_change - функция принимает на вход данные тестовой и контрольной группы и метрику, по которой считаете изменение (можно и массив передать, но будет не такое красивое отображение).
Выводит на экран средние значения и разницу в процентах между  тестовой и контрольной группой

3. get_statistics - основная функция, которая позволяет посчитать разницу, проверить применимость t-test + проверяет мощность стат тестов. Если T-test не применим, тогда будет использоваться MannWhitney U test. 
Затем считается p-value + в конце будет небольшой вывод
