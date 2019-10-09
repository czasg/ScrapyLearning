# from pandas import *
# from pylab import *
# import numpy as np
# from matplotlib import pyplot as plt
# mpl.rcParams['font.sans-serif'] = ['SimHei']  # 加载中文字体的神奇呀
# idx = Index(np.arange(1,7))
# df = DataFrame(np.random.randn(6, 2), index=idx, columns=['', 'count'])
# valss = np.array([['总数', 100], ['嘿嘿', 10], ['流皮', '5']])
# vals = np.around(df.values,2)
# fig = plt.figure(figsize=(9,4))
# ax = fig.add_subplot(111, frameon=False, xticks=[], yticks=[])  # 去掉背景的意思嘛
# the_table=plt.table(cellText=valss, rowLabels=None, colLabels=['', 'count'],colWidths = [0.1]*vals.shape[1], loc='center',cellLoc='center')
# the_table.set_fontsize(20)
# the_table.scale(2.5,2.58)
# plt.show()  # todo 画表格的


import numpy as np
import matplotlib.pyplot as plt
men_means, men_std = (20, 35, 30, 35, 27), (0, 3, 4, 1, 2)
women_means, women_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)
ind = np.arange(len(men_means))  # the x locations for the groups
width = 0.35  # the width of the bars
fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, men_means, width,
                color='SkyBlue', label='Men')
rects2 = ax.bar(ind + width/2, women_means, width,
                color='IndianRed', label='Women')
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(ind)
ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
ax.legend()
def autolabel(rects, xpos='center'):
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')
autolabel(rects1, "left")
autolabel(rects2, "right")
plt.show()