import sys
import vlc
from PyQt6 import sip
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QToolBar,
    QToolButton,
    QScrollArea,
    QHBoxLayout,
    QSizePolicy,
    QDialog,
    QLineEdit,
    QDialogButtonBox,
    QFormLayout,
    QPushButton,
    QSpacerItem,
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
        self.browser.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Top bar with Close button and URL edit
        top_bar = QHBoxLayout()

        self.url_edit = QLineEdit(url)
        self.url_edit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.url_edit.editingFinished.connect(self.on_url_edited)
        top_bar.addWidget(self.url_edit)

        grow_button = QPushButton()
        grow_icon = QIcon("btn-grow.png")
        grow_button.setIcon(grow_icon)  # fixed bug: was previously close_icon
        grow_button.setText("")
        grow_button.clicked.connect(self.request_grow)
        top_bar.addWidget(grow_button)

        close_button = QPushButton()
        close_icon = QIcon("btn-exit.png")
        close_button.setIcon(close_icon)
        close_button.setText("")
        close_button.clicked.connect(self.request_close)
        top_bar.addWidget(close_button)

        layout.addLayout(top_bar)
        layout.addWidget(self.browser)

        self.browser.urlChanged.connect(self.on_browser_url_changed)
        self.close_requested = None

    def request_close(self):
        if self.close_requested:
            self.close_requested(self)

    def request_grow(self):
        # Get a reference to the main window, which should be Fasemo
        main_window = self.window()
        if not main_window:
            return

        # Attempt to get the scroll area from the main window
        if not hasattr(main_window, "scroll_area"):
            return

        scroll_area = main_window.scroll_area

        # Make sure layout adjustments are up-to-date
        scroll_area.widget().adjustSize()

        # Compute the new width: use the viewport's width to "fill" the window
        viewport_width = scroll_area.viewport().width()

        # Set this browser container to a fixed width equal to the viewport width
        self.setFixedWidth(viewport_width)

        # After changing the size, adjust the layout again
        scroll_area.widget().adjustSize()

        # We now want to center this BrowserContainer in the scroll area.
        # To do this, we find the horizontal position and size of this widget,
        # and then set the scroll bar so that the widget is centered.

        # Get current geometry relative to the parent container
        container_pos_x = self.x()
        container_width = self.width()

        # Get viewport width for centering calculation
        view_width = scroll_area.viewport().width()

        # Calculate the scroll value needed to center the browser container
        # Desired center: widget center aligned with viewport center
        desired_scroll_value = (
            container_pos_x + (container_width / 2) - (view_width / 2)
        )

        # Ensure the value is within valid range
        h_scrollbar = scroll_area.horizontalScrollBar()
        desired_scroll_value = max(desired_scroll_value, h_scrollbar.minimum())
        desired_scroll_value = min(desired_scroll_value, h_scrollbar.maximum())

        # Set the scrollbar to the calculated position
        h_scrollbar.setValue(int(desired_scroll_value))

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


class Fasemo(QMainWindow):
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
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
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
        new_button = QToolButton()
        new_button.setText("New")
        new_button.clicked.connect(self.on_new_button_clicked)
        self.toolbar.addWidget(new_button)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.toolbar)

        self.setWindowTitle("Fasemo")

        # Add toolbar buttons for initial browsers
        for bc in self.browser_containers:
            self.add_browser_button(bc)

        # Add spacer at the end
        self.add_spacer()

        if False:
            # Create a VLC instance
            self.vlc_instance = vlc.Instance()
            self.media_player = self.vlc_instance.media_player_new()

            # Create video widget
            self.videoWidget = QWidget(self)
            self.setCentralWidget(self.videoWidget)
            self.videoWidget.setGeometry(0, 0, 1920, 1080)

            # Set up video output
            if sys.platform == "linux":  # for Linux using the X Server
                self.media_player.set_xwindow(self.videoWidget.winId())
            elif sys.platform == "win32":  # for Windows
                self.media_player.set_hwnd(self.videoWidget.winId())
            elif sys.platform == "darwin":  # for MacOS
                self.media_player.set_nsobject(self.videoWidget.winId())

            # Load media
            media = self.vlc_instance.media_new('wallpaper.mp4')
            self.media_player.set_media(media)

            # Play media
            self.media_player.play()

        self.add_browser("https://www.google.com")

    def closeEvent(self, event):
        # Cleanup code: disconnect signals, set booleans, etc.
        super().closeEvent(event)

    def add_spacer(self):
        """Add (or re-add) the spacer at the end of the layout."""
        self.remove_existing_spacer()
        self.extra_spacer = QSpacerItem(
            self.screen_width, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        self.h_layout.addItem(self.extra_spacer)

    def remove_existing_spacer(self):
        """Remove the existing spacer from the layout if present."""
        if self.extra_spacer is None:
            return

        if self.h_layout is not None and not sip.isdeleted(self.h_layout):
            for i in range(self.h_layout.count()):
                item = self.h_layout.itemAt(i)
                if item is self.extra_spacer:
                    self.h_layout.removeItem(item)
                    self.extra_spacer = None
                    break

    def add_browser_button(self, bc):
        btn = QToolButton()
        btn.setText("")
        # When the button is clicked, center the corresponding browser
        btn.clicked.connect(
            lambda checked, browser_container=bc: self.center_browser(browser_container)
        )

        action = self.toolbar.addWidget(btn)
        self.browser_toolbar_actions.append((btn, action))
        bc.browser.iconChanged.connect(
            lambda _, b=bc.browser, bt=btn: self.updateButtonIcon(bt, b)
        )
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
        if hasattr(self, "toolbar"):
            self.add_browser_button(bc)

    def updateButtonIcon(self, button, browser):
        icon = browser.icon()
        if not icon.isNull():
            button.setIcon(icon)
            button.setIconSize(QSize(64, 64))
            button.setText("")

    def on_new_button_clicked(self):
        self.add_browser("https://www.google.com")

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

    def center_browser(self, bc: BrowserContainer):
        scroll_area = self.scroll_area
        # Ensure layout adjustments are up to date
        scroll_area.widget().adjustSize()

        # Calculate position to center the browser container
        container_pos_x = bc.x()
        container_width = bc.width()
        view_width = scroll_area.viewport().width()

        # Centering calculation: we want the center of the browser container
        # to align with the center of the viewport.
        desired_scroll_value = (
            container_pos_x + (container_width / 2) - (view_width / 2)
        )

        h_scrollbar = scroll_area.horizontalScrollBar()
        # Ensure the desired value is within the scrollbar's range
        desired_scroll_value = max(desired_scroll_value, h_scrollbar.minimum())
        desired_scroll_value = min(desired_scroll_value, h_scrollbar.maximum())

        # Scroll to the calculated position
        h_scrollbar.setValue(int(desired_scroll_value))


def main():
    app = QApplication(sys.argv)
    window = Fasemo()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
