import matplotlib.pyplot as plt
import numpy
from fuzzy import MembershipArray

gene = [[[-0.9539658434541948,  -0.025565952540989922, -0.016246364446154682],
         [0.2892988027420131, 0.4649000608588642, 0.5085767386066072],
         [3, 0, 2, 0, 2, 3, 0, 1, 3, 0, 1, 2],
         [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
         [-165, -160, -87, -77, -58, -37, -32],
         [21, 28, 62, 102, 102, 127, 131]], 0]

gene = gene[0]
angle_geneN = sorted(gene[0])
angle_geneP = sorted(gene[1])

avoid_rule = gene[2]
thrust_rule = gene[3]
avoid_geneN = sorted(gene[4])
avoid_geneP = sorted(gene[5])

angle_geneN = [x * 360 for x in angle_geneN]
angle_geneP = [x * 360 for x in angle_geneP]

angleMF_values = [(-360, angle_geneN[0], angle_geneN[1]),
                  (angle_geneN[2], 0, angle_geneP[0]), (angle_geneP[1], angle_geneP[2], 360)]
shootMF_values = [(0, 3, 6), (4, 8, 10)]
targetRules = [0, 1, 0]

aimMF_values = [(-180, -90, -0.5), (-1, 0, 1), (0.5, 90, 180)]
steerMF_values = [(-100, -99, 1), (-2, 0, 2), (1, 99, 100)]
shootRules = [0, 1, 2]


collideMF_values = [(0, 80, 100), (80, 120, 160), (140, 160, 800)]
interceptMF_values = [(0, 0.8, 1.2), (0.8, 1.0, 10.0)]
# Outputs are NOTHING, TARGET, AVOID
threatMF_values = [(0, 0.6, 1.2), (1.0, 1.6, 2.2), (2.0, 2.5, 3.0)]
collideRules = [2, 1, 2, 1, 1, 0]


avoidMF_values = [(-180, avoid_geneN[0], avoid_geneN[1]), (avoid_geneN[2], avoid_geneN[3], avoid_geneN[4]),
                  (avoid_geneN[5], avoid_geneN[6], 0), (0, avoid_geneP[0], avoid_geneP[1]),
                  (avoid_geneP[2], avoid_geneP[3], avoid_geneP[4]), (avoid_geneP[5], avoid_geneP[6], 180)]

veerMF_values = [(100, 70, 40), (60, 30, 0), (0, -30, -60), (-40, -70, -100)]
thrustMF_values = [(-200, -150, 0), (0, 150, 200)]
