import os
import pandas as pd

if __name__ == "__main__":
    """
    Gunakan dataset terakhir yang merupakan hasil gabungan
    dari seluruh data yang ada.

    Keterangan data :
    data	                    notification date
    stato	                    country 3-letter code
    ricoverati_con_sintomi	    hospitalized patients with symptoms
    terapia_intensiva	        hospitalized patients in intensive care
    totale_ospedalizzati	    total hospitalized patients (hospitalized patients with symptoms + hospitalized patients in intensive care)
    isolamento_domiciliare	    home-confinement patients
    totale_attualmente_positivi	total amount of currently positive cases (total hospitalized patients + home-confinement patients)
    nuovi_attualmente_positivi	total amount of new positive cases (total amount of currently positive cases - total amount of positive cases of the previous day)
    dimessi_guariti	            recovered cases
    deceduti	                death
    totale_casi	                total amount of positive cases (total amount of currently positive cases + recovered cases + death)
    tamponi	                    tests performed
    casi testato	            cases tested
    """
    filename = "dpc-covid19-ita-andamento-nazionale.csv"
    dataframe = pd.read_csv("dataset/" + filename)

    """
    Ganti nilai NaN menjadi 0. Kita menganggap data ini sebagai kosong.
    Serta drop kolom yang tidak terpakai.
    """
    dataframe = dataframe.drop(columns=['note_it', 'note_en'])
    dataframe = dataframe.fillna(0)
    print(dataframe)

    """
    Untuk model SIR, kita akan menggunakan kolom berikut :
        -   Susceptible
            (populasi yang belum terinfeksi)
        -   Infected
            (populasi yang terinfeksi)
        -   Removed
            (populasi sembuh dan meninggal)
    """
