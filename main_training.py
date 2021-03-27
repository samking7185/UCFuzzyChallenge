from CGA import CGA

# %%
# ---------------------------------------------------- #
# ---------------- Genetic Algorithm ------------------#
# M must be even number
M = 50
MaxGen = 50
Pc = 0.9
Pm = 0.4
Er = 0.2

n = [3, 3, 7]
UB = [-0.01, 1,  1000]
LB = [-1, 0.01, 1]

var = ['float', 'float', 'int']

# Available settings
settings = {
    "graphics_on": True,
    # "sound_on": False,
    # "frequency": 60,
    "real_time_multiplier": 100,
    "lives": 1,
    "prints": False,
    # "allow_key_presses": False
}

gaTest = CGA(M, MaxGen, Pc, Pm, Er, n, UB, LB, var, settings)

print('\n')
print('--------------------- Best Chromosome ------------------------')
print(gaTest.BestChrom)
print('\n')
print('------------------------- Fitness ----------------------------')
print(gaTest.Fitness)

