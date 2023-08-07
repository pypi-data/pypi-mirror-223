from Furious.Gui.Action import Action, Seperator
from Furious.Widget.Widget import Menu, MessageBox, ZoomableTextBrowser
from Furious.Utility.Utility import (
    StateContext,
    SupportConnectedCallback,
    bootstrapIcon,
)
from Furious.Utility.Translator import Translatable, gettext as _
from Furious.Utility.Theme import DraculaTheme

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QTextBrowser


class SaveErrorBox(MessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.saveError = ''

    def getText(self):
        if self.saveError:
            return _('Unable to save log.') + f'\n\n{self.saveError}'
        else:
            return _('Unable to save log.')

    def retranslate(self):
        with StateContext(self):
            self.setWindowTitle(_(self.windowTitle()))
            self.setText(self.getText())

            # Ignore informative text, buttons

            self.moveToCenter()


class SaveAsFileAction(Action):
    def __init__(self, **kwargs):
        super().__init__(_('Save As...'), **kwargs)

        self.saveErrorBox = SaveErrorBox(
            icon=MessageBox.Icon.Critical, parent=self.parent()
        )

    def triggeredCallback(self, checked):
        filename, selectedFilter = QFileDialog.getSaveFileName(
            self.parent(), _('Save File'), filter=_('Text files (*.txt);;All files (*)')
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(self.parent().textBrowser.toPlainText())
            except Exception as ex:
                # Any non-exit exceptions

                self.saveErrorBox.saveError = str(ex)
                self.saveErrorBox.setWindowTitle(_('Error saving log'))
                self.saveErrorBox.setText(self.saveErrorBox.getText())

                # Show the MessageBox and wait for user to close it
                self.saveErrorBox.exec()


class ExitAction(Action):
    def __init__(self, **kwargs):
        super().__init__(_('Exit'), **kwargs)

    def triggeredCallback(self, checked):
        self.parent().syncSettings()
        self.parent().hide()


class CopyAction(Action):
    def __init__(self, **kwargs):
        super().__init__(_('Copy'), icon=bootstrapIcon('files.svg'), **kwargs)

        self.setShortcut(
            QtCore.QKeyCombination(
                QtCore.Qt.KeyboardModifier.ControlModifier,
                QtCore.Qt.Key.Key_C,
            )
        )

    def triggeredCallback(self, checked):
        self.parent().textBrowser.copy()


class SelectAllAction(Action):
    def __init__(self, **kwargs):
        super().__init__(_('Select All'), **kwargs)

        self.setShortcut(
            QtCore.QKeyCombination(
                QtCore.Qt.KeyboardModifier.ControlModifier,
                QtCore.Qt.Key.Key_A,
            )
        )

    def triggeredCallback(self, checked):
        self.parent().textBrowser.selectAll()


class ZoomInAction(Action):
    def __init__(self, **kwargs):
        super().__init__(_('Zoom In'), **kwargs)

        self.setShortcut(
            QtCore.QKeyCombination(
                QtCore.Qt.KeyboardModifier.ControlModifier, QtCore.Qt.Key.Key_Plus
            )
        )

    def triggeredCallback(self, checked):
        self.parent().textBrowser.zoomIn()


class ZoomOutAction(Action):
    def __init__(self, **kwargs):
        super().__init__(_('Zoom Out'), **kwargs)

        self.setShortcut(
            QtCore.QKeyCombination(
                QtCore.Qt.KeyboardModifier.ControlModifier, QtCore.Qt.Key.Key_Minus
            )
        )

    def triggeredCallback(self, checked):
        self.parent().textBrowser.zoomOut()


class LogViewerWidget(Translatable, SupportConnectedCallback, QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle(_('Log Viewer'))
        self.setWindowIcon(bootstrapIcon('rocket-takeoff-window.svg'))

        self.textBrowser = ZoomableTextBrowser(parent=self)
        self.textBrowser.setLineWrapMode(QTextBrowser.LineWrapMode.NoWrap)
        self.textBrowser.setStyleSheet(
            DraculaTheme.getStyleSheet(
                widgetName='QTextBrowser',
                fontFamily=QApplication.instance().customFontName,
            )
        )

        try:
            # Restore point size
            font = self.textBrowser.font()
            font.setPointSize(int(QApplication.instance().ViewerWidgetPointSize))

            self.textBrowser.setFont(font)
        except Exception:
            # Any non-exit exceptions

            pass

        self.setCentralWidget(self.textBrowser)

        fileMenuActions = [
            SaveAsFileAction(parent=self),
            Seperator(),
            ExitAction(parent=self),
        ]

        editMenuActions = [
            CopyAction(parent=self),
            Seperator(),
            SelectAllAction(parent=self),
        ]

        viewMenuActions = [
            ZoomInAction(parent=self),
            ZoomOutAction(parent=self),
        ]

        for menu in (fileMenuActions, editMenuActions, viewMenuActions):
            for action in menu:
                if isinstance(action, Action):
                    setattr(self, f'{action}', action)

        self._fileMenu = Menu(*fileMenuActions, title=_('File'), parent=self)
        self._editMenu = Menu(*editMenuActions, title=_('Edit'), parent=self)
        self._viewMenu = Menu(*viewMenuActions, title=_('View'), parent=self)

        self.menuBar().addMenu(self._fileMenu)
        self.menuBar().addMenu(self._editMenu)
        self.menuBar().addMenu(self._viewMenu)

    def log(self):
        return self.textBrowser.toPlainText()

    def syncSettings(self):
        QApplication.instance().ViewerWidgetPointSize = str(
            self.textBrowser.font().pointSize()
        )

    def closeEvent(self, event):
        event.ignore()

        self.syncSettings()
        self.hide()

    def connectedCallback(self):
        self.setWindowIcon(bootstrapIcon('rocket-takeoff-connected-dark.svg'))

    def disconnectedCallback(self):
        self.setWindowIcon(bootstrapIcon('rocket-takeoff-window.svg'))

    def retranslate(self):
        with StateContext(self):
            self.setWindowTitle(_(self.windowTitle()))
