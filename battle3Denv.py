import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import math
import random
import time
from entities import Enemy, Player


class Battle3DEnv:
    def __init__(self):
        plt.close("all")
        self.fig = plt.figure(figsize=(14, 6))
        self.mapSize = 160 * 1000
        self.ax1 = self.fig.add_subplot(111, projection='3d')
        self.num_enemy = 3
        self.enemies = []
        self.ax1.set_xlabel('x')
        self.ax1.set_ylabel('y')
        self.ax1.set_zlabel('z')
        self.ax1.set_xlim(0, self.mapSize)
        self.ax1.set_ylim(0, self.mapSize)
        self.ax1.set_zlim(0, 2000)
        self.lines = []
        self.bullet = False
        self.bullets = []
        self.bulletLife = 15
        self.trajectoryLen = 1000
        self.x_b = []
        self.y_b = []
        self.z_b = []
        self.episode = 0
        self.deadEntities = 0
        self.relAngleWRTAssignedTarget = 0

    def resetParams(self):
        self.deadEntities = 0
        plt.close("all")
        self.fig = plt.figure(figsize=(16, 8))
        self.ax1 = p3.Axes3D(self.fig)
        e_coors = [int(self.mapSize / 2) - 5000, int(self.mapSize / 2), int(self.mapSize / 2) + 5000]
        self.enemies = []
        for i in range(self.num_enemy):
            e = Enemy(x=int(self.mapSize / 2), y=e_coors[i], z=0)
            self.ax1.plot([e.x], [e.y], [e.z], color='r', markersize=10, marker="o")
            self.ax1.text(e.x, e.y, e.z, "e-{}".format(i), color='black')
            self.enemies.append(e)

        self.ax1.set_xlabel('x')
        self.ax1.set_ylabel('y')
        self.ax1.set_zlabel('z')
        self.ax1.set_xlim(0, self.mapSize)
        self.ax1.set_ylim(0, self.mapSize)
        self.ax1.set_zlim(0, 2000)
        self.lines = []
        self.bullet = False
        self.bullets = []
        self.bulletLife = 15
        self.trajectoryLen = 30
        self.x_b = []
        self.y_b = []
        self.z_b = []
        self.timeStep = 0
        self.agent = Player(self.trajectoryLen, self.mapSize)
        self.agent.assignedTargetID = np.random.randint(self.num_enemy)
        self.agent.move(np.random.randint(360), head_distance=200, acceleration=0, moving=False)
        self.getRelativeAngle()
        self.enemyIDs = list(range(self.num_enemy))

    def reset(self):
        self.resetParams()
        p1 = np.array([self.agent.x, self.agent.y, self.agent.z]) * 0.001
        p2 = np.array([self.enemies[self.agent.assignedTargetID].x, self.enemies[self.agent.assignedTargetID].y, self.enemies[self.agent.assignedTargetID].z]) * 0.001
        dist = np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
        state = [self.relAngleWRTAssignedTarget, dist, self.deadEntities]
        return state

    def getAngle(self, a, b, c):
        ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
        ang = ang + 360 if ang < 0 else ang
        ang = 360 - ang if ang > 180 else ang
        return ang

    def getRelativeAngle(self):
        self.relAngleWRTAssignedTarget = self.getAngle((self.agent.target_x, self.agent.target_y),
                       (self.agent.trajectory_X[-1], self.agent.trajectory_Y[-1]),
                       (self.enemies[self.agent.assignedTargetID].x, self.enemies[self.agent.assignedTargetID].y))
        self.ax1.text2D(0.0, 0.92, "angle btwn enemy-{}-agent: {}".format(self.agent.assignedTargetID, self.relAngleWRTAssignedTarget), transform=self.ax1.transAxes, bbox=dict(facecolor='g', alpha=0.15))

        self.ax1.text2D(0.0, 0.89, "headAngle: {}".format(math.degrees(self.agent.headAngle)%360),
                        transform=self.ax1.transAxes, bbox=dict(facecolor='g', alpha=0.15))


    def step(self, actionDict):
        reward = -0.007
        done = False
        targetID = actionDict["chosedTarget"]
        directionAction = actionDict['directionAction']
        acceleration = actionDict['accerelation']
        angle = directionAction * 3 if directionAction <= 10 else -(directionAction-10) * 3
        self.agent.move(angle, head_distance=200, acceleration=acceleration, moving=True)
        self.getRelativeAngle()

        reward -= self.relAngleWRTAssignedTarget / 60

        p1 = np.array([self.agent.x, self.agent.y, self.agent.z]) * 0.001
        p2 = np.array([self.enemies[self.agent.assignedTargetID].x, self.enemies[self.agent.assignedTargetID].y, self.enemies[self.agent.assignedTargetID].z]) * 0.001
        dist = np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
        # for y, enemy in enumerate(self.enemies):
        #     p2 = np.array([enemy.x, enemy.y, enemy.z]) * 0.001
        #     dist = np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
        #     self.ax1.text2D(0.0, 0.91 - y * 0.03, "dist to enemy-{}: {}".format(y, dist),
        #                     transform=self.ax1.transAxes, bbox=dict(facecolor='g', alpha=0.15))


        if self.timeStep < self.trajectoryLen:
            self.ax1.plot(self.agent.trajectory_X[:-1], self.agent.trajectory_Y[:-1], self.agent.trajectory_Z[:-1], color='green', markersize=1, marker=".")
        else:
            self.ax1.plot(self.agent.trajectory_X[-self.trajectoryLen:-1], self.agent.trajectory_Y[-self.trajectoryLen:-1],
                                   self.agent.trajectory_Z[-self.trajectoryLen:-1], color='green', markersize=1, marker=".")

        self.ax1.plot([self.agent.trajectory_X[-1]], [self.agent.trajectory_Y[-1]], [self.agent.trajectory_Z[-1]],
                           color='b', marker='.', markeredgecolor='b', markersize=20)
        # self.ax1.plot([self.agent.target_x], [self.agent.target_y], [self.agent.trajectory_Z[-1]],
        #                    color='g', marker='.', markeredgecolor='g', markersize=5)

        X = [self.agent.trajectory_X[-1], self.agent.target_x]
        Y = [self.agent.trajectory_Y[-1], self.agent.target_y]
        Z = [self.agent.trajectory_Z[-1], self.agent.trajectory_Z[-1]]
        self.ax1.plot(X, Y, Z, c="r") # add head line


        if not targetID == 3 and targetID==self.agent.assignedTargetID:
            p2 = np.array([self.enemies[targetID].x, self.enemies[targetID].y, self.enemies[targetID].z]) * 0.001 # m to km
            dist = np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2)
            if dist < 12: # füze menzili max 10 km
                targetEnemy = self.enemies[targetID]
                x_b = np.linspace(self.agent.trajectory_X[-1], targetEnemy.x, self.bulletLife)
                y_b = np.linspace(self.agent.trajectory_Y[-1], targetEnemy.y, self.bulletLife)
                z_b = np.linspace(self.agent.trajectory_Z[-1], targetEnemy.z, self.bulletLife)
                bulletTimer = 0
                # print("bullet")
                reward -= 10
                self.bullets.append([x_b, y_b, z_b, bulletTimer, targetID])

        if len(self.bullets) != 0:
            for k, bullet in enumerate(self.bullets):
                bullet_x = bullet[0][bullet[3]]
                bullet_y = bullet[1][bullet[3]]
                bullet_z = bullet[2][bullet[3]]
                bullet[3] = bullet[3] + 1

                if bullet[3] == self.bulletLife: # füze hedefe ulaştı mı?
                    self.bullets.pop(k)
                    enemyDead = random.choices(range(2), [0.75, 0.25], k=1)[0]
                    if enemyDead == 1:
                        enemy = self.enemies[self.agent.assignedTargetID]
                        if enemy.x == bullet_x and enemy.y == bullet_y and enemy.z == bullet_z:
                            # ödül alacak
                            self.enemies[self.agent.assignedTargetID].dead = True
                            reward += 100
                            self.deadEntities += 1
                            if not self.deadEntities == self.num_enemy: # sağ kalan varsa birini daha seç
                                self.agent.assignedTargetID = random.choices(self.enemyIDs, k=1)[0]
                                enemy = self.enemies[self.agent.assignedTargetID]
                                while enemy.dead: # assign new target
                                    self.agent.assignedTargetID = random.choices(self.enemyIDs, k=1)[0]
                                    enemy = self.enemies[self.agent.assignedTargetID]

                else:
                    self.ax1.plot([bullet_x], [bullet_y], [bullet_z],
                                                marker='.', markeredgecolor='black',
                                                markersize=2)  # füzeyi adım adım çiz

        self.timeStep += 1
        aliveEnemies = len(self.enemies)
        for no, e in enumerate(self.enemies):
            if e.dead:
                aliveEnemies -= 1
                self.ax1.plot([e.x], [e.y], [e.z], color='y', markersize=5, marker="o")
                self.ax1.text(e.x+20, e.y, e.z, " {}".format(no), color='black')
            else:
                self.ax1.plot([e.x], [e.y], [e.z], color='r', markersize=5, marker="o")
                self.ax1.text(e.x+20, e.y, e.z, " {}".format(no), color='black')

        self.aliveEnemies = aliveEnemies
        if aliveEnemies == 0:
            self.episode += 1
            done = True
        state = [self.relAngleWRTAssignedTarget, dist, self.deadEntities]
        return state, reward, done

    def render(self):
        time.sleep(0.001)
        self.ax1.text2D(0.0, 0.98, "Episode/Timestep: {}/{}".format(self.episode, self.timeStep),
                        transform=self.ax1.transAxes, bbox=dict(facecolor='b', alpha=0.15))
        self.ax1.text2D(0.0, 0.95, "Num. enemies: {}".format(self.aliveEnemies),
                        transform=self.ax1.transAxes, bbox=dict(facecolor='r', alpha=0.15))
        self.ax1.set_xlabel('x')
        self.ax1.set_ylabel('y')
        self.ax1.set_zlabel('z')
        self.ax1.set_xlim(0, self.mapSize)
        self.ax1.set_ylim(0, self.mapSize)
        self.ax1.set_zlim(0, 2000)
        plt.pause(0.002)
        plt.draw()
        plt.cla()
        # plt.show()




