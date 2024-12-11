import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QToolBar, QToolButton,
    QScrollArea, QHBoxLayout, QSizePolicy, QDialog, QLineEdit, QDialogButtonBox, QFormLayout, QPushButton, QSpacerItem
)
from PyQt6.QtCore import Qt, QUrl, QSize
from PyQt6.QtGui import QPixmap, QPainter, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView

class BrowserContainer(QWidget):
    def __init__(self, url: str, parent=None):
        super().__init__(parent)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        self.browser.setMinimumWidth(320)
        # Let the browser expand in both directions
        self.browser.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        # Top bar with Close button and URL edit
        top_bar = QHBoxLayout()

        self.url_edit = QLineEdit(url)
        self.url_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.url_edit.editingFinished.connect(self.on_url_edited)
        top_bar.addWidget(self.url_edit)

        close_button = QPushButton()
        close_icon = QIcon("btn-exit.png")
        close_button.setIcon(close_icon)
        close_button.setText("")  # Remove text
        close_button.clicked.connect(self.request_close)
        top_bar.addWidget(close_button)

        layout.addLayout(top_bar)
        layout.addWidget(self.browser)

        self.browser.urlChanged.connect(self.on_browser_url_changed)
        self.close_requested = None

    def request_close(self):
        if self.close_requested:
            self.close_requested(self)

    def on_browser_url_changed(self, qurl: QUrl):
        self.url_edit.setText(qurl.toString())

    def on_url_edited(self):
        text = self.url_edit.text().strip()
        if text:
            if not (text.startswith("http://") or text.startswith("https://")):
                text = "http://" + text
            self.browser.setUrl(QUrl(text))

class SplitterHandle(QWidget):
    def __init__(self, left_widget, container, parent=None):
        super().__init__(parent)
        self.left_widget = left_widget
        self.container = container
        self.setFixedWidth(20)
        self.setCursor(Qt.CursorShape.SplitHCursor)
        self.dragging = False
        self.offset = 0

        # Load the pixmap (drag image)
        self.drag_pixmap = QPixmap("drag.png")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.position().x()

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.position().x() - self.offset
            new_width = self.left_widget.width() + delta
            if new_width < 320:
                new_width = 320
            self.left_widget.setFixedWidth(int(new_width))
            self.offset = event.position().x()
            self.container.adjustSize()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        
        # Center the pixmap horizontally and vertically
        x = (self.width() - self.drag_pixmap.width()) // 2
        y = (self.height() - self.drag_pixmap.height()) // 2
        painter.drawPixmap(x, y, self.drag_pixmap)


class NewUrlDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Open New URL")

        layout = QFormLayout()
        self.url_edit = QLineEdit()
        layout.addRow("URL:", self.url_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_url(self):
        return self.url_edit.text().strip()

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout()
        central_widget.setLayout(self.main_layout)

        # Horizontal container
        self.h_layout = QHBoxLayout()
        self.h_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.container = QWidget()
        self.container.setLayout(self.h_layout)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidget(self.container)
        self.main_layout.addWidget(self.scroll_area)

        # Track browsers, handles, and toolbar actions
        self.browser_containers = []
        self.handles = []
        self.browser_toolbar_actions = []

        # Determine screen width for spacer
        screen = QApplication.primaryScreen()
        self.screen_width = screen.availableGeometry().width()
        self.extra_spacer = None

        # Create first toolbar for browser buttons
        self.toolbar = QToolBar("Browser Toolbar")
        self.toolbar.setOrientation(Qt.Orientation.Horizontal)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.toolbar)

        # Second toolbar with "New" button
        toolbar2 = QToolBar("New Toolbar")
        toolbar2.setOrientation(Qt.Orientation.Horizontal)
        new_button = QToolButton()
        new_button.setText("New")
        new_button.clicked.connect(self.on_new_button_clicked)
        toolbar2.addWidget(new_button)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, toolbar2)

        self.setWindowTitle("Fasemo")

        # Add toolbar buttons for initial browsers
        for bc in self.browser_containers:
            self.add_browser_button(bc)

        # Add spacer at the end
        self.add_spacer()

    def add_spacer(self):
        """Add (or re-add) the spacer at the end of the layout."""
        self.remove_existing_spacer()
        self.extra_spacer = QSpacerItem(self.screen_width, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.h_layout.addItem(self.extra_spacer)

    def remove_existing_spacer(self):
        """Remove the existing spacer from the layout if present."""
        if self.extra_spacer is None:
            return
        for i in range(self.h_layout.count()):
            item = self.h_layout.itemAt(i)
            if item is self.extra_spacer:
                self.h_layout.removeItem(item)
                self.extra_spacer = None
                break

    def add_browser_button(self, bc):
        btn = QToolButton()
        btn.setText("")
        action = self.toolbar.addWidget(btn)
        self.browser_toolbar_actions.append((btn, action))
        bc.browser.iconChanged.connect(lambda _, b=bc.browser, bt=btn: self.updateButtonIcon(bt, b))
        self.updateButtonIcon(btn, bc.browser)

    def add_browser(self, url: str):
        # Before adding a new browser, remove spacer so we can put it after the new elements
        self.remove_existing_spacer()

        bc = BrowserContainer(url)
        bc.close_requested = self.close_browser

        # Add the browser
        self.h_layout.addWidget(bc)
        self.browser_containers.append(bc)

        # After adding a browser, always add a handle to its right
        handle = SplitterHandle(bc, self.container)
        self.h_layout.addWidget(handle)
        self.handles.append(handle)

        # Re-add the spacer at the end
        self.add_spacer()
        self.container.adjustSize()

        # If toolbar already exists, add a button for this new browser
        if hasattr(self, 'toolbar'):
            self.add_browser_button(bc)

    def updateButtonIcon(self, button, browser):
        icon = browser.icon()
        if not icon.isNull():
            button.setIcon(icon)
            button.setIconSize(QSize(64,64))
            button.setText("")

    def on_new_button_clicked(self):
        dialog = NewUrlDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            url = dialog.get_url()
            if url:
                if not (url.startswith("http://") or url.startswith("https://")):
                    url = "http://" + url
                self.add_browser(url)

    def close_browser(self, bc: BrowserContainer):
        if bc not in self.browser_containers:
            return
        index = self.browser_containers.index(bc)

        # Remove spacer first
        self.remove_existing_spacer()

        # Remove the browser container
        item_to_remove = self.find_layout_item(self.h_layout, bc)
        if item_to_remove is not None:
            self.h_layout.removeItem(item_to_remove)
        self.h_layout.removeWidget(bc)
        bc.setParent(None)
        self.browser_containers.remove(bc)

        # Remove the handle right after this browser
        if index < len(self.handles):
            handle = self.handles[index]
            handle_item = self.find_layout_item(self.h_layout, handle)
            if handle_item is not None:
                self.h_layout.removeItem(handle_item)
            self.h_layout.removeWidget(handle)
            handle.setParent(None)
            self.handles.pop(index)

        # Remove corresponding toolbar button and action
        if index < len(self.browser_toolbar_actions):
            btn, action = self.browser_toolbar_actions[index]
            self.toolbar.removeAction(action)
            self.browser_toolbar_actions.pop(index)

        # Re-add spacer
        self.add_spacer()
        self.container.adjustSize()

    def find_layout_item(self, layout, widget):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and item.widget() == widget:
                return item
        return None

def main():
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
