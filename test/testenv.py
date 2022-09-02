import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from battle3Denv import Battle3DEnv
import random

class RuleAgent4Battle3DEnv:
    def __init__(self):
        pass

    def selectAction(self, state):
        action = 0
        relativeAngle = state[0]
        if relativeAngle > 20:
            action = 3

        return action



if __name__ == "__main__":
    render = True
    rule = False
    if rule:
        ruleAgent=RuleAgent4Battle3DEnv()
    env = Battle3DEnv()
    for e in range(100000):
        state = env.reset()
        done = False
        episodeReward = 0
        for timestep in range(200):
            action = {}
            missileEntityID = random.choices(range(4), [0.3, 0.3, 0.3, 0.1], k=1)[0]
            if rule:
                direction = ruleAgent.selectAction(state)
            else:
                direction = random.choices(range(21), k=1)[0]
            accerelation = random.choices(range(20), k=1)[0]
            action["chosedTarget"] = missileEntityID
            action['directionAction'] = direction
            action['accerelation'] = accerelation
            state, reward, done = env.step(action)
            episodeReward += reward
            # print(done)
            if render:
                env.render()
            if done:
                break
        print("episode: {} numofDeadEnities:{} reward: {}".format(e, state[2], episodeReward))
