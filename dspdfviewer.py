import sys
from qtpy import QtCore, QtWidgets, QtGui
import fitz
import presenterview


class ImageLoader(object):
    split_none = 0
    split_left = 1
    split_right = 2

    def __init__(self, doc, split, size):
        self.doc = doc
        self.split = split
        self.size = size

    def loadPage(self, page_no):
        page = self.doc.loadPage(page_no)

        clip = self.calcSplit(page.rect)
        pix = page.getPixmap(matrix=self.calcMatrix(clip), clip=clip)
        imageBytes = pix.getPNGData()

        image = QtGui.QImage()
        image.loadFromData(imageBytes)
        return QtGui.QPixmap(image)

    def calcSplit(self, rect):
        if self.split == ImageLoader.split_none:
            return rect

        if self.split == ImageLoader.split_right:
            return fitz.Rect(rect.br.x * 0.5, rect.tl.y, rect.br)

        return fitz.Rect(rect.tl, rect.br.x * 0.5, rect.br.y)

    def calcMatrix(self, rect):
        width = self.size[0] / rect.br.x
        height = self.size[1] / rect.br.y

        aspect = min(width, height)

        return fitz.Matrix(aspect, aspect)


class Pipe(QtCore.QObject):
    sig_close = QtCore.Signal(int)
    sig_change_page = QtCore.Signal(int)
    sig_reset = QtCore.Signal(int)
    sig_toggle_presenter_view = QtCore.Signal(int)


class Window(QtWidgets.QWidget):
    toggle_both = 1
    toggle_slides_notes = 2

    def __init__(self, pipe, doc):
        super().__init__(None)
        self.pipe = pipe
        self.page = 0
        self.pages = doc.pageCount

    def validPage(self, page):
        return 0 <= page < self.pages

    def keyPressEvent(self, event):
        # G: goto page
        # F1, ? help
        # F12, S swap screens
        # B, . blank screem

        if event.key() in [QtCore.Qt.Key_Escape, QtCore.Qt.Key_Q]:
            self.pipe.sig_close.emit(1)

        if event.key() in [QtCore.Qt.Key_Right, QtCore.Qt.Key_Space, QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return]:
            if self.validPage(self.page + 1):
                self.page += 1
                self.pipe.sig_change_page.emit(self.page)

        if event.key() in [QtCore.Qt.Key_Left, QtCore.Qt.Key_Backspace]:
            if self.validPage(self.page - 1):
                self.page -= 1
                self.pipe.sig_change_page.emit(self.page)

        if event.key() in [QtCore.Qt.Key_Home, QtCore.Qt.Key_H, QtCore.Qt.Key_R]:
            self.page = 0
            self.pipe.sig_change_page.emit(self.page)
            self.pipe.sig_reset.emit(1)

        if event.key() == QtCore.Qt.Key_T:
            self.pipe.sig_toggle_presenter_view.emit(Window.toggle_slides_notes)

        if event.key() == QtCore.Qt.Key_D:
            self.pipe.sig_toggle_presenter_view.emit(Window.toggle_both)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            if self.validPage(self.page - 1):
                self.page -= 1
                self.pipe.sig_change_page.emit(self.page)

        if event.button() == QtCore.Qt.LeftButton:
            if self.validPage(self.page + 1):
                self.page += 1
                self.pipe.sig_change_page.emit(self.page)

    def wheelEvent(self, event):
        if event.delta() > 0:
            if self.validPage(self.page - 1):
                self.page -= 1
                self.pipe.sig_change_page.emit(self.page)

        if event.delta() < 0:
            if self.validPage(self.page + 1):
                self.page += 1
                self.pipe.sig_change_page.emit(self.page)


class AudienceWindow(Window):
    def __init__(self, pipe, doc, screenSize):
        super().__init__(pipe, doc)
        self.screenSize = screenSize
        self.imageLoader = ImageLoader(doc, ImageLoader.split_left, screenSize)

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.imageLabel = QtWidgets.QLabel("image")
        self.changePage(0)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addWidget(self.imageLabel)
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(self.mainLayout)

        self.pipe.sig_close.connect(self.onClose)
        self.pipe.sig_change_page.connect(self.changePage)

    @QtCore.Slot(int)
    def onClose(self, _):
        self.close()

    @QtCore.Slot(int)
    def changePage(self, page):
        self.imageLabel.setPixmap(self.imageLoader.loadPage(page))


class PresenterWindow(Window):
    def __init__(self, pipe, doc, screenSize):
        super().__init__(pipe, doc)
        self.screenSize = screenSize

        self.imageLoader = ImageLoader(doc, ImageLoader.split_right, screenSize)

        self.sides_notes = Toggle(ImageLoader(doc, ImageLoader.split_left, screenSize), self.imageLoader)
        self.display_both = Toggle(ImageLoader(doc, ImageLoader.split_none, screenSize), self.imageLoader)

        self.presentationStarted = False

        self.ui = presenterview.Ui_Form()
        self.ui.setupUi(self)
        thumbSize = (screenSize[0]/10, screenSize[1]/10)
        self.thumbnailLoader = ImageLoader(doc, ImageLoader.split_none, thumbSize)

        self.updateSlide(0)

        self.pipe.sig_close.connect(self.onClose)
        self.pipe.sig_change_page.connect(self.changePage)
        self.pipe.sig_reset.connect(self.reset)
        self.pipe.sig_toggle_presenter_view.connect(self.toggle)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTimers)
        self.timer.start(1000)

        self.presentationClock = QtCore.QElapsedTimer()
        self.presentationClock.start()
        self.slideClock = QtCore.QElapsedTimer()
        self.slideClock.start()

    @QtCore.Slot(int)
    def onClose(self, _):
        self.close()

    @QtCore.Slot(int)
    def changePage(self, page):
        self.updateSlide(page)
        self.updateThumbs(page)

        if not self.presentationStarted:
            self.presentationClock.restart()
            self.presentationStarted = True

        self.slideClock.restart()

    def resizeEvent(self, event):
        self.updateThumbs(self.page)

    def updateSlide(self, page_no):
        page = self.imageLoader.loadPage(page_no)
        self.ui.imageLabel.resize(page.size())
        self.ui.imageLabel.setPixmap(page)

    def updateThumbs(self, page_no):
        thumbsize = (self.ui.thumbnailArea.frameRect().size().width() / 3, self.ui.thumbnailArea.frameRect().size().height())

        self.thumbnailLoader.size = thumbsize

        if self.validPage(page_no - 1):
            thumb = self.thumbnailLoader.loadPage(page_no - 1)
            self.ui.previousThumbnail.setPixmap(thumb)
            self.ui.previousThumbnail.show()
        else:
            self.ui.previousThumbnail.hide()

        thumb = self.thumbnailLoader.loadPage(page_no)
        self.ui.currentThumbnail.setPixmap(thumb)

        if self.validPage(page_no + 1):
            thumb = self.thumbnailLoader.loadPage(page_no + 1)
            self.ui.nextThumbnail.setPixmap(thumb)
            self.ui.nextThumbnail.show()
        else:
            self.ui.nextThumbnail.hide()

    @QtCore.Slot(int)
    def updateTimers(self):
        self.ui.wallClock.setText(QtCore.QTime.currentTime().toString('HH:mm:ss'))

        if self.presentationStarted:
            self.ui.slideClock.setText(QtCore.QTime(0,0).addMSecs(self.slideClock.elapsed()).toString('mm:ss'))
            self.ui.presentationClock.setText('Total\n' + QtCore.QTime(0, 0).addMSecs(self.presentationClock.elapsed()).toString('HH:mm:ss'))

    @QtCore.Slot(int)
    def reset(self):
        self.slideClock.restart()
        self.presentationClock.restart()
        self.updateTimers()
        self.presentationStarted = False

    @QtCore.Slot(int)
    def toggle(self, what):
        if what == Window.toggle_slides_notes:
            self.imageLoader = self.sides_notes.toggle()
            self.display_both.reset()

        if what == Window.toggle_both:
            self.imageLoader = self.display_both.toggle()
            self.sides_notes.reset()

        self.updateSlide(self.page)

class Toggle:
    def __init__(self, on, off):
        self.items = [off, on]
        self.state = 0

    def toggle(self):
        self.state = (self.state + 1) % 2
        return self.items[self.state]

    def reset(self):
        self.state = 0


class DSPydfViewer:
    def __init__(self, argv, app):
        self.pipe = Pipe()
        self.doc = fitz.open(argv[1])

        screens = app.screens()

        self.setupAudienceWindow(screens[1].geometry())
        self.setupPresenterWindow(screens[1].geometry())

    def setupAudienceWindow(self, screen):
        self.audienceWindow = AudienceWindow(self.pipe, self.doc, (screen.width(), screen.height()))
        self.audienceWindow.move(screen.x(), screen.y())
        self.audienceWindow.showFullScreen()

    def setupPresenterWindow(self, screen):
        self.presenterWindow = PresenterWindow(self.pipe, self.doc, (screen.width(), screen.height()))
        self.presenterWindow.move(screen.x(), screen.y())
        self.presenterWindow.showFullScreen()


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    viewer = DSPydfViewer(sys.argv, app)

    sys.exit(app.exec_())