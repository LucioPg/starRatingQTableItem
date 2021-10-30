
from PyQt5.QtWidgets import QTableWidget
from .m_qtableitem import BaseItem
from .star_rating_delegate import StarDelegate
from .m_qtableitem import StarRatingItem
from abc import abstractmethod



class AbsStarRatingTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(AbsStarRatingTable, self).__init__(*args, **kwargs)
        self.itemChanged.connect(self.item_change_callbk)

    @abstractmethod
    def item_change_callbk(self, item):
            pass

    def setItem(self, row: int, column: int, item: BaseItem) -> None:
        if isinstance(item, StarRatingItem):
            self._check_delegate()
        return super(AbsStarRatingTable, self).setItem(row, column, item)

    def _check_delegate(self):
        if not isinstance(self.itemDelegate(), StarDelegate):
            self.setItemDelegate(StarDelegate())

    @abstractmethod
    def populate_table(self, data):
        pass