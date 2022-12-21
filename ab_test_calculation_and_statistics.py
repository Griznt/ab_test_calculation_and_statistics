import pandas as pd
import numpy as np

pd.options.display.float_format = '{:.2f}'.format 
np.set_printoptions(suppress=True)

import matplotlib.pyplot as plt
plt.style.use('default')
plt.style.use('dark_background')

from scipy.stats import ttest_ind, mannwhitneyu, probplot
 
import pylab

# a-test group pandas dataframe
# b-control group pandas dataframe
# feature - metric
# silent - Boolean. If True all prints would be turned off.
# Returns calculated p-values with ttest in bootstrap for specified features.
def compare_distributions(_a,_b,features,silent=False):
    result = []
    n = 1000
    sample_size = 3000
    t = []
    
    for feature in features:
        for _ in range(n):
            a = _a[feature].sample(sample_size, replace=True)
            b = _b[feature].sample(sample_size, replace=True)
            _, pval = ttest_ind(a,b,equal_var=False)
            result.append(pval)

        _t = pd.Series(result)
        if(silent == False):
            print(f'{feature} p-value < 0.05', (_t < 0.05).mean())
        t.append( (_t < 0.05).mean())
    
    if(silent == False):
        print('=========================')
        print('result', sum(t))
        print('users count', len(_a), len(_b))
        print('=========================')
    return t

# a-test group pandas dataframe
# b-control group pandas dataframe
# feature - metric
# Returns change for specified feature
def get_change(a,b,feature):
    t=a[feature].mean()
    c=b[feature].mean()
    print('test:   ', t)
    print('control:', c)
    change = (t-c)/c*100
    print(change,'%')
    return change

# Проверим применимость t-test
# Как проверить, что можно применять t test:  
# - выборочное среднее распределено нормально (bootstrap + qq) 
# - p-value для выборок из одного распределения имеет равномерное распределение (bootstrap + qq)
# - теоретический false positive == практическому false positiv
# Проверим распределение выборочного среднего
# a-test group pandas dataframe
# feature - metric
# Checks ttest applicability for dataframe a
def check_t_test_applicability(a,feature):
    sample_size = 10000
    t = pd.DataFrame([a[feature].sample(sample_size, replace=True).mean() for _ in (range(10000))])

    probplot(t[0], dist='norm', plot=pylab)
    
    display(t.hist(), pylab.show())

# Оценим мощность
# Когда выборки разные, p-value будет маленьким, так как между выборками есть разница и она получена не случайно.  
# Тогда, если мы будем генерировать выборки из наших исходных выборок и считать p-value много раз, мы получим распределение значений p-value.  
# Большинство (80%) значений должно быть меньше уровня значимости альфа 0.5%. Таких значений должно быть около 80% и выше.
# a-test group pandas dataframe
# b-control group pandas dataframe
# feature - metric
# test - test ttest_ind or mannwhitneyu. ttest_ind is default value
# Returns power for specified test
def calculate_power(_a,_b,feature,test=ttest_ind):
    result = []
    n = 10000
    sample_size = 5000
    for _ in range(n):
      pval=1
      a = _a[feature].sample(sample_size, replace=True)
      b = _b[feature].sample(sample_size, replace=True)
      if(test==mannwhitneyu):
        _, pval = mannwhitneyu(a,b,alternative='two-sided')
      else:
        _, pval = ttest_ind(a,b,equal_var=False)
      result.append(pval)
      pass

    t = pd.Series(result)

    text =  f'Мощность {np.where(test==mannwhitneyu,"MannWhitneyu", "T")} test {(t<0.05).mean()*100}%'
    display(t.hist(), text)
    return (t<0.05).mean()

# a-test group pandas dataframe
# b-control group pandas dataframe
# feature - metric
# test - test ttest_ind or mannwhitneyu. ttest_ind is default value
# Returns p-value
def calculate_pval(a,b,feature,test=ttest_ind):
    pval = 1
    if(test==mannwhitneyu):
        _, pval = mannwhitneyu(a[feature], b[feature], alternative='two-sided')
    else:
        _, pval = ttest_ind(a[feature], b[feature], equal_var=False)
    print('p-value', pval, '\r\npval < 0.05', pval < 0.05)
    return pval < 0.05

# a-test group pandas dataframe
# b-control group pandas dataframe
# feature - metric
# threshold - Power from 0 to 1
def get_statistics(a,b,feature,threshold=0.8):
    change = get_change(a,b,feature)
    test = ttest_ind
    power = calculate_power(a,b,feature,test=test)
    pval = 1
    if power < threshold:
        test = mannwhitneyu
        print(f'Power of T test is less than {threshold*100}%')
    power = calculate_power(a,b,feature,test=test)
    if power < threshold:
        print(f'Power of MannWhitney U test is less than {threshold*100}%')
        print(f'Мы не можем задетектить изменение {round(change,2)} для {feature} c мощностью от {threshold*100}%')
        return False
    result = calculate_pval(a,b,feature,test=test)
    if result==False:
        print(f'Изменение {feature} на {round(change,2)}% статистически не значимо.')
        print(f'Это значит, что мы не знаем, полученные результаты являются изменением в продукте или влиянием внешних факторов')
    return pval
