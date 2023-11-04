from random import randint


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Cell:
    def __init__(self, around_mines: int, mine: bool, *args, fl_open= False):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = fl_open
        self.flag = False


class GamePole:
    def __init__(self, N: int, M: int):
        self.N = N
        self.M = M
        self.flags_available = M
        if M > N * N:
            exit('too many mines')
        self.__init()

    def __fill_up_the_pole(self):
        self.__secret = []
        count = self.M
        while count:
            row = randint(0, self.N - 1)
            col = randint(0, self.N - 1)
            a = self.pole[row][col]
            if not a.mine:
                a.mine = True
                count -= 1
                self.__secret.append(tuple([row, col])) #row - 1, col - 1
        index = (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)
        for row, col in self.__secret:
            for i, j in index:
                if 0 <= row + i < self.N and 0 <= col + j < self.N:
                    if not self.pole[row + i][col + j].mine:
                        self.pole[row + i][col + j].around_mines += 1


    def __init(self):
        self.pole = [[Cell(0, False, False) for i in range(self.N)] for j in range(self.N)]  # N + 2
        self.__fill_up_the_pole()

    def show(self):
        print(f'{bcolors.OKBLUE} ', end=' ')
        print(*range(self.N), sep=' ')
        k = 0
        for i in self.pole:
            print(f'{bcolors.OKBLUE}{k}', end=' ')
            for j in i:
                print((
                          f'{bcolors.OKCYAN}#{bcolors.ENDC}' if not j.flag else f'{bcolors.FAIL}f{bcolors.ENDC}') if not j.fl_open else (
                    f'{bcolors.OKGREEN}{j.around_mines}{bcolors.ENDC}' if not j.mine else f'{bcolors.FAIL}*{bcolors.ENDC}'),
                      end=' ')
            k += 1
            print()
        print(f'{bcolors.FAIL}flags: {self.flags_available}{bcolors.ENDC}')

    def __is_lose(self, row, col):
        if self.pole[row][col].mine:
            self.__show_all_mines()
            print(f'{bcolors.FAIL}you lost :({bcolors.ENDC}')
            if input('restart? y/n: ').lower() == 'y':
                self.restart()
            else:
                exit('bye ')

    def __show_all_mines(self):
        for i, j in self.__secret:
            self.pole[i][j].fl_open = True
        self.show()

    def restart(self):
        self.__init__(self.N, self.M)

    def player_move(self, row, col):
        self.pole[row][col].fl_open = True
        self.__is_lose(row, col)
        if self.pole[row][col].around_mines == 0:
            self.__zeros_around(row, col)

    def set_flag(self, row, col):
        if not self.flags_available and not self.pole[row][col].flag:
            print('you are out the flags')
        else:
            self.pole[row][col].flag = not self.pole[row][col].flag
            self.flags_available += -1 if self.pole[row][col].flag else 1
            self.__is_win()

    def __is_win(self):
        if all(map(lambda x: self.pole[x[0]][x[1]].flag, self.__secret)):
            exit("YOU WON! :0")

    def exit(self):
        exit('game closed')

    def __zeros_around(self, row, col):
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if (0 <= i < self.N and 0 <= j < self.N) and (not self.pole[i][j].fl_open):
                    self.pole[i][j].fl_open = True
                    if self.pole[i][j].around_mines == 0:
                        self.__zeros_around(i, j)


if __name__ == '__main__':
    # pole_game = GamePole(int(input('pole NxN: ')), int(input('Mines: ')))
    pole_game = GamePole(10, 15)
    print(f'{bcolors.WARNING}# as a closed cell, 0 as a opened one')
    print('restart to restart')
    print(f'exit to exit{bcolors.ENDC}')

    while True:
        pole_game.show()
        N = input(f'{bcolors.WARNING}if you want to set/delete the flag input "f row col", to open new cell "row col": {bcolors.ENDC}').split()
        if all(map(str.isdigit, N)):
            try:
                pole_game.player_move(*map(int, N))
            except (IndexError, TypeError):
                print(f'{bcolors.FAIL}out of pole{bcolors.ENDC}')
        else:
            if N[0] == 'f':
                pole_game.set_flag(*map(int, N[1:]))
            elif N[0] == 'restart':
                pole_game.restart()
            elif N[0] == 'exit':
                pole_game.exit()
