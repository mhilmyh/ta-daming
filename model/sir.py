"""
SIR disease model :
    -   dS = -b*S*I
        Penurunan jumlag yang dialami oleh 
        Susceptible pada satuan waktu

    -   dI = b*S*I - g*I
        Kenaikan jumlah Infected pada satuan 
        dengan mengurangi jumlah yang Removed
        
    -   dR = g*I
        Kenaikan jumlah Removed pada tiap 
        satuan waktu
"""


class SIR:
    S0 = 0      # Susceptible
    I0 = 0      # Infected
    R0 = 0      # Removed
    b = None    # fungsi beta
    g = None    # fungsi gamma

    def __init__(self, S0, I0, R0, b, g):
        self.S0 = S0
        self.I0 = I0
        self.R0 = R0
        self.b = b
        self.g = g

    def __call__(self, S0, I0, R0):
        self.S0 = self.S0 if S0 is None else S0
        self.I0 = self.I0 if I0 is None else I0
        self.R0 = self.R0 if R0 is None else R0

    def initial(self):
        return (self.S0, self.I0, self.R0)

    def beta(self, function=None):
        if function is None:
            return self.b
        else:
            self.b = function
            return True

    def gamma(self, function=None):
        if function is None:
            return self.g
        else:
            self.g = function
            return True
