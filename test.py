# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np
# sns.set_style("white")
#
# df = pd.read_csv("https://github.com/selva86/datasets/raw/master/mpg_ggplot2.csv")
# text_test = pd.read_csv('./slaves/1234.csv')
# print(text_test[:])
#
# test_array = text_test.values
#
# second_list = []
# kw_list = []
#
# for i in test_array:
#     second_list.append(i[3])
#     kw_list.append(i[4])
#
# # second_list = np.array(second_list)
# # kw_list = np.array(kw_list)
#
# plt.figure(figsize=(16, 10), dpi=70)
# # sns.kdeplot(df.loc[df['cyl'] == 8, "cty"], shade=True, color="orange", alpha=.7)
# # sns.kdeplot(text_test.loc[text_test['kw'] == 3, "second"], shade=True, color="orange", alpha=.7)
# #sns.kdeplot(kw_list, second_list, shade=True, color="orange")
# #sns.kdeplot(text_test.loc[text_test['kw'] == -1, "second"], shade=True, color="orange")
# sns.kdeplot(df.loc[df['cyl'] == 4, "cty"], shade=True, color="g", label="Cyl=4", alpha=.7)
# plt.show()


import matplotlib.pyplot as plt

plt.subplot()
#plt.ion()

x_list = range(0, 100, 1)
y_list = range(0, 100, 1)

    plt.fill_between(x_list, y_list, 0, color='green', alpha=0.7)

plt.show()