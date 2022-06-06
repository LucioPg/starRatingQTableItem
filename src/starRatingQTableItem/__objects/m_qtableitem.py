
from PyQt5.QtCore import pyqtSignal, Qt, QObject
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QStandardItem

from .star_rating_delegate import StarRating


class _InnerQObject(QObject):
    value_changed = pyqtSignal(QTableWidgetItem)
    starEditFinished = pyqtSignal(int, int)

class _InnerStandardQObject(QObject):
    value_changed = pyqtSignal(QStandardItem)
    starEditFinished = pyqtSignal(int, int)

class BaseStandardItem(QStandardItem):

    def __init__(self, *args, **kwargs):
        super(BaseStandardItem, self).__init__(*args, **kwargs)
        self._inner_qobjc = _InnerStandardQObject()
        self.value_changed = self._inner_qobjc.value_changed
        self._value = self._old_value = args[0] if args else None


    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def old_value(self):
        return self._old_value

    @old_value.setter
    def old_value(self, val):
        self._old_value = val

    def setText(self, atext: str) -> None:
        self._set_values(atext)
        super(BaseStandardItem, self).setText(atext)

    def text(self) -> str:
        return str(self.value) if self.value is not None else ''

    def _set_values(self, value):
        self.old_value = self.value
        self.value = value
        self.value_changed.emit(self)

    def setData(self, role: int, value) -> None:
        if role == Qt.EditRole:
            if value != self.old_value:
                self._set_values(value)
        super(BaseStandardItem, self).setData(role, value)


class BaseItem(QTableWidgetItem):

    def __init__(self, *args, **kwargs):
        super(BaseItem, self).__init__(*args, **kwargs)
        self._inner_qobjc = _InnerQObject()
        self.value_changed = self._inner_qobjc.value_changed
        self._value = self._old_value = args[0] if args else None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def old_value(self):
        return self._old_value

    @old_value.setter
    def old_value(self, val):
        self._old_value = val

    def setText(self, atext: str) -> None:
        self._set_values(atext)
        super(BaseItem, self).setText(atext)

    def text(self) -> str:
        return str(self.value) if self.value is not None else ''

    def _set_values(self, value):
        self.old_value = self.value
        self.value = value
        self.value_changed.emit(self)

    def setData(self, role: int, value) -> None:
        if role == Qt.EditRole:
            if value != self.old_value:
                self._set_values(value)
        super(BaseItem, self).setData(role, value)


class StarRatingStandardItem(BaseStandardItem):

    def __init__(self, rating, query):
        super(StarRatingStandardItem, self).__init__()
        self.starEditFinished = self._inner_qobjc.starEditFinished
        star_rating = StarRating(rating)
        self.setData(star_rating, 0)
        self.query = query

    @staticmethod
    def _get_star_rating_obj(rating):
        return StarRating(rating)

    def _set_start_rating(self, star_rating: StarRating):

        self.emitter = star_rating.emitter
        self.emitter.connect(self.star_editing_processor)

    def new_start_rating(self, rating):
        star_rating = self._get_star_rating_obj(rating)
        self._set_start_rating(star_rating)
        return star_rating

    def setData(self, value: StarRating, role:int) -> None:
        if isinstance(value, StarRating) and role in (Qt.EditRole, Qt.DisplayRole):
            stars = int(value.starCount())
            if stars != self.old_value:
                # if self.value is not None:
                self.old_value = self.value
                if self.value != stars:
                    self.value = stars
                    value = self.new_start_rating(stars)
                    self.value_changed.emit(self)
        super(BaseStandardItem, self).setData(value, role)

    def _set_old_ratting(self, rating):
        self.old_rating = rating
        self.setData(Qt.UserRole, rating)

    def star_editing_processor(self, stars):
        self.value_changed.emit(self)

class StarRatingItem(BaseItem):

    def __init__(self, rating):
        super(StarRatingItem, self).__init__()
        # self._check_delegate()
        self.starEditFinished = self._inner_qobjc.starEditFinished
        star_rating = StarRating(rating)
        self.setData(0, star_rating)

    @staticmethod
    def _get_star_rating_obj(rating):
        return StarRating(rating)

    def _set_start_rating(self, star_rating: StarRating):

        self.emitter = star_rating.emitter
        self.emitter.connect(self.star_editing_processor)

    def new_start_rating(self, rating):
        star_rating = self._get_star_rating_obj(rating)
        self._set_start_rating(star_rating)
        return star_rating

    def setData(self, role: int, value) -> None:
        if isinstance(value, StarRating) and role in (Qt.EditRole, Qt.DisplayRole):
            stars = int(value.starCount())
            if stars != self.old_value:
                # if self.value is not None:
                self.old_value = self.value
                if self.value != stars:
                    self.value = stars
                    value = self.new_start_rating(stars)
                    self.value_changed.emit(self)
        super(BaseItem, self).setData(role, value)

    def _set_old_ratting(self, rating):
        self.old_rating = rating
        self.setData(Qt.UserRole, rating)

    def star_editing_processor(self, stars):
        self.value_changed.emit(self)