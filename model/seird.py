from scipy.integrate import odeint
import matplotlib.pyplot as plt


class SEIRD:
    """
    Implementasi yang lebih advance dengan 
    memperhitungkan hal detail dari kejadian pandemi.

    Persamaan yang digunakan adalah sebagai berikut : 
    https://miro.medium.com/max/1400/1*002FJ30Y58ApR33Pk3njLA.png

    Arsitektur model yang digunakan sebagai berikut :
    https://miro.medium.com/max/1400/1*TIZaRpt70TR1RFtf2dmlew.png

    SEIRD model disease :
        -   dS = -beta * S * I / N
            Susceptible adalah orang yang masih sehat
            di dalam populasi dan berkemungkinan
            menjadi exposed

        -   dE = beta * S * I / N - delta * E
            Kenaikan jumlah Exposed pada satuan waktu.
            Exposed merupakan orang yang berkontakan
            dengan infected namun tidak di rawat.
            Asumsi yang digunakan yaitu mereka adalaj

        -   dI = delta * E - (1 - alpha) * gamma * I - alpha * rho * I
            Kenaikan jumlah Infected pada satuan waktu.
            Infected memiliki lama headling rate sebesar
            gamma.

        -   dR = (1 - alpha) * gamma * I
            Jumlah orang yang telah sembut pada hari ke-t.

        -   dD = alpha * rho * I
            Jumlah orang yang telah meninggal pada hari ke-t.
            Probabiliti orang meninggal direpresentasikan oleh
            variabel rho   
    """

    _population = 0
    _infectionTime = 0
    _startLockdown = 0

    _S0 = 0
    _E0 = 0
    _I0 = 0
    _R0 = 0
    _D0 = 0

    # [Constructor] @return void
    def __init__(self):
        raise NotImplementedError

    def beta(self):
        raise NotImplementedError

    def delta(self):
        raise NotImplementedError

    def alpha(self):
        raise NotImplementedError

    def gamma(self):
        raise NotImplementedError

    def rho(self):
        raise NotImplementedError
