
import math

from PyQt5.QtCore import pyqtSignal, QPointF, QSize, Qt
from PyQt5.QtGui import QPainter, QPolygonF
from PyQt5.QtWidgets import (QStyle,
                             QStyledItemDelegate, QWidget)


class Emitter(object):
    def __init__(self):
        self.connected = list()

    def emit(self, *args):
        for func in self.connected:
            func(*args)

    def connect(self, func, *args):
        if func not in self.connected:
            self.connected.append(func)

class StarRating(object):
    # enum EditMode
    Editable, ReadOnly = range(2)

    PaintingScaleFactor = 20
    # editingFinished = pyqtSignal(int)

    def __init__(self, starCount=1, maxStarCount=5):
        # super(StarRating, self).__init__()
        self._starCount = starCount
        self._maxStarCount = maxStarCount
        self.emitter = Emitter()

        self.starPolygon = QPolygonF([QPointF(1.0, 0.5)])
        for i in range(5):
            self.starPolygon << QPointF(0.5 + 0.5 * math.cos(0.8 * i * math.pi),
                                        0.5 + 0.5 * math.sin(0.8 * i * math.pi))

        self.diamondPolygon = QPolygonF()
        self.diamondPolygon << QPointF(0.4, 0.5) \
                            << QPointF(0.5, 0.4) \
                            << QPointF(0.6, 0.5) \
                            << QPointF(0.5, 0.6) \
                            << QPointF(0.4, 0.5)

    def starCount(self):
        return self._starCount

    def starCount2(self):
        return self._starCount

    def maxStarCount(self):
        return self._maxStarCount

    def setStarCount(self, starCount):
        self._starCount = starCount

    def setMaxStarCount(self, maxStarCount):
        self._maxStarCount = maxStarCount

    def sizeHint(self):
        return self.PaintingScaleFactor * QSize(self._maxStarCount, 1)

    def paint(self, painter, rect, palette, editMode):
        painter.save()

        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.NoPen)

        if editMode == StarRating.Editable:
            painter.setBrush(palette.highlight())
        else:
            painter.setBrush(palette.windowText())

        yOffset = (rect.height() - self.PaintingScaleFactor) / 2
        painter.translate(rect.x(), rect.y() + yOffset)
        painter.scale(self.PaintingScaleFactor, self.PaintingScaleFactor)

        for i in range(self._maxStarCount):
            if i < self._starCount:
                painter.drawPolygon(self.starPolygon, Qt.WindingFill)
            elif editMode == StarRating.Editable:
                painter.drawPolygon(self.diamondPolygon, Qt.WindingFill)

            painter.translate(1.0, 0.0)

        painter.restore()


class StarEditor(QWidget):

    editingFinished = pyqtSignal(int)

    def __init__(self, parent = None):
        super(StarEditor, self).__init__(parent)

        self._starRating = StarRating()

        self.setMouseTracking(True)
        self.setAutoFillBackground(True)

    def setStarRating(self, starRating):
        self._starRating = starRating

    def starRating(self):
        return self._starRating

    def sizeHint(self):
        return self._starRating.sizeHint()

    def paintEvent(self, event):
        painter = QPainter(self)
        self._starRating.paint(painter, self.rect(), self.palette(),
                StarRating.Editable)

    def mouseMoveEvent(self, event):
        star = self.starAtPosition(event.x())

        if star != self._starRating.starCount() and star != -1:
            self._starRating.setStarCount(star)
            self.update()

    def mouseReleaseEvent(self, event):
        star = self.starAtPosition(event.x())

        self.editingFinished.emit(int(star))

    def starAtPosition(self, x):
        # Enable a star, if pointer crosses the center horizontally.
        starwidth = self._starRating.sizeHint().width() // self._starRating.maxStarCount()
        star = (x + starwidth / 2) // starwidth
        if 0 <= star <= self._starRating.maxStarCount():
            return star

        return -1


class StarDelegate(QStyledItemDelegate):
    editingFinished = pyqtSignal(int)

    def paint(self, painter, option, index):
        starRating = index.data()
        if isinstance(starRating, StarRating):
            if option.state & QStyle.State_Selected:
                painter.fillRect(option.rect, option.palette.highlight())

            starRating.paint(painter, option.rect, option.palette,
                    StarRating.ReadOnly)
        else:
            super(StarDelegate, self).paint(painter, option, index)

    def sizeHint(self, option, index):
        starRating = index.data()
        if isinstance(starRating, StarRating):
            return starRating.sizeHint()
        else:
            return super(StarDelegate, self).sizeHint(option, index)

    def createEditor(self, parent, option, index):
        starRating = index.data()
        if isinstance(starRating, StarRating):
            editor = StarEditor(parent)
            editor.editingFinished.connect(self.commitAndCloseEditor)
            return editor
        else:
            return super(StarDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        starRating = index.data()
        if isinstance(starRating, StarRating):
            editor.setStarRating(starRating)
        else:
            super(StarDelegate, self).setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        starRating = index.data()
        if isinstance(starRating, StarRating):
            stars = editor.starRating()
            model.setData(index, stars)
            starRating.emitter.emit(stars)
            # editor.editingFinished.emit(int(editor.starRating()))
        else:
            super(StarDelegate, self).setModelData(editor, model, index)

    def commitAndCloseEditor(self, stars):
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor)
        self.editingFinished.emit(stars)


