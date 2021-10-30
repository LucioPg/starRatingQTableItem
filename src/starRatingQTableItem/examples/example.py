__all__ = [
    'run'
]


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QTableWidgetItem)
from ..__objects.starRatingQTable import AbsStarRatingTable
from ..__objects.m_qtableitem import BaseItem, StarRatingItem
from random import randint



class StarRatingTable(AbsStarRatingTable):
    def __init__(self, *args, **kwargs):
        super(StarRatingTable, self).__init__(*args, **kwargs)

    def item_change_callbk(self, item):
        if isinstance(item, StarRatingItem):
            print(item.value, item.old_value)
        else:
            print(item.text())

    def populate_table(self, data):

        for row, ((title, title_flags), (genre, gen_flags), (artist, artist_flags), (rating, rating_flags)) in enumerate(data):
            item0 = BaseItem(title)
            item0.setData(Qt.UserRole, randint(1,100))
            item0.setToolTip(str(item0.data(Qt.UserRole)))
            for flag in title_flags:
                item0.setFlags(item0.flags() ^ flag)

            item1 = QTableWidgetItem(genre) #BaseItem(genre)
            item2 = QTableWidgetItem(artist) #BaseItem(artist)
            item3 = StarRatingItem(rating ) #StarRatingItem(rating)
            self.setItem(row, 0, item0)
            self.setItem(row, 1, item1)
            self.setItem(row, 2, item2)
            self.setItem(row, 3, item3)


def run():
    staticData = (
        (("Mass in B-Minor", [Qt.ItemIsEditable]), ("Baroque", []), ("MJ.S. Bach", []), (5, [])),
        (("Three More Foxes", []), ("Jazz", []), ("Maynard Ferguson", []), (4, [])),
        (("Sex Bomb", []), ("Pop", []), ("Tom Jones", []), (3, [])),
        (("Barbie Girl", []), ("Pop", []), ("Aqua", []), (5, [])),
    )

    import sys

    app = QApplication(sys.argv)

    tableWidget = StarRatingTable(4, 4)
    tableWidget.setEditTriggers(
        QAbstractItemView.DoubleClicked)
    tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

    headerLabels = ("Title", "Genre", "Artist", "Rating")
    tableWidget.setHorizontalHeaderLabels(headerLabels)

    tableWidget.populate_table(staticData)
    tableWidget.resizeColumnsToContents()
    tableWidget.resize(500, 300)
    tableWidget.show()

    sys.exit(app.exec_())
