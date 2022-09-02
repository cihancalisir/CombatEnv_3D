# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
#
# # plt.ion()
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
#
# for k in range(0,100):
#     ax.plot([0 + k*0.2], [0 + k*0.2], [0 + k*0.2], marker="*")
#     # plt.draw()
#     plt.pause(0.02)
#     ax.cla()

import matplotlib.pyplot as plt
import time
import random
from collections import deque
import numpy as np

# simulates input from serial port
def random_gen():
    while True:
        val = random.randint(1,10)
        yield val
        time.sleep(0.1)


a1 = deque([0]*100)
ax = plt.axes(xlim=(0, 20), ylim=(0, 10))
d = random_gen()

line, = plt.plot(a1)
plt.ion()
plt.ylim([0,10])
plt.show()

for i in range(0,20):
    a1.appendleft(next(d))
    datatoplot = a1.pop()
    line.set_ydata(a1)
    plt.draw()
    i += 1
    time.sleep(0.1)
    plt.pause(0.001)