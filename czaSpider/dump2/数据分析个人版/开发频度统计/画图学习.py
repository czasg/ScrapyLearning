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

# import matplotlib.pyplot as plt
# labels = 'Frogs', 'Hogs'
# fracs = [15, 30]
# fig = plt.figure(1, figsize=(9, 10))
# fig.set_label('123')
#
# def draw(xyz=(0, 0, 0)):
#     a = fig.add_subplot(*xyz)
#     if (xyz[2] - 1) % 5 == 0:
#         a.set_ylabel('123')
#     autotexts = plt.pie(fracs, autopct=lambda pct: func(pct, fracs), shadow=True, colors=['red', 'skyblue'])[2]
#     plt.setp(autotexts, size='x-small')
# count = 1
# for i in range(1,6):
#     for j in range(1, 6):
#         draw(xyz=(6, 5, count))
#         count += 1
# fig.legend(labels, loc="upper right")
# ax = plt.subplot(616)
# ind = np.arange(5)
# width = 0.25
# plt.bar(ind-width/2, [1, 2, 3, 4, 5], width, color='red')
# plt.bar(ind+width/2, [1, 2, 3, 4, 5], width, color='skyblue')
# ax.set_xticks(ind)
# ax.set_xticklabels(['czd', 'asd', '123', 'ased', 'afsdf'])
# plt.show()


from collections import Counter
a = Counter([1,2,3,3,3,3,3,3])
print(a)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
def radar_factory(num_vars, frame='circle'):
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    def draw_poly_patch(self):
        verts = unit_poly_verts(theta + np.pi / 2)
        return plt.Polygon(verts, closed=True, edgecolor='k')
    def draw_circle_patch(self):
        return plt.Circle((0.5, 0.5), 0.5)
    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)
    class RadarAxes(PolarAxes):
        name = 'radar'
        RESOLUTION = 1
        draw_patch = patch_dict[frame]
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.set_theta_zero_location('N')
        def fill(self, *args, closed=True, **kwargs):
            return super().fill(closed=closed, *args, **kwargs)
        def plot(self, *args, **kwargs):
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)
        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)
        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)
        def _gen_axes_patch(self):
            return self.draw_patch()
        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            spine_type = 'circle'
            verts = unit_poly_verts(theta + np.pi / 2)
            verts.append(verts[0])
            path = Path(verts)
            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}
    register_projection(RadarAxes)
    return theta
def unit_poly_verts(theta):
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts
def example_data():
    data = [
        ['Sulfate', 'Nitrate', 'EC', 'OC1', 'OC2', 'OC3', 'OP', 'CO', 'O3'],
        ('Basecase', [
            # [0.88, 0.01, 0.03, 0.03, 0.00, 0.06, 0.01, 0.00, 0.00],
            # [0.07, 0.95, 0.04, 0.05, 0.00, 0.02, 0.01, 0.00, 0.00],
            # [0.01, 0.02, 0.85, 0.19, 0.05, 0.10, 0.00, 0.00, 0.00],
            # [0.02, 0.01, 0.07, 0.01, 0.21, 0.12, 0.98, 0.00, 0.00],
            [0.01, 0.01, 0.02, 0.71, 0.74, 0.70, 0.00, 0.00, 0.00]]),
        ('With CO', [
            # [0.88, 0.02, 0.02, 0.02, 0.00, 0.05, 0.00, 0.05, 0.00],
            # [0.08, 0.94, 0.04, 0.02, 0.00, 0.01, 0.12, 0.04, 0.00],
            # [0.01, 0.01, 0.79, 0.10, 0.00, 0.05, 0.00, 0.31, 0.00],
            # [0.00, 0.02, 0.03, 0.38, 0.31, 0.31, 0.00, 0.59, 0.00],
            [0.02, 0.02, 0.11, 0.47, 0.69, 0.58, 0.88, 0.00, 0.00]]),
        ('With O3', [
            # [0.89, 0.01, 0.07, 0.00, 0.00, 0.05, 0.00, 0.00, 0.03],
            # [0.07, 0.95, 0.05, 0.04, 0.00, 0.02, 0.12, 0.00, 0.00],
            # [0.01, 0.02, 0.86, 0.27, 0.16, 0.19, 0.00, 0.00, 0.00],
            # [0.01, 0.03, 0.00, 0.32, 0.29, 0.27, 0.00, 0.00, 0.95],
            [0.02, 0.00, 0.03, 0.37, 0.56, 0.47, 0.87, 0.00, 0.00]]),
        ('CO & O3', [
            # [0.87, 0.01, 0.08, 0.00, 0.00, 0.04, 0.00, 0.00, 0.01],
            # [0.09, 0.95, 0.02, 0.03, 0.00, 0.01, 0.13, 0.06, 0.00],
            # [0.01, 0.02, 0.71, 0.24, 0.13, 0.16, 0.00, 0.50, 0.00],
            # [0.01, 0.03, 0.00, 0.28, 0.24, 0.23, 0.00, 0.44, 0.88],
            [0.02, 0.00, 0.18, 0.45, 0.64, 0.55, 0.86, 0.00, 0.16]]),
        ('Basecase', [
            # [0.88, 0.01, 0.03, 0.03, 0.00, 0.06, 0.01, 0.00, 0.00],
            # [0.07, 0.95, 0.04, 0.05, 0.00, 0.02, 0.01, 0.00, 0.00],
            # [0.01, 0.02, 0.85, 0.19, 0.05, 0.10, 0.00, 0.00, 0.00],
            # [0.02, 0.01, 0.07, 0.01, 0.21, 0.12, 0.98, 0.00, 0.00],
            [0.01, 0.01, 0.02, 0.71, 0.74, 0.70, 0.00, 0.00, 0.00]]),
        ('With CO', [
            # [0.88, 0.02, 0.02, 0.02, 0.00, 0.05, 0.00, 0.05, 0.00],
            # [0.08, 0.94, 0.04, 0.02, 0.00, 0.01, 0.12, 0.04, 0.00],
            # [0.01, 0.01, 0.79, 0.10, 0.00, 0.05, 0.00, 0.31, 0.00],
            # [0.00, 0.02, 0.03, 0.38, 0.31, 0.31, 0.00, 0.59, 0.00],
            [0.02, 0.02, 0.11, 0.47, 0.69, 0.58, 0.88, 0.00, 0.00]]),
        ('With O3', [
            # [0.89, 0.01, 0.07, 0.00, 0.00, 0.05, 0.00, 0.00, 0.03],
            # [0.07, 0.95, 0.05, 0.04, 0.00, 0.02, 0.12, 0.00, 0.00],
            # [0.01, 0.02, 0.86, 0.27, 0.16, 0.19, 0.00, 0.00, 0.00],
            # [0.01, 0.03, 0.00, 0.32, 0.29, 0.27, 0.00, 0.00, 0.95],
            [0.02, 0.00, 0.03, 0.37, 0.56, 0.47, 0.87, 0.00, 0.00]]),
        ('CO & O3', [
            # [0.87, 0.01, 0.08, 0.00, 0.00, 0.04, 0.00, 0.00, 0.01],
            # [0.09, 0.95, 0.02, 0.03, 0.00, 0.01, 0.13, 0.06, 0.00],
            # [0.01, 0.02, 0.71, 0.24, 0.13, 0.16, 0.00, 0.50, 0.00],
            # [0.01, 0.03, 0.00, 0.28, 0.24, 0.23, 0.00, 0.44, 0.88],
            [0.02, 0.00, 0.18, 0.45, 0.64, 0.55, 0.86, 0.00, 0.16]]),
        ('With O3', [
            # [0.89, 0.01, 0.07, 0.00, 0.00, 0.05, 0.00, 0.00, 0.03],
            # [0.07, 0.95, 0.05, 0.04, 0.00, 0.02, 0.12, 0.00, 0.00],
            # [0.01, 0.02, 0.86, 0.27, 0.16, 0.19, 0.00, 0.00, 0.00],
            # [0.01, 0.03, 0.00, 0.32, 0.29, 0.27, 0.00, 0.00, 0.95],
            [0.02, 0.00, 0.03, 0.37, 0.56, 0.47, 0.87, 0.00, 0.00]]),
        ('CO', [
            # [0.87, 0.01, 0.08, 0.00, 0.00, 0.04, 0.00, 0.00, 0.01],
            # [0.09, 0.95, 0.02, 0.03, 0.00, 0.01, 0.13, 0.06, 0.00],
            # [0.01, 0.02, 0.71, 0.24, 0.13, 0.16, 0.00, 0.50, 0.00],
            # [0.01, 0.03, 0.00, 0.28, 0.24, 0.23, 0.00, 0.44, 0.88],
            [0.02, 0.00, 0.18, 0.45, 0.64, 0.55, 0.86, 0.00, 0.16]])
    ]
    return data


if __name__ == '__main__':
    N = 9
    theta = radar_factory(N, frame='polygon')

    data = example_data()
    spoke_labels = data.pop(0)

    fig, axes = plt.subplots(figsize=(9, 16), nrows=5, ncols=2,
                             subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ['b', 'r', 'g', 'm', 'y']
    # Plot the four cases from the example data on separate axes
    for ax, (title, case_data) in zip(axes.flatten(), data):
        ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
        ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.1),
                     horizontalalignment='center', verticalalignment='center')
        for d, color in zip(case_data, colors):
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    ax = axes[0, 0]
    # labels = ('Factor 1', 'Factor 2', 'Factor 3', 'Factor 4', 'Factor 5')
    labels = ('Factor 1')
    legend = ax.legend(labels, loc=(0.9, .95),
                       labelspacing=0.1, fontsize='small')

    fig.text(0.5, 0.965, '5-Factor Solution Profiles Across Four Scenarios',
             horizontalalignment='center', color='black', weight='bold',
             size='large')

    plt.show()