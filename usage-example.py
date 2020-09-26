from earclip import EarClipTriangulation
import numpy as np
import matplotlib

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

matplotlib.use("TkAgg")


def _get_triangles_patches(triangles):
    patches = []
    for triangle in triangles:
        patches.append(
            plt.Polygon(triangle.get_points(), closed=True, fill=None, edgecolor='g')
        )
    return patches


def _ear_clipping_animation(polygon, triangles):
    plt.style.use('ggplot')
    fig = plt.figure(figsize=(7, 7))
    axis_max = np.max(polygon, axis=0) + abs(np.max(polygon, axis=0) / 10)
    axis_min = np.min(polygon, axis=0) - abs(np.min(polygon, axis=0) / 10)
    distance = np.max([
        (abs(axis_min[0]) + abs(axis_max[0])), (abs(axis_min[1]) + abs(axis_max[1]))]
    )
    #with plt.style.context('dark_background'):
    ax = plt.axes(xlim=(axis_min[0], axis_min[0] + distance), ylim=(axis_min[1], axis_min[1] + distance))

    def init():
        polygon_frame = plt.Polygon(polygon, linewidth=1.4, closed=True, fill=None, edgecolor='gray')
        frame = ax.add_patch(polygon_frame)
        return frame,

    def animate(i):
        for i in range(0, (i % len(triangles))):
            tr = triangles[i]
            ax.arrow(tr.p1.x, tr.p1.y,
                     tr.p3.x - tr.p1.x,
                     tr.p3.y - tr.p1.y,
                     color="green",
                     alpha=0.8,
                     head_length=axis_max[0] / 250,
                     head_width=axis_max[0] / 250,
                     length_includes_head=True)
    anim = FuncAnimation(fig, animate, init_func=init, interval=400)
    plt.show()


n = 20
x = np.linspace(-10, 10, num=n)
y_top = np.sqrt(100 - x**2)
y_bot = -np.sqrt(100 - x**2)

xx = np.concatenate((np.flip(x)[:-1], x[:-1]))
yy = np.concatenate((y_top[:-1], y_bot[:-1]))
my_polygon = [[x,y] for x, y in zip(xx, yy)]
#
earclip = EarClipTriangulation()
triangles = earclip.triangulate(my_polygon)
_ear_clipping_animation(my_polygon, triangles)


# example 2
# star = [(150, 25), (179, 111), (269, 111), (197, 165), (223, 251), (150, 200), (77, 251), (103, 165), (31, 111), (121, 111)]
# moon = [(5, 15), (6, 14), (8, 12), (9, 10), (9, 8), (8, 6), (7, 4), (5, 2), (3, 1), (6, 1), (8, 1), (10, 2), (12, 4), (13, 7), (13, 10), (12, 12), (10, 14), (7, 15)]
# leave = [(1, -3), (5, -4), (4, -3), (9, 1), (7, 2), (8, 5), (5, 4), (5, 5), (3, 4), (4, 9), (2, 7), (0, 10), (-2, 7), (-4, 8), (-3, 3), (-5, 6), (-5, 4), (-8, 5), (-7, 2), (-9, 1), (-4, -3), (-5, -4), (0, -3), (2, -7), (2, -6), (1, -3)]
# my = np.array([(0, 0), (5, 5), (10, 0), (5, 10)])
# fig = moon
#
# earclip = EarClipTriangulation()
# triangles = earclip.triangulate(fig)
# _ear_clipping_animation(fig, triangles)
