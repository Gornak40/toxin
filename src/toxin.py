from tools import *
from gui import *
from db import *


class Toxin:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ex = ToxinUI()
        self.connect()
        self.showUI()
    
    def connect(self):
        self.links = list()
        self.downloadLink = str()
        self.ex.searchBtn.clicked.connect(self.searchFunc)
        self.ex.downloadBtn.clicked.connect(self.downloadFunc)
        self.ex.cancelBtn.clicked.connect(self.cancelFunc)
        self.ex.nextBtn.clicked.connect(self.nextFunc)
        self.ex.donateBtn.clicked.connect(self.donateFunc)
        self.ex.comboBox.currentIndexChanged[str].connect(self.onChange)
    
    def onChange(self, text):
        self.downloadLink = readDB(BASE, float(text.split()[0]))
    
    def searchH(self):
        name = self.ex.lineEdit.text()
        self.ex.lineEdit.setText(str())
        url = URL.format(name)
        self.links = parse(url, 'html', 'film')
        if not self.links:
            self.ex.statusBar.showMessage('Ничего не найдено')
            return
        self.index = 0
        self.nextH()
    
    def nextH(self):
        F = Filmer(self.links[self.index % len(self.links)])
        self.name = F.name
        self.index += 1
        self.sizes = [torrentSize(download(TORRENT, link)) for link in F.tors]
        makeDB(BASE, self.sizes, F.tors)
        try:
            self.ex.picLbl.setPixmap(QPixmap(imgResize(download(IMG, F.img))))
        except OSError:
            self.ex.picLbl.setPixmap(QPixmap(imgResize(ERROR)))
        self.ex.nameLbl.setText(F.name)
        self.ex.comboBox.clear()
        self.ex.comboBox.addItems('{} GB'.format(size) for size in filter(bool, sorted(set(self.sizes))))
        self.ex.statusBar.showMessage('{} {}'.format(len(self.links), fixWord('фильм', len(self.links))))
    
    def searchFunc(self):
        if not self.ex.lineEdit.text().strip():
            self.ex.statusBar.showMessage('Ничего не найдено')
            return
        self.ex.statusBar.showMessage('Поиск...')
        T = Thread(target=self.searchH)
        T.start()
    
    def loadTorrent(self):
        self.ses = session()
        self.ses.listen_on(6881, 6891)
        self.info = torrent_info(TORRENT)
        dnld = self.ses.add_torrent({'ti': self.info, 'save_path': KINO})
        stat = dnld.status()
        while not stat.is_seeding:
            stat = dnld.status()
            print('{}%'.format('%.2f' % (stat.progress * 100)))
            self.ex.speedLCD.display(round(stat.download_rate / 1000 / 1000, 2))
            sleep(1)
        self.ex.speedLCD.display(0)
        self.ex.statusBar.showMessage('Приятного просмотра')
    
    def downloadFunc(self):
        if not self.downloadLink:
            return
        system('mkdir {} -p'.format(KINO))
        download('{}.torrent'.format(KINO + self.name), self.downloadLink)
        self.ex.statusBar.showMessage('Торрент файл загружен')
        #self.ex.statusBar.showMessage('Скачивание фильма...')
        #Thread(target=self.loadTorrent).start()
    
    def cancelFunc(self):
        self.ex.close()
    
    def nextFunc(self):
        if not self.links:
            QMessageBox.about(self.ex, 'Ничего не найдено', 'Переформулируйте запрос')
            return
        self.ex.statusBar.showMessage('Поиск...')
        Thread(target=self.nextH).start()
    
    def donateFunc(self):
        wb.open(DONATE)
    
    def showUI(self):
        self.ex.show()
        sys.exit(self.app.exec())
        

if __name__ == '__main__':
    Toxin()
