# import matplotlib.pyplot as plt
# # Some data
# labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
# fracs = [15, 30, 45, 10]
# # Make figure and axes
# fig, axs = plt.subplots(2, 2)
# # A standard pie plot
# axs[0, 0].pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)
# # Shift the second slice using explode
# axs[0, 1].pie(fracs, labels=labels, autopct='%.0f%%', shadow=True,
#               explode=(0, 0.1, 0, 0))
# # Adapt radius and text size for a smaller pie
# patches, texts, autotexts = axs[1, 0].pie(fracs, labels=labels,
#                                           autopct='%.0f%%',
#                                           textprops={'size': 'smaller'},
#                                           shadow=True, radius=0.5)
# # Make percent texts even smaller
# plt.setp(autotexts, size='x-small')
# autotexts[0].set_color('white')
# # Use a smaller explode and turn of the shadow for better visibility
# patches, texts, autotexts = axs[1, 1].pie(fracs, labels=labels,
#                                           autopct='%.0f%%',
#                                           textprops={'size': 'smaller'},
#                                           shadow=False, radius=0.5,
#                                           explode=(0, 0.05, 0, 0))
# plt.setp(autotexts, size='x-small')
# autotexts[0].set_color('white')
#
# plt.show()



import numpy as np
# import matplotlib.pyplot as plt
# fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
# recipe = ["375 g flour",
#           "75 g sugar",
#           "250 g butter",
#           "300 g berries"]
# data = [float(x.split()[0]) for x in recipe]
# ingredients = [x.split()[-1] for x in recipe]

# wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
#                                   textprops=dict(color="w"))
# ax.legend(wedges, ingredients,
#           title="Ingredients",
#           loc="center left",
#           bbox_to_anchor=(1, 0, 0.5, 1))
# plt.setp(autotexts, size=8, weight="bold")
# ax.set_title("Matplotlib bakery: A pie")
# plt.show()




#
# fig, axs = plt.subplots(6, 5)
# plt.xlabel('test')
# plt.ylabel('test')
# def draw(xy=(0, 0)):
#     autotexts = axs[xy].pie(fracs, autopct=lambda pct: func(pct, fracs), shadow=True)[2]
#     plt.setp(autotexts, size='x-small')
# for i in range(5):
#     for j in range(5):
#         draw(xy=(i, j))
# # axs[(6,5)].plot(['1', '2', '3', '4', '5'])
# fig.legend(labels, loc="upper right")
# fig.set_size_inches(9, 10)
#
# plt.show()

import matplotlib.pyplot as plt
labels = 'Frogs', 'Hogs'
fracs = [15, 30]
fig = plt.figure(1, figsize=(9, 10))
fig.set_label('123')

def draw(xyz=(0, 0, 0)):
    a = fig.add_subplot(*xyz)
    if (xyz[2] - 1) % 5 == 0:
        a.set_ylabel('123')
    autotexts = plt.pie(fracs, autopct=lambda pct: func(pct, fracs), shadow=True, colors=['red', 'skyblue'])[2]
    plt.setp(autotexts, size='x-small')
count = 1
for i in range(1,6):
    for j in range(1, 6):
        draw(xyz=(6, 5, count))
        count += 1
fig.legend(labels, loc="upper right")
ax = plt.subplot(616)
ind = np.arange(5)
width = 0.25
plt.bar(ind-width/2, [1, 2, 3, 4, 5], width, color='red')
plt.bar(ind+width/2, [1, 2, 3, 4, 5], width, color='skyblue')
ax.set_xticks(ind)
ax.set_xticklabels(['czd', 'asd', '123', 'ased', 'afsdf'])
plt.show()