import os
import pandas as pd
import constant

if __name__ == "__main__":
    """
    Gunakan dataset terakhir yang merupakan hasil gabungan
    dari seluruh data yang ada.

    Keterangan data (* apabila sudah ditotal di kolom lain):
    data	                    notification date
    stato	                    country 3-letter code
    ricoverati_con_sintomi*	    hospitalized patients with symptoms
    terapia_intensiva*	        hospitalized patients in intensive care
    totale_ospedalizzati*	    total hospitalized patients (hospitalized patients with symptoms + hospitalized patients in intensive care)
    isolamento_domiciliare*	    home-confinement patients
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
    Cleaning data :
    1. Drop kolom yang tidak terpakai. 
    2. Ganti nilai NaN menjadi 0. (anggap NaN sebagai kosong)
    3. Rename nama kolom sesuai dengan data nya.
    4. Serta hitung sisa populasi yg belum terinfeksi
    dengan asumsi bahwa total populasi itali adalah 60.36 juta
    """
    dataframe = dataframe.drop(
        columns=[
            'stato',
            'note_it',
            'note_en',
            'ricoverati_con_sintomi',
            'variazione_totale_positivi',
            'nuovi_positivi',
            'terapia_intensiva',
            'totale_ospedalizzati',
            'isolamento_domiciliare',
            'casi_testati',
            'tamponi'
        ]
    )
    dataframe = dataframe.fillna(0)
    dataframe = dataframe.rename(
        columns={
            "data": "date",
            "totale_positivi": "infected",
            "dimessi_guariti": "recovered",
            "deceduti": "death",
            "totale_casi": "susceptible"
        }
    )
    dataframe['date'] = dataframe['date'].apply(
        lambda x: x.split(":")[0].split("T")[0]
    )
    population = constant.TOTAL_POPULATION
    dataframe['susceptible'] = dataframe['susceptible'].apply(
        lambda x: population - x
    )

    """
    Untuk model SIR, kita akan menggunakan kolom berikut :
        -   Susceptible
            [Total Population - 'totale_casi' => susceptible]
            (populasi yang belum terinfeksi)
        -   Infected
            [totale_attualmente_positivi => infected]
            (populasi yang terinfeksi)
        -   Removed
            [dimessi_guariti => recovered, deceduti => death]
            (populasi sembuh dan meninggal)
    """
    dataframe['removed'] = dataframe['recovered'] + dataframe['death']
    dataframe = dataframe.drop(
        columns=[
            'recovered',
            'death'
        ]
    )

    """
    Simpan dataframe ke dalam file csv agar bisa
    diproses untuk langkah selanjutnya
    """
    dataframe.to_csv('dataset/dataframe.csv')
    print(dataframe)
