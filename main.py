#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import (
    QApplication,QWidget, 
    QFileDialog, QLabel, 
    QPushButton, QHBoxLayout,
    QVBoxLayout, QListWidget 
) 

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap 


from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import (
    BLUR, SHARPEN, SMOOTH, CONTOUR
)


app = QApplication([])
win = QWidget()
win.resize(900,600)
win.setWindowTitle('Eazy Editor')
lb_image = QLabel("Картинка")
btn_dir = QPushButton("Папка")
lw_files = QListWidget()

btn_right = QPushButton('Право')
btn_left = QPushButton('Лево')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')
btn_blur = QPushButton('Размытие')
btn_smooth = QPushButton('Гладкий')
btn_contour = QPushButton('Контурный')

row = QHBoxLayout()  #Основная строка
col1 = QVBoxLayout()  #Делится на два столба
col2 = QVBoxLayout()
col1.addWidget(btn_dir)  #в перовом - кнопка выбора директори
col1.addWidget(lw_files) #и список файлов
col2.addWidget(lb_image, 95)  #во втором - картинка
row_tools = QHBoxLayout()  #и строка кнопок
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
row_tools.addWidget(btn_blur)
row_tools.addWidget(btn_smooth)
row_tools.addWidget(btn_contour)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)

win.show()

workdir = ' '

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)

    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)
    
btn_dir.clicked.connect(showFilenamesList)


class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, filename):
        ''' при загрузке запоминаем путь и имя файла '''
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)

    def saveImage(self):
        '''сохраняет копию файла в подпапке'''
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)

        self.image.save(fullname)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
            
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_blur(self):
        self.image = self.image.filter(BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_smooth(self):
        self.image = self.image.filter(SMOOTH)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_contour(self):
        self.image = self.image.filter(CONTOUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()


def showChoosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))


workimage = ImageProcessor()
lw_files.currentRowChanged.connect(showChoosenImage)


btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharp)
btn_flip.clicked.connect(workimage.do_flip)
btn_blur.clicked.connect(workimage.do_blur)
btn_smooth.clicked.connect(workimage.do_smooth)
btn_contour.clicked.connect(workimage.do_contour)


app.exec()