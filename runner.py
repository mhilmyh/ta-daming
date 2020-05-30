from model import SIR
import constant as c
import numpy as np

if __name__ == '__main__':
    """
    Asumsi waktu pandemi yang berlangsung
    yaitu 160 hari 
    """
    days = np.linspace(0, 160, 160)

    """
    Model SIR dibuat dengan memberikan
    parameter yang dibutuhkan
    """
    sir = SIR(c.TOTAL_POPULATION, I0=c.I0, b=c.BETA, g=c.GAMMA, t=days)

    """
    Lakukan perhitungan integral
    untuk memperoleh kurva
    """
    sir.integrate()

    """
    Gambarkan pada plot
    """
    sir.plot()
