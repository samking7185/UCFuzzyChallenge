import matplotlib.pyplot as plt
import numpy as np
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

angleX = np.linspace(-180, 180, num=1000)
angleMFA1 = MembershipArray(angleMF_values[0])
angleMFA2 = MembershipArray(angleMF_values[1])
angleMFA3 = MembershipArray(angleMF_values[2])

angleMF1 = angleMFA1.lshlder(angleX)
angleMF2 = angleMFA2.triangle(angleX)
angleMF3 = angleMFA3.rshlder(angleX)

plt.figure(1)
plt.plot(angleX, angleMF1, label='Negative')
plt.plot(angleX, angleMF2, label='Zero')
plt.plot(angleX, angleMF3, label='Positive')
plt.xlabel('Angle (deg)')
plt.ylabel('Membership')
plt.title('targetFIS Angle Input')
plt.axis([-180, 180, 0, 1.1])
plt.legend()

shootX = np.linspace(0, 10, num=100)
shootMFA1 = MembershipArray(shootMF_values[0])
shootMFA2 = MembershipArray(shootMF_values[1])

shootMF1 = shootMFA1.lshlder(shootX)
shootMF2 = shootMFA2.rshlder(shootX)

plt.figure(2)
plt.plot(shootX, shootMF1, label='Nothing')
plt.plot(shootX, shootMF2, label='Fire')
plt.xlabel('Value')
plt.ylabel('Membership')
plt.title('targetFIS Fire Output')
plt.axis([0, 10, 0, 1.1])
plt.legend()

aimX = np.linspace(-180, 180, num=1000)
aimMFA1 = MembershipArray(aimMF_values[0])
aimMFA2 = MembershipArray(aimMF_values[1])
aimMFA3 = MembershipArray(aimMF_values[2])

aimMF1 = aimMFA1.lshlder(aimX)
aimMF2 = aimMFA2.triangle(aimX)
aimMF3 = aimMFA3.rshlder(aimX)

plt.figure(3)
plt.plot(aimX, aimMF1, label='Negative')
plt.plot(aimX, aimMF2, label='Zero')
plt.plot(aimX, aimMF3, label='Positive')
plt.xlabel('Angle (deg)')
plt.ylabel('Membership')
plt.title('shootFIS Angle Input')
plt.axis([-180, 180, 0, 1.1])
plt.legend()

steerX = np.linspace(-100, 100, num=1000)
steerMFA1 = MembershipArray(steerMF_values[0])
steerMFA2 = MembershipArray(steerMF_values[1])
steerMFA3 = MembershipArray(steerMF_values[2])

steerMF1 = steerMFA1.triangle(steerX)
steerMF2 = steerMFA2.triangle(steerX)
steerMF3 = steerMFA3.triangle(steerX)

plt.figure(4)
plt.plot(steerX, steerMF1, label='Turn Left')
plt.plot(steerX, steerMF2, label='Nothing')
plt.plot(steerX, steerMF3, label='Turn Right')

plt.xlabel('Angle to Target')
plt.ylabel('Membership')
plt.title('shootFIS Steer Output')
plt.axis([-100, 100, 0, 1.1])
plt.legend()

collideX = np.linspace(0, 200, num=1000)
collideMFA1 = MembershipArray(collideMF_values[0])
collideMFA2 = MembershipArray(collideMF_values[1])
collideMFA3 = MembershipArray(collideMF_values[2])

collideMF1 = collideMFA1.lshlder(collideX)
collideMF2 = collideMFA2.triangle(collideX)
collideMF3 = collideMFA3.rshlder(collideX)

plt.figure(5)
plt.plot(collideX, collideMF1, label='Danger Close')
plt.plot(collideX, collideMF2, label='Danger Near')
plt.plot(collideX, collideMF3, label='Danger Far')
plt.xlabel('Distance to Target')
plt.ylabel('Membership')
plt.title('collideFIS Collision Input')
plt.axis([0, 200, 0, 1.1])
plt.legend()

velocityX = np.linspace(0, 10, num=100)
velocityMFA1 = MembershipArray(interceptMF_values[0])
velocityMFA2 = MembershipArray(interceptMF_values[1])

velocityMF1 = velocityMFA1.lshlder(velocityX)
velocityMF2 = velocityMFA2.rshlder(velocityX)

plt.figure(6)
plt.plot(velocityX, velocityMF1, label='Negative')
plt.plot(velocityX, velocityMF2, label='Positive')
plt.xlabel('Change in Relative Position')
plt.ylabel('Membership')
plt.title('collideFIS Position Input')
plt.axis([0, 10, 0, 1.1])
plt.legend()

threatX = np.linspace(0, 3, num=100)
threatMFA1 = MembershipArray(threatMF_values[0])
threatMFA2 = MembershipArray(threatMF_values[1])
threatMFA3 = MembershipArray(threatMF_values[2])

threatMF1 = threatMFA1.triangle(threatX)
threatMF2 = threatMFA2.triangle(threatX)
threatMF3 = threatMFA3.triangle(threatX)

plt.figure(7)
plt.plot(threatX, threatMF1, label='Targeting')
plt.plot(threatX, threatMF2, label='Defensive Targeting')
plt.plot(threatX, threatMF3, label='Avoidance')
plt.xlabel('Threat Level')
plt.ylabel('Membership')
plt.title('collideFIS Threat Output')
plt.axis([0, 3, 0, 1.1])
plt.legend()

avoidX = aimX
avoidMFA1 = MembershipArray(avoidMF_values[0])
avoidMFA2 = MembershipArray(avoidMF_values[1])
avoidMFA3 = MembershipArray(avoidMF_values[2])
avoidMFA4 = MembershipArray(avoidMF_values[3])
avoidMFA5 = MembershipArray(avoidMF_values[4])
avoidMFA6 = MembershipArray(avoidMF_values[5])

avoidMF1 = avoidMFA1.lshlder(avoidX)
avoidMF2 = avoidMFA2.triangle(avoidX)
avoidMF3 = avoidMFA3.triangle(avoidX)
avoidMF4 = avoidMFA4.triangle(avoidX)
avoidMF5 = avoidMFA5.triangle(avoidX)
avoidMF6 = avoidMFA6.rshlder(avoidX)

plt.figure(8)
plt.plot(avoidX, avoidMF1, label='Neg. Large')
plt.plot(avoidX, avoidMF2, label='Neg. Medium')
plt.plot(avoidX, avoidMF3, label='Neg. Small')
plt.plot(avoidX, avoidMF4, label='Pos. Small')
plt.plot(avoidX, avoidMF5, label='Pos. Medium')
plt.plot(avoidX, avoidMF6, label='Pos. Large')
plt.xlabel('Angle of Attack')
plt.ylabel('Membership')
plt.title('avoidFIS Threat Input')
plt.axis([-180, 180, 0, 1.1])
plt.legend()

veerX = np.linspace(-100, 100, num=1000)
veerMFA1 = MembershipArray(sorted(veerMF_values[0]))
veerMFA2 = MembershipArray(sorted(veerMF_values[1]))
veerMFA3 = MembershipArray(sorted(veerMF_values[2]))
veerMFA4 = MembershipArray(sorted(veerMF_values[3]))

veerMF1 = veerMFA1.triangle(veerX)
veerMF2 = veerMFA2.triangle(veerX)
veerMF3 = veerMFA3.triangle(veerX)
veerMF4 = veerMFA4.triangle(veerX)

plt.figure(9)
plt.plot(veerX, veerMF4, label='Neg. Large')
plt.plot(veerX, veerMF3, label='Neg. Small')
plt.plot(veerX, veerMF2, label='Pos. Small')
plt.plot(veerX, veerMF1, label='Pos. Large')
plt.xlabel('Turn Rate')
plt.ylabel('Membership')
plt.title('avoidFIS Turn Rate Output')
plt.axis([-100, 100, 0, 1.1])
plt.legend()

thrustX = np.linspace(-200, 200, num=1000)
thrustMFA1 = MembershipArray(thrustMF_values[0])
thrustMFA2 = MembershipArray(thrustMF_values[1])

thrustMF1 = thrustMFA1.triangle(thrustX)
thrustMF2 = thrustMFA2.triangle(thrustX)

plt.figure(10)
plt.plot(thrustX, thrustMF1, label='Negative')
plt.plot(thrustX, thrustMF2, label='Positive')
plt.title('avoidFIS Thrust Output')
plt.xlabel('Thrust')
plt.ylabel('Membership')
plt.legend()
plt.axis([-200, 200, 0, 1.1])
plt.show()