if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = SudokuGUI()

    sudoku = Sudoku()
    top_widget = QWidget()
    bottom_widget = QWidget()

    main_layout = main_window.layout()
    main_layout.addWidget(top_widget)
    main_layout.addWidget(sudoku)
    main_layout.addWidget(bottom_widget)
    sudoku.update_board(get_board_from_db(1))
    app.setStyleSheet(open('style.qss').read())


    cells = sudoku.cells
    for cell_name, cell in cells.items():
        cell.editingFinished.connect(lambda cell=cell: validate_cell_changed_text(cell, sudoku))

    main_window.show()

    sys.exit(app.exec())