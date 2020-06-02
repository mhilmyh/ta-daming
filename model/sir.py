from scipy.integrate import odeint
from model.base import Base
import matplotlib.pyplot as plt
import constant
import numpy as np
import os


class SIR(Base):
    """
    Kelas yang merepresentasikan model:
    -   Susceptible
        Jumlah dari populasi yang belum
        terinfeksi

    -   Infected
        Jumlah dari populasi yang sudah
        terinfeksi

    -   Recovered / Removed
        Jumlah dari populasi yang sudah
        sembuh dari infeksi

    SIR disease formula :
    -   dS = -b * S * I / N
        Penurunan jumlah yang dialami oleh
        Susceptible pada satuan waktu

    -   dI = b * S * I / N - g * I
        Kenaikan jumlah Infected pada satuan
        dengan mengurangi jumlah yang Removed

    -   dR = g * I
        Kenaikan jumlah Removed pada tiap
        satuan waktu

    """

    S0 = 0      # susceptible awal
    S = []      # susceptible list
    I0 = 0      # infected awal
    I = []      # infected list
    R0 = 0      # removed awal
    R = []      # removed list
    b = None    # beta (contact rate)
    g = None    # gamma (mean recovery rate)
    t = None    # waktu pandemi berlangsung
    N = 0       # total populasi

    def __init__(
        self,
        S0=constant.S0,
        I0=constant.I0,
        R0=constant.R0,
        b=constant.BETA,
        g=constant.GAMMA,
        t=constant.TIME
    ):
        # Nilai awal populasi
        self.S0 = S0
        self.I0 = I0
        self.R0 = R0
        self.N = S0 + I0 + R0

        # Set nilai rate
        self.b = b
        self.g = g

        # Set nilai waktu
        self.t = np.linspace(0, t, t)

    def __call__(self, S0=None, I0=None, R0=None, b=None, g=None, t=None, **kwargs):
        self.S0 = self.S0 if S0 is None else S0
        self.I0 = self.I0 if I0 is None else I0
        self.R0 = self.R0 if R0 is None else R0

        self.b = self.b if b is None else b
        self.g = self.g if g is None else g

        self.t = np.linspace(0, t, t) if t is not None else self.t

        return self.S, self.I, self.R

    def initial(self):
        return (self.S0, self.I0, self.R0)

    def deriv(self, y, *args):
        S, I, *_ = y
        dS = (-1) * self.b * S * I / self.N
        dI = self.b * S * I / self.N - self.g * I
        dR = self.g * I
        return dS, dI, dR

    def integrate(self):
        result = odeint(
            self.deriv, self.initial(), self.t
        )
        self.S, self.I, self.R = result.T
        return result.T

    def plot(self):
        fig = plt.figure('SIR Model', facecolor='w')
        fig.suptitle('SIR Model', fontsize=12)
        ax = fig.add_subplot(111, facecolor='#eeeeee', axisbelow=True)
        ax.plot(self.t, self.S / self.N, 'b',
                alpha=0.5, lw=2, label='Susceptible')
        ax.plot(self.t, self.I / self.N, 'r',
                alpha=0.5, lw=2, label='Infected')
        ax.plot(self.t, self.R / self.N, 'g', alpha=0.5, lw=2, label='Removed')
        ax.set_xlabel('Time /days')
        ax.set_ylabel('Number (' + str(self.N) + ')')
        ax.set_ylim(0, 1.2)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)

        """
        Buat folder asset untuk menaruh file file gambar
        dari model
        """
        if not os.path.exists('assets/'):
            os.mkdir('assets/')

        fig.savefig('assets/model-sir.png', dpi=300)
        plt.show()

    def debug(self):
        print("_"*48, end="\n\n")
        print("\t\t{}".format("SIR MODEL"))
        print("_"*48)
        print("\nS0: {} orang\nI0: {} orang\nR0: {} orang\n".format(
            self.S0, self.I0, self.R0
        ))
        print("S: {}, ...\nI: {}, ...\nR: {}, ...\n".format(
            ", ".join(str(element) for element in self.S[:3]),
            ", ".join(str(element) for element in self.I[:3]),
            ", ".join(str(element) for element in self.R[:3]),
        ))
        print("beta: {}\ngamma: {}\ntime: {}\npopulation: {}\n".format(
            self.b, self.g, self.t.size, self.N
        ))
