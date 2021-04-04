from typing import Tuple, Dict, Any
from fuzzy import Membership, Rulebase, Defuzz


class FIS:
    def __init__(self, membership, rulebase):

        in1MF_values = membership[0]
        in2MF_values = membership[1]
        outMF_values = membership[2]

        in1MF = []
        in2MF = []

        for mf1 in in1MF_values:
            in1MF_temp = Membership(mf1)
            in1MF.append(in1MF_temp)

        for mf2 in in2MF_values:
            in2MF_temp = Membership(mf2)
            in2MF.append(in2MF_temp)

        self.mf1 = in1MF
        self.mf2 = in2MF
        self.out = outMF_values
        self.rules = rulebase
        self.rulebase = Rulebase()

    def compute(self, in1, in2):

        rules = self.rules
        Fr = self.rulebase
        in1MF = self.mf1
        in2MF = self.mf2
        outMF = self.out

        input1 = []
        input2 = []

        for idx, mf in enumerate(in1MF):
            if len(in1MF) <= 2:
                if idx == 0:
                    input1.append(mf.lshlder(in1))
                else:
                    input1.append(mf.rshlder(in1))
            else:
                if idx == 0:
                    input1.append(mf.lshlder(in1))
                elif idx == len(in1MF):
                    input1.append(mf.rshlder(in1))
                else:
                    input1.append(mf.triangle(in1))

        for idx, mf in enumerate(in2MF):
            if len(in2MF) <= 2:
                if idx == 0:
                    input2.append(mf.lshlder(in2))
                else:
                    input2.append(mf.rshlder(in2))
            else:
                if idx == 0:
                    input2.append(mf.lshlder(in2))
                elif idx == len(in2MF):
                    input2.append(mf.rshlder(in2))
                else:
                    input2.append(mf.triangle(in2))

        rule_combos = []
        for r1 in input1:
            for r2 in input2:
                rule_temp = Fr.AND_rule([r1, r2])
                rule_combos.append(rule_temp)

        out_array = [[] for i in range(len(outMF))]

        for rule, combo in zip(rules, rule_combos):
            out_array[rule].append(combo)

        out_array = [out for out in out_array if out != []]

        mu_array = list(map(Fr.OR_rule, out_array))

        out = Defuzz(mu_array, outMF)

        output = out.defuzz_out()
        return output


class SingleFIS:
    def __init__(self, membership, rulebase):

        inMF_values = membership[0]
        outMF_values = membership[1]

        in1MF = []
        in2MF = []

        for mf1 in inMF_values:
            in1MF_temp = Membership(mf1)
            in1MF.append(in1MF_temp)

        self.mf1 = in1MF
        self.out = outMF_values
        self.rules = rulebase
        self.rulebase = Rulebase()

    def compute(self, in1):

        rules = self.rules
        in1MF = self.mf1
        outMF = self.out
        Fr = self.rulebase

        input1 = []

        for idx, mf in enumerate(in1MF):
            if len(in1MF) <= 2:
                if idx == 0:
                    input1.append(mf.lshlder(in1))
                else:
                    input1.append(mf.rshlder(in1))
            else:
                if idx == 0:
                    input1.append(mf.lshlder(in1))
                elif idx == len(in1MF):
                    input1.append(mf.rshlder(in1))
                else:
                    input1.append(mf.triangle(in1))

        full_out_array = [[], [], [], [], [], [], []]

        for rule, combo in zip(rules, input1):
            full_out_array[rule].append(combo)

        out_array = [out for out in full_out_array if out != []]

        mu_array = list(map(Fr.OR_rule, out_array))
        out = Defuzz(mu_array, outMF)

        output = out.defuzz_out()
        return output