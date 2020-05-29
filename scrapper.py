import requests
from bs4 import BeautifulSoup


def saveFile(content, filename):
    print("Menyimpan: ", filename)
    with open("dataset/" + filename, mode="wb") as file:
        file.write(content)


if __name__ == '__main__':
    """
    Kami menggunakan data `dati-andamento-nazionale`
    yang berisi data harian jumlah kasus COVID-19 di itali.
    Diperoleh dari situs github :
    https://github.com/pcm-dpc/COVID-19/tree/master/dati-andamento-nazionale
    """
    url = 'https://github.com/pcm-dpc/COVID-19/tree/master/dati-andamento-nazionale'

    """
    Pertama, pergi ke alamat url.
    Lalu simpan nama-nama file yang akan di download.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="html.parser")
    tag = soup.select("td.content > span > a")
    links = []
    for a in tag:
        links.append(a['href'])

    """
    Dari link yang telah diperoleh, kita akan menyimpan file
    satu per satu dengan format csv pada directory dataset/ .
    ganti host url dengan url untuk raw file github yaitu :
    https://raw.githubusercontent.com/
    """
    url = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/"
    for link in links:
        filename = link.split("/")[-1]
        print("[GET]", url + filename)
        response = requests.get(url + filename)
        saveFile(response.content, filename)
