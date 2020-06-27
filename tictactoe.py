from random import choice


class TicTacToe:
    f = " " * 9  # Field in string
    p = [0, 0]   # Players (0 - user, 1-2-3 - ai easy-med-hard)
    free = 9     # Available cells on the field
    pn = 0       # Player number
    tag = ("X", "O")
    params = ("user", "easy", "medium", "hard")

    def __init__(self, f_str="_" * 9):
        self.f = f_str.replace("_", " ")
        self.free = self.f.count(" ")

    def __repr__(self):
        return f"""{"-" * 9}
| {" ".join(c for c in self.f[0:3])} |
| {" ".join(c for c in self.f[3:6])} |
| {" ".join(c for c in self.f[6:9])} |
{"-" * 9}"""

    def ind(self, x, y):
        return x - 1 + (3 - y) * 3

    def test_move(self, f, i, pn):
        f = f[:i] + self.tag[pn] + f[i+1:]
        return f

    def make_move(self, i):
        if self.p[self.pn] > 0:
            print(f'Making move level "{self.params[self.p[self.pn]]}"')
        self.f = self.f[:i] + self.tag[self.pn] + self.f[i+1:]
        self.free -= 1
        self.pn = not self.pn
        print(self)

    def check_input(self, c):
        if not c.replace(" ", "").isdecimal():
            print("You should enter numbers!")
            return False
        elif not (c[0] in "123" and c[-1] in "123"):
            print("Coordinates should be from 1 to 3!")
            return False
        return True

    def user_move(self):
        while True:
            c = input("Enter the coordinates: ")
            if self.check_input(c):
                x, y = int(c[0]), int(c[-1])
                if self.f[self.ind(x, y)] != " ":
                    print("This cell is occupied! Choose another one!")
                else:
                    break
        self.make_move(self.ind(x, y))

    def free_cells(self, f):
        free_cells = []
        [free_cells.append(i) for i in range(9) if f[i] == " "]
        return free_cells

    def ai_easy_move(self):
        self.make_move(choice(self.free_cells(self.f)))

    def ai_medium_move(self):
        free_cells = self.free_cells(self.f)
        for ind in free_cells:
            if self.check_win(self.test_move(self.f, ind, self.pn)):
                self.make_move(ind)
                return None
        for ind in free_cells:
            if self.check_win(self.test_move(self.f, ind, not self.pn)):
                self.make_move(ind)
                return None
        self.ai_easy_move()

    def ai_minimax(self, f):
        class Move:
            index = None
            score = 0

            def __init__(self, score, index=None):
                self.score = score
                self.index = index

        pn = f.count("X") > f.count("O")
        if self.check_win(f):
            return Move(1) if pn == self.pn else Move(-1)
        free_cells = self.free_cells(f)
        if not free_cells:
            return Move(0)
        moves = []
        for cell in free_cells:
            m = self.ai_minimax(self.test_move(f, cell, pn))
            m.index = cell
            moves.append(m)
        max_ = moves[0]
        min_ = moves[0]
        for m in moves:
            if m.score > max_.score:
                max_ = m
            if m.score < min_.score:
                min_ = m
        return max_ if pn != self.pn else min_

    def ai_hard_move(self):
        self.make_move(self.ai_minimax(self.f).index)

    def check_win(self, fs):
        lines = ('012', '345', '678', '630', '741', '852', '642', '048')
        for line in lines:
            fline = fs[int(line[0])] + fs[int(line[1])] + fs[int(line[2])]
            if len(set(fline)) == 1 and fline[0] != " ":
                return True
        return False

    def game(self):
        print(self)
        while not self.check_win(self.f) and self.free > 0:
            if self.p[self.pn] == 0:
                self.user_move()
            elif self.p[self.pn] == 1:
                self.ai_easy_move()
            elif self.p[self.pn] == 2:
                self.ai_medium_move()
            else:
                self.ai_hard_move()
        if self.check_win(self.f):
            print(self.tag[not self.pn] + " wins")
        else:
            print("Draw")

    def menu(self):
        cmd = input("Input command: ").split()
        if cmd[0] == "exit":
            return None
        elif len(cmd) != 3 or cmd[0] != "start" or cmd[1] not in self.params or cmd[2] not in self.params:
            print("Bad parameters!")
            self.menu()
        else:
            self.p[0] = self.params.index(cmd[1])
            self.p[1] = self.params.index(cmd[2])
            self.game()


ttt = TicTacToe()  # "O XX X OO"
ttt.menu()
