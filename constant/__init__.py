"""
Total populasi yang ada di suatu wilayah 
atau negara yang ingin dijadikan sebagai 
contoh model. Misal, populasi di italy 
sebanyak 60.36 juta orang
"""
TOTAL_POPULATION = 60_360_000

"""
Nilai probabilitas seseorang akan 
sembuh atau meinggal. Dapat juga berbentuk 
sebaran umur. Misal: 
Umur 1-14 tahun : kemungkinan meninggal 0.2%
Umur 15-64 tahun : kemungkinan meninggal 3.6%
Umur 65+ tahun : kemungkinan meninggal 25.8%
"""
ALPHA = 0.3

"""
Nilai probabilitas seseorang akan 
menjadi terinfeksi (model SIR) atau menjadi 
terexposed (model SEIRD)
"""
BETA = 0.6

"""
Nilai probabilitas seseorang akan 
menjadi recovered (model SIR & SEIRD)
"""
GAMMA = 0.1

"""
Nilai probabilitas seseorang akan 
menjadi infected dari yang tadinya
exposed (hanya model SEIRD)
"""
DELTA = 0.1

"""
Nilai probabilitas seseorang akan 
meninggal/death dari yang tadinya
infected (model SEIRD)
"""
RHO = 0.1

"""
Nilai banyaknya jumlah orang yang 
akan terexposed ketika berkontakan
dengan orang yang terinfeksi 
(model SEIRD)
"""
RO = 3.0

"""
Jumlah orang meninggal (death) 
pada saat pencatatan awal
"""
D0 = 7

"""
Jumlah orang sembuh (recovered) 
pada saat pencatatan awal
"""
R0 = 1

"""
Jumlah orang terinfeksi(infected) 
pada saat pencatatan awal
"""
I0 = 127

"""
Jumlah orang terkena kontak dengan 
orang yg terinfeksi (exposed) pada 
saat pencatatan awal
"""
E0 = 94

"""
Jumlah orang yang masih berpotensi 
untuk terkena (orang yang masih 
sehat)
"""
S0 = TOTAL_POPULATION - E0 - I0 - R0 - D0

"""
Waktu seseorang mengalami sakit (terinfeksi).
Setelah itu ia akan ditentukan apakah sembuh 
atau meninggal (pada model SIR, meninggal dan 
sembuh dianggap sama)
"""
INFECTION_TIME = 14

"""
Waktu setelah orang tersebut kontak dengan 
orang yang terinfeksi dan mulai mengalami 
gejala. Rata-rata waktunya adalah 1-3 
minggu. Misal, asumsi yang digunakan adalah 1 
minggu yaitu 7 hari
"""
INCUBATION_TIME = 7

"""
Waktu dimulai nya lockdown pada hari ke-x. 
Nilai ini bisa digunakan untuk mengubah 
fungsi Ro (berapa banyak orang yang bisa 
diinfeksi oleh orang yang terinfeksi) 
"""
START_LOCKDOWN = 1

"""
Dari rata-rata, biasanya orang yang memiliki
kemungkinan meninggal tinggi mengalami 
penyakit antara 3-6 minggu. Misal, asumsi yg digunakan 
adalah 3 minggu (21 hari)
"""
TIME_BEFORE_DEATH = 21

"""
Nilai waktu lama pandemi berlangsung. Nilai ini
harus memiliki lama yg sama dengan banyaknya baris 
pada dataframe jika ingin melakukan plot pada 
file `runner.py`
"""
TIME = 95

"""
Banyaknya pengambilan data pada waktu pandemi. 
Asumsi yang digunakan yaitu pengambilan data sesuai 
dengan lama nya waktu pandemi. Misal, waktu pandemi 
150 hari dan ada 150 kali pengambilan data berarti 
setiap hari diambil satu data. Dan nilai TIMESTEP 
sama dengan nilai TIME.
"""
TIMESTEP = TIME
