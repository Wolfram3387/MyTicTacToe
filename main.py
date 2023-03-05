import sys
from PyQt6 import QtWidgets
from random import choice

from design import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Константы
        self.cross_cell_css = """QPushButton{
                  border:none;
                  background: #272D39 url(resourses/images/cross.png) no-repeat center center;
                }
                QPushButton::hover{
                  background-color: #373D49;
                }"""
        self.cross_win_css = """QPushButton{
                          border:none;
                          background: #272D39 url(resourses/images/cross_win.png) no-repeat center center;
                        }
                        QPushButton::hover{
                          background-color: #373D49;
                        }"""
        self.cross_lose_css = """QPushButton{
                          border:none;
                          background: #272D39 url(resourses/images/cross_lose.png) no-repeat center center;
                        }
                        QPushButton::hover{
                          background-color: #373D49;
                        }"""
        self.zero_cell_css = """QPushButton{
                  border:none;
                  background: #272D39 url(resourses/images/circle.png) no-repeat center center;
                }
                QPushButton::hover{
                  background-color: #373D49;
                }"""
        self.zero_win_css = """QPushButton{
                          border:none;
                          background: #272D39 url(resourses/images/circle_win.png) no-repeat center center;
                        }
                        QPushButton::hover{
                          background-color: #373D49;
                        }"""
        self.zero_lose_css = """QPushButton{
                          border:none;
                          background: #272D39 url(resourses/images/circle_lose.png) no-repeat center center;
                        }
                        QPushButton::hover{
                          background-color: #373D49;
                        }"""
        self.empty_cell_css = """QPushButton{
                          background: #272D39;
                        }
                        QPushButton::hover{
                          background-color: #373D49;
                        }"""
        self.locked_empty_cell_css = """QPushButton{
                                  background: #272D39;
                                }
                                """
        self.green_css = "background-color: rgb(123, 255, 62)"
        self.red_css = "background-color: rgb(237, 96, 74)"
        self.default_color = "background-color: rgb(150, 150, 150)"

        # Переменные
        self.empty_item = ''
        self.player_item = 'X'
        self.computer_item = 'O'
        self.in_game = False
        self.board = [self.empty_item for _ in range(9)]
        self.all_buttons = [
            self.pushButton_1, self.pushButton_2, self.pushButton_3,
            self.pushButton_4, self.pushButton_5, self.pushButton_6,
            self.pushButton_7, self.pushButton_8, self.pushButton_9
        ]

        # Инициализация доски
        self.label.setText('Жми на кнопку "Начать игру"')
        self.pushButton_start.setStyleSheet(self.green_css)
        self.board = [self.empty_item for _ in range(9)]
        for i in range(len(self.all_buttons)):
            self.all_buttons[i].setStyleSheet(self.locked_empty_cell_css)

        # Хендлеры
        for btn in self.all_buttons:
            btn.clicked.connect(self.btn_clicked)
        self.pushButton_start.clicked.connect(self.btn_start_clicked)

    def btn_clicked(self):
        """Обработчик нажатия на игровые кнопки (ход игрока)"""
        if not self.in_game:
            return
        index = self.all_buttons.index(self.sender())
        if self.board[index] != self.empty_item:
            return
        self.all_buttons[index].setStyleSheet(self.cross_cell_css)
        self.board[index] = self.player_item
        self.check_state()
        self.computer_move()

    def computer_move(self):
        """Ход компьютера"""
        if not self.in_game:
            return

        # Если есть победный ход, то делает его
        if self.get_winning_move(self.computer_item) is not None:
            computer_index_choice = self.get_winning_move(self.computer_item)

        # Если есть вынужденный ход, то делает его
        elif self.get_winning_move(self.player_item) is not None:
            computer_index_choice = self.get_winning_move(self.player_item)

        # Иначе: выбирает индекс любой свободной ячейки
        else:
            computer_index_choice = choice([i for i, v in enumerate(self.board) if v == self.empty_item])

        # Вставляет нолик в выбранную ячейку
        self.board[computer_index_choice] = self.computer_item
        self.all_buttons[computer_index_choice].setStyleSheet(self.zero_cell_css)
        self.check_state()

    def btn_start_clicked(self):
        """Начинает или перезапускает игру"""
        self.in_game = True
        self.label.setText('Крестики-нолики')
        self.label.setStyleSheet(self.default_color)
        self.pushButton_start.setText('Сдаться')
        self.pushButton_start.setStyleSheet(self.red_css)
        self.restart_board()

    def restart_board(self):
        """Сбрасывает доску на стартовую позицию"""
        self.board = [self.empty_item for _ in range(9)]
        for i in range(len(self.all_buttons)):
            self.all_buttons[i].setStyleSheet(self.empty_cell_css)

    def get_winning_move(self, item):
        """Возвращает индекс победного хода для игрока, котоорый играет за item"""
        matrix = [
            [self.board[0], self.board[1], self.board[2]],
            [self.board[3], self.board[4], self.board[5]],
            [self.board[6], self.board[7], self.board[8]]
        ]
        # Проверка по строкам
        for i in range(3):
            if matrix[i].count(item) == 2 and matrix[i].count(self.empty_item) == 1:
                print(i * 3 + matrix[i].index(self.empty_item))
                return i * 3 + matrix[i].index(self.empty_item)
        # Проверка по столбцам
        for i in range(3):
            column = [matrix[j][i] for j in range(3)]
            if column.count(item) == 2 and column.count(self.empty_item) == 1:
                print(column.index(self.empty_item) * 3 + i)
                return column.index(self.empty_item) * 3 + i
        # Проверка по главной диагонали
        main_diagonal = [matrix[i][i] for i in range(3)]
        if main_diagonal.count(item) == 2 and main_diagonal.count(self.empty_item) == 1:
            print(main_diagonal.index(self.empty_item) * 4)
            return main_diagonal.index(self.empty_item) * 4
        # Проверка по побочной диагонали
        secondary_diagonal = [matrix[i][2 - i] for i in range(3)]
        if secondary_diagonal.count(item) == 2 and secondary_diagonal.count(self.empty_item) == 1:
            print(secondary_diagonal.index(self.empty_item) * 2 + 2)
            return secondary_diagonal.index(self.empty_item) * 2 + 2

    def get_winning_indices(self):
        """Возвращает индексы победных ячеек"""
        matrix = [
            [self.board[0], self.board[1], self.board[2]],
            [self.board[3], self.board[4], self.board[5]],
            [self.board[6], self.board[7], self.board[8]]
        ]
        for i in range(3):
            if matrix[i][0] == matrix[i][1] == matrix[i][2] != self.empty_cell_css:
                return [i * 3, i * 3 + 1, i * 3 + 2]
        for i in range(3):
            if matrix[0][i] == matrix[1][i] == matrix[2][i] != self.empty_cell_css:
                return [i, 3 + i, 6 + i]
        if matrix[0][0] == matrix[1][1] == matrix[2][2] != self.empty_cell_css:
            return [0, 4, 8]
        if matrix[0][2] == matrix[1][1] == matrix[2][0] != self.empty_cell_css:
            return [2, 4, 6]

    def check_state(self):
        """Проверяет состояние игры"""
        if self.is_win() or self.is_lose():
            if self.is_win():
                icon = self.cross_win_css
                self.label.setText('Победа!')
                self.label.setStyleSheet(self.green_css)
                self.pushButton_start.setStyleSheet(self.green_css)
            elif self.is_lose():
                icon = self.zero_lose_css
                self.label.setText('Поражение!')
                self.label.setStyleSheet(self.red_css)
                self.pushButton_start.setStyleSheet(self.red_css)

            for i in self.get_winning_indices():
                self.all_buttons[i].setStyleSheet(icon)
            self.in_game = False
            self.pushButton_start.setText('Перезапустить игру')

        elif self.is_draw():
            self.label.setText('Ничья!')
            self.in_game = False
            self.pushButton_start.setText('Перезапустить игру')
            self.pushButton_start.setStyleSheet(self.default_color)

    def is_win(self):
        winning_indices = self.get_winning_indices()
        return winning_indices is not None and self.board[winning_indices[0]] == self.player_item

    def is_lose(self):
        winning_indices = self.get_winning_indices()
        return winning_indices is not None and self.board[winning_indices[0]] == self.computer_item

    def is_draw(self):
        return self.empty_item not in self.board and not self.is_win() and not self.is_lose()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
