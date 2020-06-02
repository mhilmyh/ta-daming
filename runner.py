from model.sir import SIR
from model.seird import SEIRD
import numpy as np
import constant
import pandas as pd
import matplotlib.pyplot as plt
import os


def MSE(which='sir', datamodel=None, datareal=None):
    """
    Kegunaan :
        Berfungsi untuk menjalankan perhitungan
        Mean Square Error suatu model terhadap
        data aslinya. Menggunakan MSE karena trend
        yang dimiliki data berbentuk seperti
        polinomial regresi.
    Parameter:
        - datamodel = > data dari model
        - datareal = > data asli dari hasil scrapping
    """

    # Hitung Mean Square Error
    for column in datareal:
        # lewati jika kolom date
        if column == 'date':
            continue

        diff = datamodel[column] - datareal[column]
        square = diff ** 2
        mse = square.sum() / len(datareal[column])
        print("{}[{}]: {}".format(which.upper(), column.lower(), mse))

    print()


def simulation(
    which='sir',
    b=None,
    g=None,
    d=None,
    a=None,
    r=None,
    R=None,
    days=None,
    probabilityAge=None,
    proportionAge=None,
):
    """
    Kegunaan :
        Berfungsi untuk menjalankan simulasi suatu
        model dan mengembalikan object class model
    Parameter:
        - which = > model mana yang digunakan
        - b = > fungsi atau nilai konstan beta
        - g = > fungsi atau nilai konstan gamma
        - d = > fungsi atau nilai konstan delta
        - a = > fungsi atau nilai konstan alpha
        - r = > fungsi atau nilai konstan rho
        - R = > fungsi atau nilai konstan Ro
        - days = > lama durasi pandemi (satuan hari)
        - probabilityAge = > nilai kemungkinan hidup
        - proportionAge = > nilai persentase umur suatu wilayah
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
            I0=constant.I0 + constant.E0,
            R0=constant.R0 + constant.D0,
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
            probabilityAge=probabilityAge if probabilityAge is not None else None,
            proportionAge=proportionAge if proportionAge is not None else None,
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
    Definisikan probabilitas suatu
    umur dapat meninggal karena
    pandemi (nilai alpha).
    """
    probAge = {
        "0-14": 0.2/100,
        "15-64": 3.6/100,
        "65+": 25.8/100,
    }

    """
    Definisikan proporsi suatu
    umur di suatu negara jika di
    jumlahkan harus bernilai satu
    """
    propAge = {
        "0-14": 13.33/100,
        "15-64": 63.92/100,
        "65+": 22.75/100
    }

    """
    Definisikan fungsi persebaran
    pandemi
    """
    def R(t):
        return 4.5 / (1 + np.exp(-0.5*(-t+50))) + 0.5
    """
    Jalankan Simulasi Model yang dipilih
    dan ambil model simulasi nya
    """
    sir = simulation(
        which='sir'
    )
    sir.debug()

    seird = simulation(
        which='seird',
        probabilityAge=probAge,
        proportionAge=propAge
    )
    seird.debug()

    """
    Jadikan model sebagai dataframe
    dengan nama :
        1.  `data_sir` untuk SIR model
        2.  `data_seird` untuk SEIRD model
    """
    data_sir = pd.DataFrame(
        data={
            'susceptible': sir.S,
            'infected': sir.I,
            'removed': sir.R,
        }
    )
    data_seird = pd.DataFrame(
        data={
            'susceptible': seird.S,
            'exposed': seird.E,
            'infected': seird.I,
            'recovered': seird.R,
            'death': seird.D,
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
    MSE(which='sir', datamodel=data_sir, datareal=data_real_sir)
    MSE(which='seird', datamodel=data_seird, datareal=data_real_seird)

    """
    Plot data asli ke dalam kurva untuk
    melihat perbandingan trend antara model
    dengan data asli.
    """
    fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True)

    # Kurva SIR
    ax[0].plot(np.linspace(0, constant.TIME, constant.TIMESTEP), data_real_sir['susceptible'] /
               constant.TOTAL_POPULATION, 'b', alpha=0.5, lw=2, label='Susceptible')
    ax[0].plot(np.linspace(0, constant.TIME, constant.TIMESTEP), data_real_sir['infected'] /
               constant.TOTAL_POPULATION, 'r', alpha=0.5, lw=2, label='Infected')
    ax[0].plot(np.linspace(0, constant.TIME, constant.TIMESTEP), data_real_sir['removed'] /
               constant.TOTAL_POPULATION, 'g', alpha=0.5, lw=2, label='Removed')

    # Kurva SEIRD
    ax[1].plot(np.linspace(0, constant.TIME, constant.TIMESTEP), data_real_seird['susceptible'] /
               constant.TOTAL_POPULATION, 'b', alpha=0.5, lw=2, label='Susceptible')
    ax[1].plot(np.linspace(0, constant.TIME, constant.TIMESTEP), data_real_seird['exposed'] /
               constant.TOTAL_POPULATION, 'y', alpha=0.5, lw=2, label='Exposed')
    ax[1].plot(np.linspace(0, constant.TIME, constant.TIMESTEP), data_real_seird['infected'] /
               constant.TOTAL_POPULATION, 'r', alpha=0.5, lw=2, label='Infected')
    ax[1].plot(np.linspace(0, constant.TIME, constant.TIMESTEP), data_real_seird['recovered'] /
               constant.TOTAL_POPULATION, 'g', alpha=0.5, lw=2, label='Recovered')
    ax[1].plot(np.linspace(0, constant.TIME, constant.TIMESTEP), data_real_seird['death'] /
               constant.TOTAL_POPULATION, 'k', alpha=0.5, lw=2, label='Death')

    for i, axis in enumerate(ax.flat):
        axis.set_xlabel('Time / days')
        axis.set_ylabel(
            'Ratio (' + str(constant.TOTAL_POPULATION) + ' orang)')
        axis.set_ylim(0, 1.2)
        axis.yaxis.set_tick_params(length=0)
        axis.xaxis.set_tick_params(length=0)
        axis.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = axis.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            axis.spines[spine].set_visible(False)

    fig.tight_layout()

    """
    Buat folder asset untuk menaruh file file gambar
    dari model
    """
    if not os.path.exists('assets/'):
        os.mkdir('assets/')

    fig.savefig('assets/model-real.png', dpi=300)
    plt.show()
