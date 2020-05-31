from model.sir import SIR
import constant as c
import numpy as np


def simulation(which='sir'):
    """
    Asumsi waktu pandemi yang berlangsung
    yaitu 160 hari
    """
    days = np.linspace(0, 160, 160)

    """
    Pilih model yang akan digunakan
    """
    which = which.lower()

    if which == 'sir':

        """
        Model SIR dibuat dengan memberikan
        parameter yang dibutuhkan
        """
        sir = SIR(S0=c.S0, I0=c.I0, b=c.BETA, g=c.GAMMA, t=days)

        """
        Lakukan perhitungan integral
        untuk memperoleh kurva
        """
        sir.integrate()

        """
        Gambarkan pada plot, kurva :
        -   Susceptible
        -   Infected
        -   Removed/Recovered
        """
        sir.plot()

        return sir

    elif which == 'seird':

        print('Belum selesai')
        return None

    else:
        raise NotImplementedError


if __name__ == '__main__':
    """
    Jalankan Simulasi Model yang dipilih
    dan ambil model simulasi nya
    """
    model = simulation('seird')

    """
    Hitung akurasi model dengan data asli
    yang diambil dari folder dataset/
    """
