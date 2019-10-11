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


# import numpy as np
# import matplotlib.pyplot as plt
# men_means, men_std = (20, 35, 30, 35, 27), (0, 3, 4, 1, 2)
# women_means, women_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)
# ind = np.arange(len(men_means))  # the x locations for the groups
# width = 0.35  # the width of the bars
# fig, ax = plt.subplots()
# rects1 = ax.bar(ind - width/2, men_means, width,
#                 color='SkyBlue', label='Men')
# rects2 = ax.bar(ind + width/2, women_means, width,
#                 color='IndianRed', label='Women')
# ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
# ax.set_xticks(ind)
# ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
# ax.legend()
# def autolabel(rects, xpos='center'):
#     xpos = xpos.lower()  # normalize the case of the parameter
#     ha = {'center': 'center', 'right': 'left', 'left': 'right'}
#     offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off
#
#     for rect in rects:
#         height = rect.get_height()
#         ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
#                 '{}'.format(height), ha=ha[xpos], va='bottom')
# autolabel(rects1, "left")
# autolabel(rects2, "right")
# plt.show()  # todo 画柱形图的


# import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
# sphinx_gallery_thumbnail_number = 2
# vegetables = ["cucumber", "tomato", "lettuce", "asparagus",
#               "potato", "wheat", "barley"]
# vegetables1 = [" ", " ", " ", " ",
#               " ", " ", " "]
# vegetables2 = ["a", "asd", "asd", "asd",
#               "zxc", "asd", "qwe"]
# farmers = ["Farmer Joe", "Upland Bros.", "Smith Gardening",
#            "Agrifun", "Organiculture", "BioGoods Ltd.", "Cornylee Corp."]
# harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
#                     [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
#                     [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
#                     [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
#                     [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
#                     [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
#                     [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])
# fig, ax = plt.subplots()
# im = ax.imshow(harvest)
# ax.set_xticks(np.arange(len(farmers)))
# ax.set_xticks(np.arange(len(farmers)+1)-.5, minor=True)
# ax.set_xticklabels(farmers)
# ax.set_yticks(np.arange(len(vegetables)))
# ax.set_yticks(np.arange(len(vegetables)+1)-.5, minor=True)
# # ax.set_yticklabels(['' for _ in range(len(vegetables))])
# ax.set_yticklabels(vegetables)
# # ... and label them with the respective list entries
# # ax.set_yticklabels([1,2,3,4,5,6,7])
# # ax.set_yticklabels([str(i) for i in range(len(vegetables))])
# ax.grid(which="minor", color="w", linestyle='-', linewidth=0)
# # Rotate the tick labels and set their alignment.
# plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#          rotation_mode="anchor")
# # Loop over data dimensions and create text annotations.
# for i in range(len(vegetables)):
#     for j in range(len(farmers)):
#         text = ax.text(j, i, harvest[i, j],
#                        ha="center", va="center", color="w")
# ax.set_title("Harvest of local farmers (in tons/year)")
# fig.tight_layout()
# plt.show()



# import matplotlib.pyplot as plt
# def make_patch_spines_invisible(ax):
#     ax.set_frame_on(True)
#     ax.patch.set_visible(False)
#     for sp in ax.spines.values():
#         sp.set_visible(False)
# fig, host = plt.subplots()
# # fig.subplots_adjust(right=0.75)
# par1 = host.twinx()
# par2 = host.twinx()
# # Offset the right spine of par2.  The ticks and label have already been
# # placed on the right by twinx above.
# par2.spines["right"].set_position(("axes", 1.2))
# # Having been created by twinx, par2 has its frame off, so the line of its
# # detached spine is invisible.  First, activate the frame but make the patch
# # and spines invisible.
# make_patch_spines_invisible(par2)
# # Second, show the right spine.
# par2.spines["right"].set_visible(True)
# p1, = host.plot([0, 1, 2], [0, 1, 2], "b-", label="Density")
# p2, = par1.plot([0, 1, 2], [0, 3, 2], "r-", label="Temperature")
# p3, = par2.plot([0, 1, 2], [50, 30, 15], "g-", label="Velocity")
# host.set_xlim(0, 2)
# host.set_ylim(0, 2)
# par1.set_ylim(0, 4)
# par2.set_ylim(1, 65)
# host.set_xlabel("Distance")
# host.set_ylabel("Density")
# par1.set_ylabel("Temperature")
# par2.set_ylabel("Velocity")
# host.yaxis.label.set_color(p1.get_color())
# par1.yaxis.label.set_color(p2.get_color())
# par2.yaxis.label.set_color(p3.get_color())
# tkw = dict(size=4, width=1.5)
# host.tick_params(axis='y', colors=p1.get_color(), **tkw)
# par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
# par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
# host.tick_params(axis='x', **tkw)
# lines = [p1, p2, p3]
# host.legend(lines, [l.get_label() for l in lines])
# plt.show()



import numpy as np
import matplotlib.pyplot as plt
men_means, men_std = (20, 35, 30, 35, 27), (2, 3, 4, 1, 2)
women_means, women_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)
midde_means, midde_std = (25, 32, 34, 20, 25), (3, 5, 2, 3, 3)
ind = np.arange(len(men_means))  # the x locations for the groups
width = 0.2  # the width of the bars
fig, ax = plt.subplots()
rects1 = ax.barh(ind - width/2, men_means, width,
                color='SkyBlue', label='Men')
rects2 = ax.barh(ind + width/2, women_means, width,
                color='r', label='Women')
rects3 = ax.barh(ind + width/2 + width, midde_means, width,
                color='IndianRed', label='midde')
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_yticks(ind)
ax.set_yticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
ax.legend()
def autolabel(rects, xpos='center'):
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off
    for rect in rects:
        width = rect.get_width()
        text = '{}'.format(111)
        ax.text(1.01 * rect.get_width(), rect.get_y(), text, va='bottom')
rects1_values = []
for rects in [rects1, rects2, rects2]:
    _rects1_values = []
    for rect in rects:
        _rects1_values.append(rect.get_height())
    rects1_values.append(np.array(_rects1_values))
autolabel(rects1, "center")
autolabel(rects2, "center")
autolabel(rects3, "center")
plt.show()


import matplotlib.pyplot as plt
import numpy as np
np.random.seed(19680801)
width = 0.2
plt.rcdefaults()
fig, ax = plt.subplots()

people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
y_pos = np.arange(len(people))
performance = 3 + 10 * np.random.rand(len(people))
error = np.random.rand(len(people))

ax.barh(y_pos - width/2, performance, width, xerr=error, align='center',
        color='green', ecolor='black')
ax.barh(y_pos + width/2, performance, width, xerr=error, align='center',
        color='red', ecolor='black')
print(y_pos, people)
ax.set_yticks(y_pos)
ax.set_yticklabels(people)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Performance')
ax.set_title('How fast do you want to go today?')

plt.show()
