import requests
from bs4 import BeautifulSoup

def test():
    return download("http://loveread.ec/read_book.php?id=70351", True)

def download(book_url, save=True, folder=""):
    base_url = "http://loveread.ec/read_book.php?id=%(id)s&p=%(page)s"
    ID = book_url.split("id=")[-1].split("&")[0]
    r = requests.get(base_url % {"id": ID, "page": 1})
    r.encoding = "Windows-1251"
    soup = BeautifulSoup(r.text, "html.parser")
    PAGES = int(soup.select(".navigation a")[-2].get_text())
    NAME = soup.select(".tb_read_book h2 a")[0].get_text()

    book = []
    for i in range(1, PAGES+1):
        url = base_url % {"id": ID, "page": i}
        print("downloading from ", url)
        r = requests.get(url)
        r.encoding = "Windows-1251"
        soup = BeautifulSoup(r.text, "html.parser")
        main = soup.select("p.MsoNormal")
        book.append(main[0].get_text() + "")
        # for elem in main:
        #     book.append(elem.get_text() + "///")

    handler = open(folder + NAME + ".txt", "w+")
    strBook = "\r\n\r\n".join(book)
    if save:
        for i in strBook:
            try:
                handler.write(i)
            except ValueError:
                handler.write("?")
                
    return strBook
