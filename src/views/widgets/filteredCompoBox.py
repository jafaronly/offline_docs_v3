from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtWidgets import QComboBox, QCompleter


class FilteredComboBox(QComboBox):
    def __init__(self, options, **kwargs):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)
        # self.dropEvent()
        self.completer = QCompleter(self)
        # always show all completions
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.pFilterModel = QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setPopup(self.view())
        self.setCompleter(self.completer)
        the_style = "border-top-left-radius: 10px; border-bottom-left-radius: 10px; background-color: #f5f5f5;"
        self.lineEdit().setStyleSheet(the_style)
        if "height" in kwargs:
            self.setFixedHeight(kwargs["height"])
        else:
            self.setFixedHeight(37)

        self.lineEdit().textEdited.connect(self.pFilterModel.setFilterFixedString)
        self.completer.activated.connect(self.setTextIfCompleterIsClicked)
        model = QStandardItemModel()
        for i, word in enumerate(options):
            item = QStandardItem(word)
            model.setItem(i, 0, item)
        self.setModel(model)
        self.setModelColumn(0)
        if "width" in kwargs:
            self.setFixedWidth(kwargs["width"])
        else:
            self.setFixedWidth(260)

        style = """
        QComboBox {
          border-radius: 10px;
        }

        QComboBox::drop-down:button{
            width: 25px;
            background-color: #f5f5f5;
            border-image: url(./resources/assets/images/drop_down.png);
            border-bottom-right-radius: 10px;
            border-top-right-radius: 10px;
        }

        QComboBox::drop-down:button:hover{
            background-color: #f5f5f5;
        }
        """
        self.setStyleSheet(style)

    def setModel(self, model):
        super(FilteredComboBox, self).setModel(model)
        self.pFilterModel.setSourceModel(model)
        self.completer.setModel(self.pFilterModel)

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        self.pFilterModel.setFilterKeyColumn(column)
        super(FilteredComboBox, self).setModelColumn(column)

    def view(self):
        return self.completer.popup()

    def index(self):
        return self.currentIndex()

    def setTextIfCompleterIsClicked(self, text):
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)

    def setMaximumWidth(self, p_int):
        self.setFixedWidth(p_int)
