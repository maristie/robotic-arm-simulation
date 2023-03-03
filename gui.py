import algorithms
import math
import matplotlib.pyplot as plt
import numpy as np
import time
from arm import Arm
from matplotlib import collections as mc


WIDTH = 10
HEIGHT = 8
DPI = 100
RADIUS = 300
INTERVAL = 20
PRECISION = 0.01
GREEN_COLOR = (0, 1, 0, 1)
INTERPOLATION = 20
SLEEP_TIME = 0.25
MARKER_SIZE = 5
MARKER_COLOR = 'red'


fig = plt.figure(figsize=(WIDTH, HEIGHT), dpi=DPI)
ax = fig.add_subplot(1, 1, 1)
curr_arm = Arm()


def set_ax(arm, points=None):
    """
    Set up Cartesian axes and the arms
    """
    # Set ticks (intervals)
    xrange = np.arange(-RADIUS, RADIUS+1, INTERVAL)
    yrange = np.arange(0, RADIUS+1, INTERVAL)

    ax.set_xticks(xrange)
    ax.set_yticks(yrange)
    ax.set_aspect('equal')

    # Add grid
    ax.grid(which='both')

    # Draw circle
    t = np.arange(-RADIUS, RADIUS + PRECISION, PRECISION)
    ax.plot(t, np.sqrt(RADIUS**2 - t**2))

    # Draw points
    if points:
        for x, y in points:
            ax.plot(x, y, marker='o', markersize=MARKER_SIZE,
                    markerfacecolor=MARKER_COLOR)

    # Draw arm lines
    x1, y1 = arm.eval(point='B')
    x2, y2 = arm.eval(point='C')
    x3, y3 = arm.eval(point='D')
    lines = [[(0, 0), (x1, y1)], [(x1, y1), (x2, y2)], [(x2, y2), (x3, y3)]]
    ax.add_collection(mc.LineCollection(lines, colors=GREEN_COLOR))


def redraw(arm, points=None):
    """Redraw the given arm."""
    ax.clear()
    set_ax(arm, points)
    fig.canvas.draw()
    fig.canvas.flush_events()


def print_info(curr_arm, prev_arm, ordinal):
    """Print required informaiton of the current arm in one row."""
    bpos, cpos, dpos = curr_arm.eval(point='B'), curr_arm.eval(
        point='C'), curr_arm.eval(point='D')
    abangle, bcangle, cdangle = map(math.degrees, [
                                    curr_arm.alpha - math.pi/2, curr_arm.beta + math.pi/2, curr_arm.gamma + math.pi])
    if prev_arm is not None:
        delta1, delta2, delta3 = map(math.degrees, [abs(curr_arm.alpha - prev_arm.alpha), abs(
            curr_arm.beta - prev_arm.beta), abs(curr_arm.gamma - prev_arm.gamma)])
        maxdelta = max(delta1, delta2, delta3)
    else:
        delta1 = delta2 = delta3 = maxdelta = '---'
    print(f'{ordinal} ({bpos[0]}, {bpos[1]}) {abangle} {delta1} ({cpos[0]}, {cpos[1]}) {bcangle} {delta2} ({dpos[0]}, {dpos[1]}) {cdangle} {delta3} {maxdelta}')


def on_click(event):
    """Listen to mouse click event, and calculate, draw and print the 21 solutions."""
    global curr_arm
    print('Dot# B_Pos AB_Angle Delta_AB C_Pos BC_Angle Delta_BC D_Pos CD_Angle Delta_CD')
    print_info(curr_arm, None, 1)
    new_arm = algorithms.optimize(curr_arm, event.xdata, event.ydata)
    curr_pos, new_pos = curr_arm.eval(), new_arm.eval()
    dx, dy = (new_pos[0] - curr_pos[0]) / \
        INTERPOLATION, (new_pos[1] - curr_pos[1]) / INTERPOLATION
    points = [(curr_pos[0] + dx * i, curr_pos[1] + dy * i)
              for i in range(0, 1 + INTERPOLATION)]
    for i in range(1, 1 + INTERPOLATION):
        x, y = curr_pos[0] + dx * i, curr_pos[1] + dy * i
        next_arm = algorithms.optimize(curr_arm, x, y)
        print_info(next_arm, curr_arm, i+1)
        curr_arm = next_arm
        redraw(curr_arm, points)
        time.sleep(SLEEP_TIME)


# Set up initial arm, and draw
set_ax(curr_arm)
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.draw()
plt.tight_layout()
plt.show()
