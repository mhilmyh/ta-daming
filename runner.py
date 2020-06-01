from model.sir import SIR
from model.seird import SEIRD
from numpy import linspace
import constant
import pandas as pd


def simulation(which='sir'):
    """
    Asumsi waktu pandemi yang berlangsung
    yaitu 160 hari
    """
    days = 160

    """
    Pilih model yang akan digunakan
    """
    which = which.lower()

    if which == 'sir':
        """
        Model SIR dibuat dengan memberikan
        parameter yang dibutuhkan. Apabila 
        parameter tidak disertakan maka 
        nilai default pada class yang akan 
        dipakai.
        """
        sir = SIR(
            S0=constant.S0,
            I0=constant.I0,
            R0=0,
            b=constant.BETA,
            g=constant.GAMMA,
            t=linspace(0, days, days)
        )

        """
        Lakukan perhitungan integral
        untuk memperoleh kurva
        """
        sir.integrate()

        """
        Gambarkan pada plot, kurva:
        -   Susceptible
        -   Infected
        -   Removed/Recovered
        """
        sir.plot()

        return sir

    elif which == 'seird':
        """
        Model SEIRD dibuat dengan memberikan
        parameter yang dibutuhkan. Apabila 
        parameter tidak disertakan maka 
        nilai default pada class yang akan 
        dipakai.
        """
        seird = SEIRD(
            S0=None,
            E0=None,
            I0=None,
            R0=None,
            D0=None,
            infectionTime=None,
            incubationTime=None,
            timeBeforeDeath=None,
            time=days,
            timestep=None,
            funcRo=None,
        )

        """
        Lakukan perhitungan integral
        untuk memperoleh kurva
        """
        seird.integrate()

        """
        Gambarkan pada plot, kurva:
        -   Susceptible
        -   Exposed
        -   Infected
        -   Recovered
        -   Death
        """
        seird.plot()

        return seird

    else:
        raise NotImplementedError


if __name__ == '__main__':
    """
    Jalankan Simulasi Model yang dipilih
    dan ambil model simulasi nya
    """
    model = simulation('seird')

    """
    Jadikan model sebagai dataframe 
    dengan nama datamodel
    """

    print(model)

    """
    Impor dataframe yang sudah disimpan
    pada folder ./dataset/dataframe/
    """

    """
    Hitung akurasi model dengan data asli
    yang diambil dari folder dataset/
    """
