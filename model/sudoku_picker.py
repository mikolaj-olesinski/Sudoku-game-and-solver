from PySide6.QtWidgets import QTableView, QStyledItemDelegate, QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QMouseEvent, QPixmap
from model.utils.func import import_data_from_db
from controller.apps.sudoku_game_app import sudoku_app
from database.deleteData import deleteUsersSudoku
from database.resetData import resetUsersSudoku
from database.getData import get_username_from_id
import os

class SudokuModel(QAbstractTableModel):
    """
    A custom model for displaying Sudoku data in a QTableView.

    Attributes:
    - user_id (int): User ID associated with the Sudoku data.
    - sudoku_data (list): List of lists containing Sudoku data fetched from the database.

    Methods:
    - rowCount(parent=QModelIndex()): Returns the number of rows in the model.
    - columnCount(parent=QModelIndex()): Returns the number of columns in the model.
    - data(index, role=Qt.DisplayRole): Returns the data to be displayed at the specified index.
    - headerData(section, orientation, role=Qt.DisplayRole): Returns the header data for the specified section.
    - sort(column, order): Sorts the data in the model based on the specified column and order.
    - update_data(): Updates the Sudoku data by fetching it again from the database.
    """

    def __init__(self, user_id):
        """
        Initializes the SudokuModel with the given user ID.

        Args:
        - user_id (int): User ID associated with the Sudoku data.
        """
        super().__init__()
        self.user_id = user_id
        self.sudoku_data = import_data_from_db(user_id)

    def rowCount(self, parent=QModelIndex()):
        """
        Returns the number of rows in the model.

        Args:
        - parent (QModelIndex): Optional parent index.

        Returns:
        - int: Number of rows in the model.
        """
        if not self.sudoku_data:
            return 1 
        return len(self.sudoku_data)

    def columnCount(self, parent=QModelIndex()):
        """
        Returns the number of columns in the model.

        Args:
        - parent (QModelIndex): Optional parent index.

        Returns:
        - int: Number of columns in the model.
        """
        if not self.sudoku_data:
            return 1
        return len(self.sudoku_data[0]) + 3 

    def data(self, index, role=Qt.DisplayRole):
        """
        Returns the data to be displayed at the specified index.

        Args:
        - index (QModelIndex): Index of the item.
        - role (Qt.ItemDataRole): Role of the item data.

        Returns:
        - QVariant: Data to be displayed at the index with the specified role.
        """
        if not self.sudoku_data:
            if role == Qt.DisplayRole and index.row() == 0 and index.column() == 0:
                return "No data available"  
            return None

        if role == Qt.DisplayRole:
            if index.column() < 7:
                return self.sudoku_data[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Returns the header data for the specified section.

        Args:
        - section (int): Section index.
        - orientation (Qt.Orientation): Header orientation.
        - role (Qt.ItemDataRole): Role of the header data.

        Returns:
        - QVariant: Header data for the specified section and role.
        """
        if role == Qt.DisplayRole:
            if not self.sudoku_data:
                return ""  
            if orientation == Qt.Horizontal:
                headers = ['id', 'difficulty', 'is solved', 'created', 'timer', 'started', 'last saved', 'Start', 'Reset', 'Delete']
                return headers[section]

    def sort(self, column, order):
        """
        Sorts the data in the model based on the specified column and order.

        Args:
        - column (int): Column index to sort by.
        - order (Qt.SortOrder): Sort order (Ascending or Descending).
        """
        self.layoutAboutToBeChanged.emit()
        if self.sudoku_data and column < 7: 
            self.sudoku_data.sort(key=lambda x: x[column], reverse=order == Qt.DescendingOrder)
        self.layoutChanged.emit()

    def update_data(self):
        """
        Updates the Sudoku data by fetching it again from the database.
        """
        self.sudoku_data = import_data_from_db(self.user_id)
        self.layoutChanged.emit()


class ButtonDelegate(QStyledItemDelegate):
    """
    A custom delegate for rendering buttons in specific columns of a QTableView.

    Attributes:
    - sudoku_picker (SudokuPicker): Reference to the parent SudokuPicker widget.

    Methods:
    - paint(painter, option, index): Renders the item specified by index using the given painter and style options.
    - editorEvent(event, model, option, index): Processes events for the item specified by index.
    - get_path_for_icon(index): Returns the path for the icon based on the column index.
    - _drawButton(painter, option, index): Draws a button at the specified index.
    - _handleStartButtonClick(model, index): Handles the click event for the Start button.
    - _handleResetButtonClick(model, index): Handles the click event for the Reset button.
    - _handleDeleteButtonClick(model, index): Handles the click event for the Delete button.
    """

    def __init__(self, sudoku_picker, parent=None):
        """
        Initializes the ButtonDelegate with the given SudokuPicker reference.

        Args:
        - sudoku_picker (SudokuPicker): Reference to the parent SudokuPicker widget.
        """
        super().__init__(parent)
        self.sudoku_picker = sudoku_picker

    def paint(self, painter, option, index):
        """
        Renders the item specified by index using the given painter and style options.

        Args:
        - painter (QPainter): Painter object used for rendering.
        - option (QStyleOptionViewItem): Style options for the item view.
        - index (QModelIndex): Index of the item to render.
        """
        if self.sudoku_picker.model.sudoku_data and index.column() >= 7:
            self._drawButton(painter, option, index)
        else:
            super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        """
        Processes events for the item specified by index.

        Args:
        - event (QEvent): Event to process.
        - model (QAbstractItemModel): Model containing the data.
        - option (QStyleOptionViewItem): Style options for the item view.
        - index (QModelIndex): Index of the item to process.

        Returns:
        - bool: True if the event was processed; otherwise False.
        """
        if not model.sudoku_data:
            return False 

        if event.type() == QMouseEvent.MouseButtonRelease and index.column() == 7:
            self._handleStartButtonClick(model, index)
        elif event.type() == QMouseEvent.MouseButtonRelease and index.column() == 8:
            self._handleResetButtonClick(model, index)
        elif event.type() == QMouseEvent.MouseButtonRelease and index.column() == 9:
            self._handleDeleteButtonClick(model, index)
        return super().editorEvent(event, model, option, index)

    def get_path_for_icon(self, index):
        """
        Returns the path for the icon based on the column index.

        Args:
        - index (QModelIndex): Index of the item.

        Returns:
        - str: Path to the icon file.
        """
        base_path = os.path.abspath(os.path.join("constants", "resources"))
        icons = ["play.png", "reset.png", "delete.png"]
        if 7 <= index.column() <= 9:
            return os.path.join(base_path, icons[index.column() - 7])
        return "Button"

    def _drawButton(self, painter, option, index):
        """
        Draws a button at the specified index.

        Args:
        - painter (QPainter): Painter object used for drawing.
        - option (QStyleOptionViewItem): Style options for the item view.
        - index (QModelIndex): Index of the item to draw the button.
        """
        button_rect = option.rect
        sudoku_data = self.get_path_for_icon(index)
        if sudoku_data and os.path.isfile(sudoku_data):
            button_icon = QPixmap(sudoku_data)
            button_icon = button_icon.scaled(button_rect.size(), Qt.KeepAspectRatio)
            button_icon_rect = button_icon.rect()
            button_icon_rect.moveCenter(button_rect.center())
            painter.drawPixmap(button_icon_rect, button_icon)
        else:
            button_text = sudoku_data if isinstance(sudoku_data, str) else 'Button'
            painter.drawText(button_rect, Qt.AlignCenter, button_text)

    def _handleStartButtonClick(self, model, index):
        """
        Handles the click event for the Start button.

        Args:
        - model (QAbstractItemModel): Model containing the data.
        - index (QModelIndex): Index of the Start button item.
        """
        data = model.sudoku_data[index.row()]
        sudoku_id = data[0]
        self.sudoku_picker.open_sudoku(sudoku_id)

    def _handleResetButtonClick(self, model, index):
        """
        Handles the click event for the Reset button.

        Displays a confirmation dialog asking the user if they are sure they want to reset the Sudoku.
        If confirmed, retrieves the Sudoku ID from the model based on the clicked index, resets the Sudoku
        data in the database, and updates the displayed data in the SudokuPicker.

        Args:
        - model (QAbstractItemModel): Model containing the Sudoku data.
        - index (QModelIndex): Index of the Reset button item.
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Confirmation")
        msg_box.setText("Are you sure you want to reset?")
        
        yes_button = msg_box.addButton("Yes", QMessageBox.YesRole)
        no_button = msg_box.addButton("No", QMessageBox.NoRole)

        msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            data = model.sudoku_data[index.row()]
            sudoku_id = data[0]
            resetUsersSudoku(self.sudoku_picker.user_id, sudoku_id)
            self.sudoku_picker.update_data()

    def _handleDeleteButtonClick(self, model, index):
        """
        Handles the click event for the Delete button.

        Displays a confirmation dialog asking the user if they are sure they want to delete the Sudoku.
        If confirmed, retrieves the Sudoku ID from the model based on the clicked index, deletes the Sudoku
        data from the database, and updates the displayed data in the SudokuPicker.

        Args:
        - model (QAbstractItemModel): Model containing the Sudoku data.
        - index (QModelIndex): Index of the Delete button item.
        """
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Confirmation")
        msg_box.setText("Are you sure you want to delete?")
        
        yes_button = msg_box.addButton("Yes", QMessageBox.YesRole)
        no_button = msg_box.addButton("No", QMessageBox.NoRole)

        msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            data = model.sudoku_data[index.row()]
            sudoku_id = data[0]
            deleteUsersSudoku(self.sudoku_picker.user_id, sudoku_id)
            self.sudoku_picker.update_data()


class SudokuPicker(QWidget):
    """
    Widget for displaying a table of Sudoku data with interactive buttons.

    Attributes:
    - user_id (int): User ID associated with the Sudoku data.
    - model (SudokuModel): Model containing the Sudoku data.
    - table_view (QTableView): Table view widget for displaying Sudoku data.
    - app: Reference to the parent application.

    Methods:
    - _setupUI(): Sets up the user interface for the SudokuPicker widget.
    - _initializeModel(): Initializes the SudokuModel and sets it to the table view.
    - _initializeView(): Configures the table view with sorting and item delegate.
    - _setWindowSize(): Adjusts the size of the widget based on the table view's dimensions.
    - open_sudoku(sudoku_id): Opens a Sudoku game application for the specified Sudoku ID.
    - update_data(): Updates the Sudoku data in the model and adjusts the table view's size.
    """

    def __init__(self, user_id):
        """
        Initializes the SudokuPicker widget with the given user ID.

        Args:
        - user_id (int): User ID associated with the Sudoku data.
        """
        super().__init__()
        self.user_id = user_id
        self._setupUI()
        self.app = None

    def _setupUI(self):
        """
        Sets up the user interface for the SudokuPicker widget.
        - Creates a vertical layout and adds a QTableView to it.
        - Initializes the model, configures the view, and adjusts the window size.
        """
        self.layout = QVBoxLayout(self)
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)
        self._initializeModel()
        self._initializeView()
        self._setWindowSize()

    def _initializeModel(self):
        """
        Initializes the SudokuModel with the current user ID and sets it to the table view.
        """
        self.model = SudokuModel(self.user_id)
        self.table_view.setModel(self.model)

    def _initializeView(self):
        """
        Configures the table view with sorting enabled and sets a custom item delegate (ButtonDelegate) for interaction.
        """
        self.table_view.setSortingEnabled(True)
        self.table_view.setItemDelegate(ButtonDelegate(self))
        self.table_view.resizeColumnsToContents()

    def _setWindowSize(self):
        """
        Adjusts the widget's size based on the dimensions of the table view.
        """
        table_width = self.table_view.horizontalHeader().length() + 30
        self.resize(table_width, 400)
        self.setContentsMargins(0,0,0,0)

    def open_sudoku(self, sudoku_id):
        """
        Opens a Sudoku game application for the specified Sudoku ID.

        Args:
        - sudoku_id (int): ID of the Sudoku game to open.
        """
        self.cams = sudoku_app(self.user_id, sudoku_id, self)
        self.cams.show()
        self.cams.setWindowTitle(f"User: {get_username_from_id(self.user_id)} - Sudoku ID: {sudoku_id}")
        self.app.hide()

    def update_data(self):
        """
        Updates the Sudoku data in the model and adjusts the table view's size accordingly.
        """
        self.model.update_data()
        self.table_view.resizeColumnsToContents()
        self._setWindowSize()
