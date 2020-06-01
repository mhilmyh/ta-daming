from scipy.integrate import odeint
from numpy import linspace
from model.base import Base
import matplotlib.pyplot as plt
import constant


class SEIRD(Base):
    """
    SEIRD model disease:
        -   dS = -beta * S * I / N
            Susceptible adalah orang yang masih sehat
            di dalam populasi dan berkemungkinan
            menjadi exposed.

        -   dE = beta * S * I / N - delta * E
            Kenaikan jumlah Exposed pada satuan waktu.
            Exposed merupakan orang yang berkontakan
            dengan infected namun tidak di rawat.

        -   dI = delta * E - (1 - alpha) * gamma * I - alpha * rho * I
            Kenaikan jumlah Infected pada satuan waktu.
            Infected memiliki lama headling rate sebesar
            gamma.

        -   dR = (1 - alpha) * gamma * I
            Jumlah orang yang telah sembut pada hari ke-t.

        -   dD = alpha * rho * I
            Jumlah orang yang telah meninggal pada hari ke-t.
            Probabiliti orang meninggal direpresentasikan oleh
            variabel rho.
    """

    """
    -   totalPopulation[int](jumlah masyarakat)

        = > Penjelasan:
        Jumlah penduduk total dalam suatu kawasan
        atau negara.

        = > Asumsi:
        Asumsinya, pada saat penyebaran penyakit
        berlangsung total populasi tidak berubah.
    """
    _totalPopulation = 0

    """
    -   infectionTime[int](hari infeksi)

        = > Penjelasan:
        Durasi infeksi yang terjadi pada saat seseorang
        terkena infeksi sampai sembuh atau meninggal.

        = > Asumsi:
        Infeksi diasumsikan juga konstan. selama beberapa
        hari dan langsung sembuh atau meninggal tanpa ada
        gejala yg muncul untuk kedua kalinya.
    """
    _infectionTime = 0

    """
    -   incubationTime[int](hari infeksi)

        = > Penjelasan:
        Durasi incubasi yang terjadi pada saat seseorang
        terexposed sampai infeksi.

        = > Asumsi:
        Waktu inkubasi konstan pada setiap orang.
    """
    _incubationTime = 0

    """
    -   timeBeforeDeath[int](lama hari sebelum meninggal)

        = > Penjelasan:
        Durasi dari mulai terinfeksi sampai meninggal.

        = > Asumsi:
        Infeksi diasumsikan juga konstan. selama beberapa
        hari dan langsung sembuh atau meninggal tanpa ada
        gejala yg muncul untuk kedua kalinya.
    """
    _timeBeforeDeath = 0

    """
    -   S0[int](jumlah orang sehat)

        = > Penjelasan:
        Jumlah penduduk awal yang belum terinfeksi
        dalam artian masih sehat.

        = > Asumsi:
        Nilai awal ini hanya berlaku pada hari
        pertama pandemi dimulai.
    """
    _S0 = 0

    """
    -   E0[int](jumlah orang dalam pantauan)

        = > Penjelasan:
        Jumlah penduduk yang berkontakan dengan
        orang yang terinfeksi.

        = > Asumsi:
        Setiap orang yang berkontakan dengan orang
        yang terinfeksi 100 % menjadi exposed dalam
        beberapa hari(sudah ditentukan lama nya).
    """
    _E0 = 0

    """
    -   I0[int](jumlah pasien dalam pantauan)

        = > Penjelasan:
        Jumlah penduduk yang terkena infeksi.

        = > Asumsi:
        Asumsinya, pada saat penyebaran penyakit
        berlangsung total populasi tidak berubah.
    """
    _I0 = 0

    """
    -   D0[int](jumlah orang yang meninggal)

        = > Penjelasan:
        Jumlah penduduk yang meninggal dalam
        suatu kawasan setelah terinfeksi. Terdapat
        probabilitas untuk orang meninggal sebesar
        alpha.

        = > Asumsi:
        Penduduk meninggal hanya dihitung setelah
        infeksi. Tidak ada penduduk yg meninggal
        karena penyakit lain.
    """
    _D0 = 0

    """
    -   time[array](lama waktu pandemi)

        = > Penjelasan:
        Lama hari pandemi berlangsung.

        = > Asumsi:
        Waktu pandemi tidak bertambah ataupun
        berkurang.
    """
    _time = []

    """
    -   funcRo[function](fungsi jumlah orang tertular)

        = > Penjelasan:
        Fungsi yang digunakan untuk
        merepresentasikan banyak orang yang
        terinfeksi pada t hari.

        = > Asumsi:
        Kenaikan atau Penurunan jumlah orang
        yang terinfeksi ideal sesuai dengan
        fungsi yang ditentukan.
    """
    _funcRo = None

    """
    -   pAge[dictionary](nilai alpha pada umur tertentu)

        = > Penjelasan:
        digunakan untuk menentukan nilai alpha
        dalam bentuk probabilitas pada sebaran
        umur tertentu.

        = > Asumsi:
        Suatu range umur memiliki satu nilai
        alpha yang constant.
    """
    _pAge = None

    """
    -   propAge[dictionary](nilai persentase umur suatu wilayah)

        = > Penjelasan:
        digunakan untuk menentukan berapa persen 
        jumlah penduduk yang berusia tua, muda, dll
        dalam satuan decimal.

        = > Asumsi:
        hasil penjumlahan range umur bernilai 
        satu atau 100% .
    """
    _propAge = None

    """
    -   valAlpha[float](nilai alpha)

        = > Penjelasan:
        nilai final alpha hasil dari perhitungan 
        antara probabiliti age (pAge) dan 
        proportional age (propAge).

        = > Asumsi:
        nilai alpha tidak lebih dari 1.0, atau
        tidak lebih dari 100% .
    """
    _valAlpha = 0.0

    """
    -   S,E,I,R,D[array](hasil integrasi)

        = > Penjelasan:
        Array hasil integrasi yang akan 
        dijadikan plot dan sebagai model
        dari SEIRD
    """
    S = []
    E = []
    I = []
    R = []
    D = []

    def __init__(
        self,
        S0=None,
        E0=None,
        I0=None,
        R0=None,
        D0=None,
        infectionTime=None,
        incubationTime=None,
        timeBeforeDeath=None,
        time=None,
        timestep=None,
        funcRo=None,
        probabilityAge=None,
        proportionAge=None,
    ):
        """
        +   Fungsi Constructor
            = > Kegunaan :
            untuk set nilai awal dari
            parameter yang dibutuhkan.
        """
        self._S0 = int(S0) if S0 is not None else constant.S0
        self._E0 = int(E0) if E0 is not None else constant.E0
        self._I0 = int(I0) if I0 is not None else constant.I0
        self._R0 = int(R0) if R0 is not None else constant.R0
        self._D0 = int(D0) if D0 is not None else constant.D0

        self._totalPopulation = self._S0 + self._E0 + self._I0 + self._R0 + self._D0

        self._infectionTime = int(
            infectionTime
        ) if infectionTime is not None else constant.INFECTION_TIME

        self._incubationTime = int(
            incubationTime
        ) if incubationTime is not None else constant.INCUBATION_TIME

        self._timeBeforeDeath = int(
            timeBeforeDeath
        ) if timeBeforeDeath is not None else constant.TIME_BEFORE_DEATH

        # menyimpan dictionari age
        self._pAge = probabilityAge
        self._propAge = proportionAge

        # Menyetel nilai waktu pandemi
        time = time if time is not None else constant.TIME
        timestep = time if timestep is None else timestep
        self._time = linspace(0, time, timestep)

        # Mendefinisikan fungsi Ro
        if funcRo is None:
            self._funcRo = lambda x: 1.0
        elif isinstance(funcRo, (float, int)):
            self._funcRo = lambda x: funcRo
        elif callable(funcRo):
            self._funcRo = funcRo
        else:
            raise TypeError('Function Ro is in wrong type')

        # Menghitung Nilai Alpha
        value = 0.0
        if self._pAge is not None and self._propAge is not None:
            for age in self._pAge.keys():
                if age in self._propAge:
                    value += self._propAge.get(age) * self._pAge.get(age)
                else:
                    raise TypeError('Wrong key in age')

            self._valAlpha = value
        else:
            self._valAlpha = constant.ALPHA

    def __call__(self, **kwargs):
        """
        +   Fungsi Call
            = > Kegunaan :
            untuk set nilai jika ingin mengganti 
            nilai awal dari keyword argument yang
            diberikan.
        """
        if kwargs.get('S0') is not None:
            self._S0 = int(kwargs['S0'])

        if kwargs.get('E0') is not None:
            self._E0 = int(kwargs['E0'])

        if kwargs.get('I0') is not None:
            self._I0 = int(kwargs['I0'])

        if kwargs.get('R0') is not None:
            self._R0 = int(kwargs['R0'])

        if kwargs.get('D0') is not None:
            self._D0 = int(kwargs['D0'])

        if kwargs.get('totalPopulation') is not None:
            self._totalPopulation = int(kwargs['totalPopulation'])

        if kwargs.get('infectionTime') is not None:
            self._infectionTime = int(kwargs['infectionTime'])

        if kwargs.get('incubationTime') is not None:
            self._incubationTime = int(kwargs['incubationTime'])

        if kwargs.get('timeBeforeDeath') is not None:
            self._timeBeforeDeath = int(kwargs['timeBeforeDeath'])

        if kwargs.get('time') is not None and kwargs.get('timestep') is not None:
            self._time = linspace(0, kwargs['time'], kwargs['timestep'])

        if kwargs.get('funcRo') is not None:
            if isinstance(kwargs.get('funcRo'), (float, int)):
                self._funcRo = lambda x: kwargs['funcRo']
            elif callable(kwargs.get('funcRo')):
                self._funcRo = kwargs['funcRo']
            else:
                raise TypeError('Function Ro is in wrong type')

        if kwargs.get('probabilityAge') is not None:
            if kwargs.get('proportionalAge') is not None:
                value = 0.0
                if self._pAge is not None and self._propAge is not None:
                    for age in self._pAge.keys():
                        if age in self._propAge:
                            value += self._propAge.get(age) * \
                                self._pAge.get(age)

                    self._valAlpha = value
                else:
                    self._valAlpha = constant.ALPHA

    def initial(self):
        """
        +   Fungsi initial()
            = > Kegunaan :
            untuk mengembalikan nilai 
            parameter awal.
        """
        return (
            self._S0,
            self._E0,
            self._I0,
            self._R0,
            self._D0
        )

    def beta(self, t, *args):
        """
        +   Fungsi beta(t)
            = > Kegunaan :
            persentase dari banyaknya orang 
            yang setiap harinya berkontakan 
            dengan orang yang terinfeksi 
            sehingga dikategorikan exposed.
        """
        return self.Ro(t) * self.gamma()

    def delta(self, *args):
        """
        +   Fungsi delta(t)
            = > Kegunaan :
            persentase inkubasi dari orang
            yang berkategori exposed menjadi 
            terinfeksi.
        """
        return 1.0 / self._incubationTime

    def alpha(self, *args):
        """
        +   Fungsi alpha(t)
            = > Kegunaan :
            persentase kematian yang 
            terjadi setelah seseorang 
            terinfeksi.
        """
        return self._valAlpha

    def gamma(self, *args):
        """
        +   Fungsi gamma(t)
            = > Kegunaan :
            persentase kematian yang 
            terjadi setelah seseorang 
            terinfeksi.
        """
        return 1.0 / self._infectionTime

    def rho(self, *args):
        """
        +   Fungsi rho(t)
            = > Kegunaan :
            persentase lama hari dari
            mulai dari infeksi sampai 
            meninggal.
        """
        return 1.0 / self._timeBeforeDeath

    def Ro(self, t, *args):
        """
        +   Fungsi Ro(t)
            = > Kegunaan :
            jumlah dari banyaknya orang 
            yang terinfeksi oleh satu 
            orang yang infected.
        """
        return self._funcRo(t)

    def deriv(self, y, t):
        """
        +   Fungsi deriv(y,t)
            = > Kegunaan :
            melakukan perhitungan 
            penurunan dari variable 
            S0, E0, I0, R0 dan D0
        """
        S, E, I, *_ = y

        dS = (-1) * self.beta(t) * S * I / self._totalPopulation
        dE = (-1) * dS - self.delta() * E
        dI = self.delta() * E - (1 - self.alpha(t)) * self.gamma() * \
            I - self.alpha(t) * self.rho() * I
        dR = (1 - self.alpha(t)) * self.gamma() * I
        dD = self.alpha(t) * self.rho() * I

        return dS, dE, dI, dR, dD

    def integrate(self):
        """
        +   Fungsi integrate()
            = > Kegunaan :
            melakukan integrasi sehingga 
            dapat terbentuk kurva dari 5 
            komponen
        """
        result = odeint(
            self.deriv, self.initial(), self._time
        )
        self.S, self.E, self.I, self.R, self.D = result.T
        return result.T

    def plot(self):
        """
        +   Fungsi plot()
            = > Kegunaan :
            menampilkan gambar grafik 
            model SEIRD
        """
        fig = plt.figure('SEIRD Model', facecolor='w')
        fig.suptitle('SEIRD Model', fontsize=12)
        ax = fig.add_subplot(111, facecolor='#eeeeee', axisbelow=True)
        ax.plot(self._time, self.S / self._totalPopulation, 'b',
                alpha=0.5, lw=2, label='Susceptible')
        ax.plot(self._time, self.E / self._totalPopulation, 'y',
                alpha=0.5, lw=2, label='Exposed')
        ax.plot(self._time, self.I / self._totalPopulation, 'r',
                alpha=0.5, lw=2, label='Infected')
        ax.plot(self._time, self.R / self._totalPopulation, 'g',
                alpha=0.5, lw=2, label='Recovered')
        ax.plot(self._time, self.D / self._totalPopulation, 'k',
                alpha=0.5, lw=2, label='Death')
        ax.set_xlabel('Time /days')
        ax.set_ylabel('Ratio (' + str(self._totalPopulation) + ' orang)')
        ax.set_ylim(0, 1.2)
        ax.yaxis.set_tick_params(length=0)
        ax.xaxis.set_tick_params(length=0)
        ax.grid(b=True, which='major', c='w', lw=2, ls='-')
        legend = ax.legend()
        legend.get_frame().set_alpha(0.5)
        for spine in ('top', 'right', 'bottom', 'left'):
            ax.spines[spine].set_visible(False)
        plt.show()

    def debug(self):
        """
        +   Fungsi debug()
            = > Kegunaan :
            memberikan informasi semua
            parameter yang dimiliki model
        """
        print("\nS0: {} orang\nE0: {} orang\nI0: {} orang\nR0: {} orang\nD0: {} orang\n".format(
            self._S0, self._E0, self._I0, self._R0, self._D0
        ))
        print("S: {}, ...\nE: {}, ...\nI: {}, ...\nR: {}, ...\nD: {}, ...\n".format(
            ", ".join(str(element) for element in self.S[:3]),
            ", ".join(str(element) for element in self.E[:3]),
            ", ".join(str(element) for element in self.I[:3]),
            ", ".join(str(element) for element in self.R[:3]),
            ", ".join(str(element) for element in self.D[:3])
        ))
        print("Populasi: {} orang\nMasa Infeksi: {} hari\nMasa Inkubasi: {} hari\n".format(
            self._totalPopulation, self._infectionTime, self._incubationTime
        ), end="")
        print("Lama pandemi: {} hari\nLama hari sebelum meninggal: {} hari\n".format(
            self._time.size, self._timeBeforeDeath
        ))
        print("Nilai Alpha: {}\nNilai Delta: {}\nNilai Gamma: {}\nNilai Rho: {}\n".format(
            self._valAlpha, self.delta(), self.gamma(), self.rho(),
        ))
        print("="*6, "Sebaran Probabilitas Alpha")
        print(self._pAge)
        print("="*6, "Sebaran Proporsionalitas Umur")
        print(self._propAge)
