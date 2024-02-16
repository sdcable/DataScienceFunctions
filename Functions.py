# -*- coding: utf-8 -*-
"""IS415Project

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QkQzqDWLm8_aCaA0l8_nsrbGO4SS1LQh
"""

#Func 1 - Univeariate Stats Viz
def calculateUnivariateStatsViz(df):
  import seaborn as sns
  from matplotlib import pyplot as plt
  import pandas as pd
  statList = ['Count', 'Unique', 'Data Type', 'Missing', 'Mode', 'Min', '25%', 'Median', '75%', 'Max', 'Std dev','Mean', 'Skew','Kurt']
  newdf=pd.DataFrame(columns=[statList])
  for col in df:
    if pd.api.types.is_numeric_dtype(df[col]): #return either true or false
      text = 'Count: ' + str(df[col].count()) + '\n'
      text += 'Unique: ' + str(round(df[col].nunique(), 2)) + '\n'
      text += 'Data Type: ' + str(df[col].dtype) + '\n'
      text += 'Missing: ' + str(round(df[col].isnull().sum(), 2)) + '\n'
      text += 'Mode: ' + str(df[col].mode().values[0]) + '\n'
      text += 'Min: ' + str(round(df[col].min(), 2)) + '\n'
      text += '25%: ' + str(round(df[col].quantile(.25), 2)) + '\n'
      text += 'Median: ' + str(round(df[col].median(), 2)) + '\n'
      text += '75%: ' + str(round(df[col].quantile(.75), 2)) + '\n'
      text += 'Max: ' + str(round(df[col].max(), 2)) + '\n'
      text += 'Std dev: ' + str(round(df[col].std(), 2)) + '\n'
      text += 'Mean: ' + str(round(df[col].mean(), 2)) + '\n'
      text += 'Skew: ' + str(round(df[col].skew(), 2)) + '\n'
      text += 'Kurt: ' + str(round(df[col].kurt(), 2))

      #Subplots for numeric values
      f, (ax_box, ax) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .65)}) #Ax_box represents box plot and ax represents hist plot
      sns.set(style = 'ticks')
      flierprops = dict(marker = 'o', markersize = 4, markerfacecolor='none', linestyle='none', markeredgecolor = 'gray')
      sns.boxplot(x=df[col], ax=ax_box, fliersize=4, width=.5, linewidth=1, flierprops=flierprops)
      sns.histplot(x= df[col], ax=ax)
      ax_box.set(yticks=[])
      ax_box.set(xticks=[])
      ax_box.set_xlabel('')
      sns.despine(ax=ax)
      sns.despine(ax=ax_box, left=True, bottom=True)
      ax.text(.9, .25, text, fontsize=10, transform=plt.gcf().transFigure)
      ax_box.set_title(col, fontsize=14)
      #add current feature to dataframe
      newdf.loc[col] = [str(df[col].count()), str(round(df[col].nunique(), 2)), str(df[col].dtype), str(round(df[col].isnull().sum(), 2)), str(round(df[col].mode().values[0],2)),
                        str(round(df[col].min(), 2)), str(round(df[col].quantile(.25), 2)), str(round(df[col].median(), 2)), str(round(df[col].quantile(.75), 2)),
                        str(round(df[col].max(), 2)), str(round(df[col].std(), 2)), str(round(df[col].mean(), 2)), str(round(df[col].skew(), 2)), str(round(df[col].kurt(), 2))]
    else:
      text = 'Count: ' + str(df[col].count()) + '\n'
      text += 'Unique: ' + str(round(df[col].nunique(), 2)) + '\n'
      text += 'Data Type: ' + str(df[col].dtype) + '\n'
      text += 'Missing: ' + str(round(df[col].isnull().sum(), 2)) + '\n'

      ax_count = sns.countplot(x=col, data=df, order=df[col].value_counts().index, palette=sns.color_palette("RdBu_r", df[col].nunique()))
      sns.despine(ax=ax_count)
      ax_count.set_title(col)
      ax_count.set_xlabel(col)
      ax_count.set_ylabel('Count')
      ax_count.text(.9, .25, text, fontsize=10, transform=plt.gcf().transFigure)
      #add current feature to dataframe
      newdf.loc[col] = [str(df[col].count()), str(round(df[col].nunique(), 2)), str(df[col].dtype), str(round(df[col].isnull().sum(), 2)), 'NaN', 'NaN', 'NaN', 'NaN', 'NaN',
                        'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
    plt.show()
  return newdf

# Bivariate Stats
def calculateBivariateStatsViz(df, label):
  import seaborn as sns
  from matplotlib import pyplot as plt
  import pandas as pd
  from scipy import stats
  statList = ['Stat Value', '+/-', 'Effect Size', 'P-value']
  newdf=pd.DataFrame(columns=[statList])
  for col in df:
    if pd.api.types.is_numeric_dtype(df[col]):
      createScatterPlot(df, col, label)
      r, p = stats.pearsonr(df[col], df[label])
      if r>0:
        plusminus = 1
      else:
        plusminus = -1
      newdf.loc[col] = ['r', plusminus, round(abs(r),2), round(p,2)]
    else:
      createBarChart(df, col, label)
      unique_groups=df[col].nunique()
      if unique_groups > 2:
        F, p = calculateANOVA(df, col, label)
        newdf.loc[col] = ['F', ' ', round(F,2), round(p,2)]
      else:
        t, p = calculateTTest(df, col, label)
        newdf.loc[col] = ['T', ' ', round(t,2), round(p,2)]

  return newdf

#Calculate t-test
def calculateTTest(df, feature, label):
   import pandas as pd
   from scipy import stats

   groups = df[feature].unique()
   group_labels = []
   for g in groups:
     group_labels.append(df[df[feature] == g][label])
   t, p = stats.ttest_ind(group_labels[0], group_labels[1])
   return t,p

#Calculate Anova
def calculateANOVA(df, feature, label):
   import pandas as pd
   from scipy import stats

   groups = df[feature].unique()
   group_labels = []
   for g in groups:
     group_labels.append(df[df[feature] == g][label])
   return stats.f_oneway(*group_labels)

#Bar Chart
def createBarChart(df, feature, label):
  import pandas as pd
  from matplotlib import pyplot as plt
  import seaborn as sns
  from statsmodels.stats.multicomp import pairwise_tukeyhsd

  unique_groups=df[feature].nunique()
  if unique_groups > 2:
    F, p = calculateANOVA(df, feature, label)
    textstr = 'ANOVA' + '\n'
    textstr += 'F-Stat: ' + str(round(F,2)) + '\n'
    textstr += 'p-value: ' + str(round(p,2)) + '\n\n'

    tukey = pairwise_tukeyhsd(endog=df[label],
                              groups=df[feature],
                              alpha=0.05)
    print(tukey)

  else:
    t, p = calculateTTest(df, feature, label)
    textstr = 'T-Test' + '\n'
    textstr += 'T-Stat: ' + str(round(t,2)) + '\n'
    textstr += 'p-value: ' + str(round(p,2)) + '\n\n'
  ax = sns.barplot(x=df[feature], y=df[label])
  ax.text(1, 0.1, textstr, fontsize=12, transform=plt.gcf().transFigure)
  plt.title(feature + ' and ' + label)
  plt.show()

#Scatterplot
def createScatterPlot(df, feature, label):
  import numpy as np
  import matplotlib.pyplot as plt
  from scipy import stats
  from sklearn.metrics import r2_score
  import seaborn as sns
  import pandas as pd


  model = np.polyfit(df[feature], df[label], 1)
  predict = np.poly1d(model)

  corr = stats.pearsonr(df[feature], df[label])
  r2 = r2_score(df[label], predict(df[feature]))

  textstr = 'y = ' + str(round(model[0], 2)) + 'x +' + str(round(model[1], 2)) + '\n'
  textstr += 'r2 = ' + str(round(r2,2)) + '\n'
  textstr += 'p = ' + str(round(corr[1], 2)) + '\n'
  textstr += 'r = ' + str(round(corr[0], 2)) + '\n'

  sns.set(color_codes = True)
  ax = sns.jointplot(x=df[feature],y=df[label], kind='reg')
  ax.fig.text(1, 0.114, textstr, fontsize=12, transform=plt.gcf().transFigure)
  ax.fig.suptitle(feature + ' and ' + label)
  ax.fig.tight_layout()
  ax.fig.subplots_adjust(top=0.95)

  plt.show()

#MLR - Assumption 1 - Linear Relationship
def assumption1LinearRelationship(df, label):
  import seaborn as sns
  from scipy import stats
  import matplotlib.pyplot as plt
  import pandas as pd
  from sklearn.metrics import r2_score
  import numpy as np

  summary_df = pd.DataFrame(columns = ['R-Value'])

  for col in df:
    if not col == label:
      if df[col].isnull().sum() == 0:
        if pd.api.types.is_numeric_dtype(df[col]):

          r, p,  = stats.pearsonr(df[col], df[label])

          if r < 0.5 :
            createScatterPlot(df, col, label)

            summary_df.loc[col] = [round(r,2)]

  summary_df.sort_values(by=['R-Value'], ascending=False, inplace=True)
  print(summary_df)


  #MLR - Assumption 2 - Multicollinearity
def assumption2Multicollinearity(df, label):
  import numpy as np
  from sklearn.linear_model import LinearRegression
  import pandas as pd

  #select only numeric columns
  numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
  newdf = df.select_dtypes(include=numerics)

  #drop the label
  newdf = newdf.drop([label], axis = 1)
  newdf.head()

  # initialize dictionaries
  vif_dict = {}

  # form input data for each exogenous variable
  for col in newdf:
    y =  newdf[col]
    X = newdf.drop(columns=[col])

    # extract r-squared from the fit
    r_squared = LinearRegression().fit(X, y).score(X, y)

    # calculate VIF
    vif = round(1/(1 - r_squared), 4)
    vif_dict[col] = vif

  df_sort = pd.DataFrame({'VIF': vif_dict})
  df_sort.sort_values(by=['VIF'], ascending=False, inplace=True)
  print(df_sort)

#MLR - Assumption 3 - Independence
def assumption3Independence(df, label):
  import numpy as np
  import pandas as pd
  import statsmodels.api as sm
  from statsmodels.stats.stattools import durbin_watson

  results = mlr(df, label)

  dw = round(float(durbin_watson(results.resid)),3)
  if dw < 1.5:
    output = 'IS NOT'
  elif dw > 2.5:
    output = 'IS NOT'
  else:
    output = 'IS MET'
  print(str(dw) + ". " + "The Independence assumption " + output + ".")

#MLR - Assumption 4 - Homoscedasticity
def assumption4Homoscedasticity(df, label):
  from statsmodels.compat import lzip
  import statsmodels.stats.api as sms
  import numpy as np
  import pandas as pd
  import statsmodels.api as sm

  model = mlr(df, label)

  bp_data = sms.het_breuschpagan(model.resid, model.model.exog)

  names = ['Lagrange multiplier statistic', 'p-value']
  bp_data_dict= dict(lzip(names, bp_data))
  bp_df = pd.DataFrame(bp_data_dict, index = ['Breusch-Pagan Values'])
  if bp_data[1] < .05:
    output = 'IS NOT MET'
  else:
    output = 'IS MET'

  print(str(round(bp_df, 4)) + "\n Homoscedasticity assumption " + output)

#Assumption 5 - Multivariate Normality
def assumption5MultivariateNormality(df, label):
  import matplotlib.pyplot as plt
  from scipy import stats
  import numpy as np
  import pandas as pd
  import statsmodels.api as sm

  df_copy = df.copy()

  for col in df_copy:
    if not pd.api.types.is_numeric_dtype(df_copy[col]):
      df_copy = df_copy.join(pd.get_dummies(df_copy[col], prefix=col, drop_first=True))

  # Set label and features
  y = df_copy[label]
  X = df_copy.select_dtypes(np.number).assign(const=1)
  X = X.drop(columns=[label])

  # Run the multiple linear regression model
  model = sm.OLS(y, X)
  results = model.fit()

  #run assumption
  fig, ax = plt.subplots()

  _,(_,_,r) = stats.probplot(results.resid, plot=ax, fit=True)
  if r < .05:
    output = "IS NOT MET"
  else:
    output = "IS MET"

  print('Jarque-Bera values ' + str(round(r**2,4)) + "\n" + "The MultiVariate assumption " + output)

#Parents Assumptions function
def assumptions(df, label):
  import pandas as pd

  print('Assumption #1: Linear Relationship' + '\n')
  print('Features that dont have a linear relationship with ' + label + ': ')
  assumption1LinearRelationship(df, label)

  print('\n' + 'Assumption #2: No multicollinearity' + '\n')
  assumption2Multicollinearity(df, label)

  print('\n' + 'Assumption #3: Independence' + '\n')
  assumption3Independence(df, label)

  print('\n' + 'Assumption #4: Homoscedasticity' + '\n')
  assumption4Homoscedasticity(df, label)

  print('\n' + 'Assumption #5: Multivariate Normality' + '\n')
  assumption5MultivariateNormality(df, label)

#MLR
def mlr(df, label):
  from sklearn import preprocessing
  import numpy as np
  import statsmodels.api as sm
  import pandas as pd


  for col in df:
    if not pd.api.types.is_numeric_dtype(df[col]): #if the value is not numeric, it must be categorical so we need to create dummy variables
      df = df.join(pd.get_dummies(df[col], prefix=col, drop_first=True)) #get_dummy creates the dummy codes for us. It will technically do dummy codes for all the values, since we need one less than the total values, we will drop the first one

  df_num = df.select_dtypes(np.number)

  df_minmax = pd.DataFrame(preprocessing.MinMaxScaler().fit_transform(df_num), columns=df_num.columns)
  df_minmax.head()

  y = df_minmax[label]
  X = df_minmax.select_dtypes(np.number).assign(const=1)
  X=df_minmax.drop(columns=[label]).assign(const=1)

  model=sm.OLS(y,X)
  results=model.fit()
  return results

#CalculateMetrics
def calculateMetrics(df, label):
  import numpy as np
  import pandas as pd
  import statsmodels.api as sm
  for col in df:
    if not pd.api.types.is_numeric_dtype(df[col]):
      df = df.join(pd.get_dummies(df[col], prefix=col, drop_first=True))

  y = df[label]
  X = df.select_dtypes(np.number).assign(const=1)
  X = X.drop(columns=[label])

  model = sm.OLS(y,X)
  results = model.fit()

  residuals = np.array(df[label]) - np.array(results.fittedvalues)
  rmse = np.sqrt(sum((residuals**2)) / len(df[label]))

  mae = np.mean(abs(residuals))

  metricDict = {"R-squared":str(round(results.rsquared, 4)),
                "RMSE":str(round(rmse, 4)),
                "MAE":str(round(mae, 4)),
                "Label mean":str(round(df[label].mean(), 4))}
  return metricDict

#RandMetrics
def calculateMLRandMetrics(df, label):
  import pandas as pd

  results = mlr(df,label)
  print(results.summary())
  print('\nMLR Metrics\n\n', calculateMetrics(df,label))