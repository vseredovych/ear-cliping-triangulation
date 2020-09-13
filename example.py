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
    fig = plt.figure(figsize=(15, 15))
    axis_max = np.max(polygon, axis=0) * 1.1
    axis_min = np.min(polygon, axis=0) / 1.1
    #with plt.style.context('dark_background'):
    ax = plt.axes(xlim=(axis_min[0], axis_max[0]), ylim=(axis_min[1], axis_max[1]))

    def init():
        polygon_frame = plt.Polygon(polygon, linewidth=1.4, closed=True, fill=None, edgecolor='gray')
        frame = ax.add_patch(polygon_frame)
        return frame,

    def animate(i):
        for i in range(0, (i % len(polygon) - 1)):
            tr = triangles[i]
            #ax.plot(tr.p1.x, tr.p3.x], [tr.p1.y, tr.p3.y], "g")
            ax.arrow(tr.p1.x, tr.p1.y,
                     tr.p3.x - tr.p1.x,
                     tr.p3.y - tr.p1.y,
                     color="green",
                     alpha=0.8,
                     head_length=axis_max[0] / 250,
                     head_width=axis_max[0] / 250,
                     length_includes_head=True)
    anim = FuncAnimation(fig, animate, init_func=init, interval=100)
    plt.show()


star = np.array([(350, 75), (379, 161), (469, 161), (397, 215), (423, 301), (350, 250), (277, 301), (303, 215), (231, 161), (321, 161)])

earclip = EarClipTriangulation()
triangles = earclip.triangulate(star)
_ear_clipping_animation(star, triangles)


