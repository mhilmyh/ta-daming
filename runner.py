from model.sir import SIR
from model.seird import SEIRD
import numpy as np
import constant
import pandas as pd


def accuracy(datamodel, datareal):
    raise NotImplementedError


def simulation(
    which='sir',
    b=None,
    g=None,
    d=None,
    a=None,
    r=None,
    R=None,
    days=None
):
    """
    Parameter:
        - which = > model mana yang digunakan
        - b = > fungsi atau nilai konstan beta
        - g = > fungsi atau nilai konstan gamma
        - d = > fungsi atau nilai konstan delta
        - a = > fungsi atau nilai konstan alpha
        - r = > fungsi atau nilai konstan rho
        - R = > fungsi atau nilai konstan Ro
    """

    """
    Asumsi waktu pandemi yang berlangsung
    yaitu 160 hari
    """
    days = days if days is not None else constant.TIME

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
            R0=constant.R0,
            b=constant.BETA if b is None else b,
            g=constant.GAMMA if g is None else g,
            t=constant.TIME
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
            S0=constant.S0,
            E0=constant.E0,
            I0=constant.I0,
            R0=constant.R0,
            D0=constant.D0,
            infectionTime=constant.INFECTION_TIME,
            incubationTime=constant.INCUBATION_TIME,
            timeBeforeDeath=constant.TIME_BEFORE_DEATH,
            time=days,
            timestep=constant.TIMESTEP,
            funcRo=R if R is not None else lambda x: constant.RO,
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
    sir = simulation('sir')
    seird = simulation('seird')

    """
    Jadikan model sebagai dataframe
    dengan nama :
        1.  `data_sir` untuk SIR model
        2.  `data_seird` untuk SEIRD model
    """
    data_sir = pd.DataFrame(
        data={
            'Susceptible': sir.S,
            'Infected': sir.I,
            'Removed': sir.R,
        }
    )
    data_seird = pd.DataFrame(
        data={
            'Susceptible': seird.S,
            'Exposed': seird.E,
            'Infected': seird.I,
            'Recovered': seird.R,
            'Death': seird.D,
        }
    )

    """
    Impor dataframe yang sudah disimpan
    pada folder ./dataset/dataframe/
    """
    data_real_sir = pd.read_csv('./dataset/dataframe/sir.csv')
    data_real_seird = pd.read_csv('./dataset/dataframe/seird.csv')

    """
    Hitung akurasi model dengan data asli
    yang diambil dari folder dataset/
    """
    result_sir = accuracy(data_sir, data_real_sir)
    result_seird = accuracy(data_seird, data_real_seird)
