from math import sin, cos, radians, pi
import numpy as np


class Enemy:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x #np.random.randint(-40000, 40000, 1)[0]
        self.y = y #np.random.randint(-40000, 40000, 1)[0]
        self.z = z
        self.dead = False

class Player:
    def __init__(self, lenTrajectory, limit):
        self.x = np.random.randint(2000, limit, 1)[0]
        self.y = np.random.randint(2000, limit, 1)[0]
        self.z = 1000
        self.speed = 200
        self.lenTrajectory = lenTrajectory
        self.trajectory_X = [self.x]
        self.trajectory_Y = [self.y]
        self.trajectory_Z = [self.z]
        self.preheadAngle = 0
        self.head_pos(x0=self.x, y0=self.y, d=200, theta=np.random.randint(360))
        self.assignedTargetID = 0

    def head_pos(self, x0, y0, d, theta):
        theta = theta + self.preheadAngle
        self.headAngle = pi/2 - radians(theta)
        self.preheadAngle = theta
        self.target_x, self.target_y = x0 + 30 * d * cos(self.headAngle) , y0 + 30 * d * sin(self.headAngle)


    def move2D(self, acceleration):
        self.dx = cos(self.headAngle) * acceleration * self.speed
        self.dy = sin(self.headAngle) * acceleration * self.speed
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.trajectory_X.append(self.x)
        self.trajectory_Y.append(self.y)
        self.trajectory_Z.append(self.z)
        if len(self.trajectory_X) > self.lenTrajectory: self.trajectory_X.pop(0)
        if len(self.trajectory_Y) > self.lenTrajectory: self.trajectory_Y.pop(0)
        if len(self.trajectory_Z) > self.lenTrajectory: self.trajectory_Z.pop(0)

    def move(self, angle, head_distance, acceleration, moving=True):
        self.head_pos(x0=self.x, y0=self.y, d=head_distance, theta=angle)
        if moving: self.move2D(acceleration)