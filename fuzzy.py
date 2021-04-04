import numpy as np


class Membership:
    def __init__(self, values):
        self.values = values
        self.le = None
        self.ce = None
        self.re = None
        self.mu = None

    def triangle(self, x):
        values = self.values

        le = values[0]
        ce = values[1]
        re = values[2]

        if le <= x < ce:
            mu = (x - le)/(ce - le)
        elif ce <= x <= re:
            mu = (re - x)/(re - ce)
        else:
            mu = 0
        return mu

    def rshlder(self, x):
        values = self.values
        le = values[0]
        ce = values[1]
        re = values[2]

        if le <= x < ce:
            mu = (x - le)/(ce - le)
        elif ce <= x <= re:
            mu = 1
        else:
            mu = 0
        return mu

    def lshlder(self, x):
        values = self.values
        le = values[0]
        ce = values[1]
        re = values[2]

        if le <= x < ce:
            mu = 1
        elif ce <= x <= re:
            mu = (re - x)/(re - ce)
        else:
            mu = 0
        return mu


class MembershipArray:
    def __init__(self, values):
        self.values = values
        self.le = None
        self.ce = None
        self.re = None
        self.mu = None

    def triangle(self, x):
        values = self.values
        xArray = x
        le = values[0]
        ce = values[1]
        re = values[2]
        muArray = []

        for i in range(len(xArray)):
            x = xArray[i]
            if le <= x < ce:
                mu = (x - le)/(ce - le)
            elif ce <= x <= re:
                mu = (re - x)/(re - ce)
            else:
                mu = 0
            muArray.append(mu)
        return muArray

    def rshlder(self, x):
        xArray = x
        values = self.values
        le = values[0]
        ce = values[1]
        re = values[2]
        muArray = []

        for i in range(len(xArray)):
            x = xArray[i]
            if le <= x < ce:
                mu = (x - le)/(ce - le)
            elif ce <= x <= re:
                mu = 1
            else:
                mu = 0
            muArray.append(mu)
        return muArray

    def lshlder(self, x):
        xArray = x
        values = self.values
        le = values[0]
        ce = values[1]
        re = values[2]
        muArray = []

        for i in range(len(xArray)):
            x = xArray[i]
            if le <= x < ce:
                mu = 1
            elif ce <= x <= re:
                mu = (re - x)/(re - ce)
            else:
                mu = 0
            muArray.append(mu)
        return muArray


class Rulebase:
    def __init__(self):
        self.output = None

    def AND_rule(self, input):
        self.output = np.amin(input)
        return self.output

    def OR_rule(self, input):
        self.output = np.amax(input)
        return self.output


class Defuzz:
    def __init__(self, mu, output):
        self.mu = mu
        self.output = output
        self.max = None

    def defuzz_out(self):
        output = self.output
        outMFarrays = []
        maxInd = max(max(output))
        minInd = min(min(output))
        Xvals = np.linspace(minInd, maxInd, num=100)
        mfArray = []

        for mf in output:
            mfArray.append(MembershipArray(mf))

        for i in range(len(self.mu)):
            # self.output should be list of tuples
            # (le, ce, re)
            MF = mfArray[i]
            outArrayVals = np.array(MF.triangle(Xvals))
            outArrayVals[outArrayVals >= self.mu[i]] = self.mu[i]
            outMFarrays.append(outArrayVals)
        outStacked = np.vstack(outMFarrays)
        maxOuts = np.max(outStacked, axis=0)

        self.max = maxOuts
        total_area = np.sum(maxOuts)

        if total_area == 0:
            crisp_out = 0
        else:
            crisp_out = np.divide(np.sum(np.multiply(maxOuts, Xvals)),total_area)

        return crisp_out


