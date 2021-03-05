from FISstructure import FIS
from fuzzy import Membership, Rulebase, Defuzz, MembershipArray

import numpy as np
import matplotlib.pyplot as plt

in1 = 0.3
in2 = 0.7

mf1 = [(0, 0.1, 0.4167), (0.0833, 0.5, 0.9167), (0.625, 0.9583, 1)]
mf2 = [(0, 0.1, 0.4167), (0.0833, 0.5, 0.9167), (0.625, 0.9583, 1)]
out = [(0, 0.1, 0.4167), (0.0833, 0.5, 0.9167), (0.5833, 0.95, 1)]

membership = [mf1, mf2, out]
rules = [0, 2, 2, 1, 1, 2, 0, 1, 2]

fuzzy_sys = FIS(membership, rules)
output1 = fuzzy_sys.compute(in1, in2)
print(output1)
print('-------------------------')

