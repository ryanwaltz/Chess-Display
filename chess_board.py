import pygame
import pathlib

pygame.init()

window = (400, 400)
screen = pygame.display.set_mode(window)
background = pygame.Surface(window)
white_rook = pygame.image.load("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/wr.png")
white_queen = pygame.image.load("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/wq.png")
white_pawn = pygame.image.load("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/wp.png")
white_knight = pygame.image.load("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/wn.png")
white_king = pygame.image.load("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/wk.png")
white_bishop = pygame.image.load("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/wb.png")
black_rook = pygame.image.load("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/br.png")
black_queen = pygame.image.load("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/bq.png")
black_pawn = pygame.image.load("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/bp.png")
black_knight = pygame.image.load("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/bn.png")
black_king = pygame.image.load("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/bk.png")
black_bishop = pygame.image.load("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/bb.png")

white_to_move = True
black_to_move = False
size = 50
white_rook = pygame.transform.smoothscale(white_rook, (size, size))
white_queen = pygame.transform.smoothscale(white_queen, (size, size))
white_pawn = pygame.transform.smoothscale(white_pawn, (size, size))
white_knight = pygame.transform.smoothscale(white_knight, (size, size))
white_king = pygame.transform.smoothscale(white_king, (size, size))
white_bishop = pygame.transform.smoothscale(white_bishop, (size, size))
black_rook = pygame.transform.smoothscale(black_rook, (size, size))
black_queen = pygame.transform.smoothscale(black_queen, (size, size))
black_pawn = pygame.transform.smoothscale(black_pawn, (size, size))
black_knight = pygame.transform.smoothscale(black_knight, (size, size))
black_king = pygame.transform.smoothscale(black_king, (size, size))
black_bishop = pygame.transform.smoothscale(black_bishop, (size, size))

color_variable = 0
color_values = [(255, 255, 255), (87, 87, 87)]

with open("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess games/num_games.txt", "r") as file:
    num_games = int(file.readline())
    num_games += 1
with open("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess games/num_games.txt", "w") as file:
    file.write(str(num_games))
    print(num_games)
chess_path = f"/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess games/Chess_{num_games}.pgn"
pathlib.Path(chess_path).touch()


x = 400 / 8  # this equals 57 and is the size we use to get the chessboard
values = []
i = 0
while True:
    values.append(int(x * i))
    i += 1
    if i == 8:
        break

for i in values:
    for ii in values:
        pygame.draw.rect(background, color_values[color_variable], (int(i), int(ii), 57, 57))
        screen.blit(background, (0, 0))
        if color_variable == 0:
            color_variable += 1
        else:
            color_variable -= 1
    if color_variable == 0:
        color_variable += 1
    else:
        color_variable -= 1
pygame.display.flip()


def get_correct_pos_per_square(x_pos, y_pos):  # these start from top left. This is due to pygame being annoying
    global size
    return [(x_pos * size - size), (y_pos * size - size)]


class Pawn(object):

    def __init__(self, pos_x, pos_y, color):
        self.pos = [pos_x, pos_y]
        self.color = color
        if color:
            self.image = white_pawn
            self.image_type = "white_pawn"
        else:
            self.image = black_pawn
            self.image_type = "black_pawn"
        self.hide = False
        self.can_en_passant = False

    def get_legal_moves(self, new_x_pos, new_y_pos):
        global white_to_move, black_to_move
        if self.color is not white_to_move:
            return False
        try:
            change_in_y = abs(self.pos[1] - new_y_pos)
            if self.pos[0] == new_x_pos:
                pass
            else:
                if self.color:
                    if abs(self.pos[0] - new_x_pos) == 1 and self.pos[1] - new_y_pos == 1:
                        for piece in black_pieces:
                            if piece.pos == [new_x_pos, new_y_pos]:
                                if new_y_pos == 8 or new_y_pos == 1:
                                    self.pos = [new_x_pos, new_y_pos]
                                    for new_piece in total_pieces:
                                        if new_piece.pos == self.pos:
                                            if new_piece.color is False:
                                                new_piece.delete_piece()
                                    self.Promotion()
                                    white_to_move = not white_to_move
                                    black_to_move = not black_to_move
                                    return False
                                return True
                else:
                    if abs(self.pos[0] - new_x_pos) == 1 and self.pos[1] - new_y_pos == -1:
                        for piece in white_pieces:
                            if piece.pos == [new_x_pos, new_y_pos]:
                                if new_y_pos == 8 or new_y_pos == 1:
                                    self.pos = [new_x_pos, new_y_pos]
                                    for new_piece in total_pieces:
                                        if new_piece.pos == self.pos:
                                            if new_piece.color is True:
                                                new_piece.delete_piece()
                                    self.Promotion()
                                    white_to_move = not white_to_move
                                    black_to_move = not black_to_move
                                    return False
                                return True
                return False
            if self.color:
                if self.pos[1] == 7:
                    if change_in_y <= 2:
                        pass
                    else:
                        return False

                    pass  # this means that you are able to go two squares
                else:
                    if change_in_y == 1:
                        pass
                    else:
                        return False
            else:
                if self.pos[1] == 2:
                    if change_in_y <= 2:
                        pass
                    else:
                        return False
                else:
                    if change_in_y == 1:
                        pass
                    else:
                        return False
            current_y = self.pos[1]
            if self.color:
                while True:
                    current_y -= 1
                    for piece in total_pieces:
                        if piece.pos == [self.pos[0], current_y]:
                            return False
                    if current_y == new_y_pos:
                        break

            else:
                while True:
                    current_y += 1
                    for piece in total_pieces:
                        if piece.pos == [self.pos[0], current_y]:
                            return False
                    if current_y == new_y_pos:
                        break
            if new_y_pos == 8 or new_y_pos == 1:
                self.pos = [new_x_pos, new_y_pos]
                self.Promotion()
                white_to_move = not white_to_move
                black_to_move = not black_to_move
                return False
            return True
        except KeyboardInterrupt:
            return False

    def Promotion(self, piece_type="Q"):
        if self.color:
            if piece_type == "Q":
                white_pieces.append(Queen(self.pos[0], self.pos[1], self.color))
            elif piece_type == "K":
                white_pieces.append(Knight(self.pos[0], self.pos[1], self.color))
            elif piece_type == "B":
                square_color = self.pos[0] + self.pos[1]
                if square_color % 2 == 1:
                    square_color = False
                else:
                    square_color = True
                white_pieces.append(Bishop(self.pos[0], self.pos[1], self.color, square_color))
            elif piece_type == "R":
                white_pieces.append(Rook(self.pos[0], self.pos[1], self.color))
            total_pieces.append(white_pieces[-1])
            white_pieces[-1].blit_object()
            white_pieces.remove(self)
        else:
            if piece_type == "Q":
                black_pieces.append(Queen(self.pos[0], self.pos[1], self.color))
            elif piece_type == "K":
                black_pieces.append(Knight(self.pos[0], self.pos[1], self.color))
            elif piece_type == "B":
                square_color = self.pos[0] + self.pos[1]
                if square_color % 2 == 1:
                    square_color = False
                else:
                    square_color = True
                black_pieces.append(Bishop(self.pos[0], self.pos[1], self.color, square_color))
            elif piece_type == "R":
                black_pieces.append(Rook(self.pos[0], self.pos[1], self.color))
            total_pieces.append(black_pieces[-1])
            black_pieces[-1].blit_object()
            black_pieces.remove(self)
        total_pieces.remove(self)
        pygame.display.update()

    def blit_object(self):
        if self.hide is False:
            screen.blit(self.image, get_correct_pos_per_square(self.pos[0], self.pos[1]))

    def delete_piece(self):
        try:
            total_pieces.remove(self)
            if self.color:
                white_pieces.remove(self)
            else:
                black_pieces.remove(self)
        except ValueError:
            pass


class Rook(object):

    def __init__(self, pos_x, pos_y, color):
        self.has_moved = False
        self.pos = [pos_x, pos_y]
        if color:
            self.image = white_rook
            self.image_type = "Rook"
        else:
            self.image = black_rook
            self.image_type = "Rook"
        self.hide = False
        self.color = color

    def get_legal_moves(self, new_x_pos, new_y_pos):
        if self.color is not white_to_move:
            return False
        try:
            if new_x_pos == self.pos[0] or new_y_pos == self.pos[1]:
                pass
            else:
                return False

            if new_x_pos == self.pos[0]:
                check_pos = self.pos[1]
                if new_y_pos > self.pos[1]:
                    increment = 1
                else:
                    increment = -1
                while True:
                    check_pos += increment
                    if check_pos == new_y_pos:
                        break
                    for piece in total_pieces:
                        if piece.pos == [self.pos[0], check_pos]:
                            return False
            else:
                check_pos = self.pos[0]
                if new_x_pos > self.pos[0]:
                    increment = 1
                else:
                    increment = -1
                while True:
                    check_pos += increment
                    if check_pos == new_x_pos:
                        break
                    for piece in total_pieces:
                        if piece.pos == [check_pos, self.pos[1]]:
                            return False
            self.has_moved = True
            return True
        except KeyboardInterrupt:
            return False

    def blit_object(self):
        if self.hide is False:
            screen.blit(self.image, get_correct_pos_per_square(self.pos[0], self.pos[1]))

    def delete_piece(self):
        try:
            total_pieces.remove(self)
            if self.color:
                white_pieces.remove(self)
            else:
                black_pieces.remove(self)
        except ValueError:
            pass


class Knight(object):

    def __init__(self, pos_x, pos_y, color):
        self.pos = [pos_x, pos_y]
        if color:
            self.image = white_knight
            self.image_type = "Knight"
        else:
            self.image = black_knight
            self.image_type = "Knight"
        self.hide = False
        self.color = color

    def get_legal_moves(self, new_x_pos, new_y_pos):
        if new_x_pos == self.pos[0] or new_y_pos == self.pos[1]:
            return False
        if self.color is not white_to_move:
            return False
        try:
            change_in_x = abs(self.pos[0] - new_x_pos)
            change_in_y = abs(self.pos[1] - new_y_pos)
            if change_in_y == change_in_x:
                return False
            if change_in_y + change_in_x != 3:
                return False

            return True
        except KeyboardInterrupt:
            return False

    def blit_object(self):
        if self.hide is False:
            screen.blit(self.image, get_correct_pos_per_square(self.pos[0], self.pos[1]))

    def delete_piece(self):
        try:
            total_pieces.remove(self)
            if self.color:
                white_pieces.remove(self)
            else:
                black_pieces.remove(self)
        except ValueError:
            pass


class Bishop(object):

    def __init__(self, pos_x, pos_y, color, color_of_squares):
        self.pos = [pos_x, pos_y]
        if color:
            self.image = white_bishop
            self.image_type = "Bishop"
        else:
            self.image = black_bishop
            self.image_type = "Bishop"
        self.hide = False
        self.color = color
        self.color_of_squares = color_of_squares

    def get_legal_moves(self, new_x_pos, new_y_pos):
        if self.color is not white_to_move:
            return False
        try:
            change_in_x = abs(new_x_pos - self.pos[0])
            change_in_y = abs(new_y_pos - self.pos[1])
            check_x_pos = self.pos[0]
            check_y_pos = self.pos[1]
            if new_x_pos > self.pos[0]:
                x_increment = 1
            else:
                x_increment = -1
            if new_y_pos > self.pos[1]:
                y_increment = 1
            else:
                y_increment = -1
            while True:
                check_x_pos += x_increment
                check_y_pos += y_increment
                if check_x_pos == new_x_pos:
                    break
                for piece in total_pieces:
                    if piece.pos == [check_x_pos, check_y_pos]:
                        return False

            if change_in_x == change_in_y:
                pass
            else:
                return False

            return True
        except KeyboardInterrupt:
            return False

    def blit_object(self):
        if self.hide is False:
            screen.blit(self.image, get_correct_pos_per_square(self.pos[0], self.pos[1]))

    def delete_piece(self):
        try:
            total_pieces.remove(self)
            if self.color:
                white_pieces.remove(self)
            else:
                black_pieces.remove(self)
        except ValueError:
            pass


class Queen(object):

    def __init__(self, pos_x, pos_y, color):
        self.pos = [pos_x, pos_y]
        if color:
            self.image = white_queen
            self.image_type = "Queen"
        else:
            self.image = black_queen
            self.image_type = "Queen"
        self.hide = False
        self.color = color

    def get_legal_moves(self, new_x_pos, new_y_pos):
        if self.color is not white_to_move:
            return False
        try:
            if new_x_pos == self.pos[0] or new_y_pos == self.pos[1]:  # Rook code
                if new_x_pos == self.pos[0] or new_y_pos == self.pos[1]:
                    pass
                else:
                    return False

                if new_x_pos == self.pos[0]:  # Rook Code
                    check_pos = self.pos[1]
                    if new_y_pos > self.pos[1]:
                        increment = 1
                    else:
                        increment = -1
                    while True:
                        check_pos += increment
                        if check_pos == new_y_pos:
                            break
                        for piece in total_pieces:
                            if piece.pos == [self.pos[0], check_pos]:
                                return False
                else:
                    check_pos = self.pos[0]
                    if new_x_pos > self.pos[0]:
                        increment = 1
                    else:
                        increment = -1
                    while True:
                        check_pos += increment
                        if check_pos == new_x_pos:
                            break
                        for piece in total_pieces:
                            if piece.pos == [check_pos, self.pos[1]]:
                                return False
                return True
            else:
                change_in_x = abs(new_x_pos - self.pos[0])  # Bishop code
                change_in_y = abs(new_y_pos - self.pos[1])
                check_x_pos = self.pos[0]
                check_y_pos = self.pos[1]
                if new_x_pos > self.pos[0]:
                    x_increment = 1
                else:
                    x_increment = -1
                if new_y_pos > self.pos[1]:
                    y_increment = 1
                else:
                    y_increment = -1
                while True:
                    check_x_pos += x_increment
                    check_y_pos += y_increment
                    if check_x_pos == new_x_pos:
                        break
                    for piece in total_pieces:
                        if piece.pos == [check_x_pos, check_y_pos]:
                            return False

                if change_in_x == change_in_y:
                    pass
                else:
                    return False
                return True
        except KeyboardInterrupt:
            return False

    def blit_object(self):
        if self.hide is False:
            screen.blit(self.image, get_correct_pos_per_square(self.pos[0], self.pos[1]))

    def delete_piece(self):
        try:
            total_pieces.remove(self)
            if self.color:
                white_pieces.remove(self)
            else:
                black_pieces.remove(self)
        except ValueError:
            pass


class King(object):

    def __init__(self, pos_x, pos_y, color):
        self.pos = [pos_x, pos_y]
        if color:
            self.image = white_king
            self.image_type = "King"
        else:
            self.image = black_king
            self.image_type = "King"
        self.hide = False
        self.color = color
        self.has_moved = False

    def get_legal_moves(self, new_x_pos, new_y_pos):
        global white_to_move, black_to_move
        old_pos = self.pos
        if self.color is not white_to_move:
            return False
        try:
            change_in_x = abs(new_x_pos - self.pos[0])
            change_in_y = abs(new_y_pos - self.pos[1])
            if change_in_y <= 1 and change_in_x <= 1:  # Queen code + not letting it get to far away
                pass
            else:
                if self.has_moved:
                    return False
                else:
                    if self.color:
                        if new_x_pos == 7 and new_y_pos == 8:  # short castle code
                            for piece in total_pieces:
                                if piece.pos == [6, 8] or piece.pos == [7, 8]:
                                    return False
                            white_to_move = not white_to_move
                            black_to_move = not black_to_move
                            self.pos = [6, 8]
                            if self.is_in_check()[0]:
                                self.pos = old_pos
                                return False
                            self.pos = [7, 8]
                            if self.is_in_check()[0]:
                                self.pos = old_pos
                                return False
                            self.pos = old_pos
                            white_to_move = not white_to_move
                            black_to_move = not black_to_move
                            if white_king_rook.has_moved is False:
                                white_king_king.pos = [new_x_pos, new_y_pos]
                                white_king_king.blit_object()
                                white_king_rook.pos = [6, 8]
                                white_king_rook.blit_object()
                                white_to_move = not white_to_move
                                black_to_move = not black_to_move
                                white_king_king.has_moved = True
                            else:
                                return False
                        elif new_x_pos == 3 and new_y_pos == 8:  # long castle code
                            for piece in total_pieces:
                                if piece.pos == [2, 8] or piece.pos == [3, 8] or piece.pos == [4, 8]:
                                    return False
                            white_to_move = not white_to_move
                            black_to_move = not black_to_move
                            self.pos = [2, 8]
                            if self.is_in_check()[0]:
                                self.pos = old_pos
                                return False
                            self.pos = [3, 8]
                            if self.is_in_check()[0]:
                                self.pos = old_pos
                                return False
                            self.pos = [4, 8]
                            if self.is_in_check()[0]:
                                self.pos = old_pos
                                return False
                            self.pos = old_pos
                            white_to_move = not white_to_move
                            black_to_move = not black_to_move
                            if white_queen_rook.has_moved is False:
                                white_king_king.pos = [new_x_pos, new_y_pos]
                                white_queen_rook.pos = [4, 8]
                                white_to_move = not white_to_move
                                black_to_move = not black_to_move
                                white_king_king.has_moved = True
                        else:
                            return False
                    else:
                        if new_x_pos == 7 and new_y_pos == 1:
                            for piece in total_pieces:
                                if piece.pos == [6, 1] or piece.pos == [7, 1]:
                                    return False
                            white_to_move = not white_to_move
                            black_to_move = not black_to_move
                            self.pos = [6, 1]
                            if self.is_in_check()[0]:
                                self.pos = old_pos
                                return False
                            self.pos = [7, 1]
                            if self.is_in_check()[0]:
                                self.pos = old_pos
                                return False
                            self.pos = old_pos
                            white_to_move = not white_to_move
                            black_to_move = not black_to_move
                            if black_king_rook.has_moved is False:
                                black_king_king.pos = [new_x_pos, new_y_pos]
                                black_king_rook.pos = [6, 1]
                                white_to_move = not white_to_move
                                black_to_move = not black_to_move
                                black_king_king.has_moved = True
                        elif new_x_pos == 3 and new_y_pos == 1:
                            for piece in total_pieces:
                                if piece.pos == [2, 1] or piece.pos == [3, 1] or piece.pos == [4, 1]:
                                    return False
                            white_to_move = not white_to_move
                            black_to_move = not black_to_move
                            self.pos = [2, 1]
                            if self.is_in_check()[0]:
                                self.pos = old_pos
                                return False
                            self.pos = [3, 1]
                            if self.is_in_check()[0]:
                                self.pos = old_pos
                                return False
                            self.pos = [4, 1]
                            if self.is_in_check()[0]:
                                self.pos = old_pos
                                return False
                            self.pos = old_pos
                            white_to_move = not white_to_move
                            black_to_move = not black_to_move
                            if black_queen_rook.has_moved is False:
                                black_king_king.pos = [new_x_pos, new_y_pos]
                                black_queen_rook.pos = [4, 1]
                                white_to_move = not white_to_move
                                black_to_move = not black_to_move
                                black_king_king.has_moved = True
                                return False
                        else:
                            return False

            if new_x_pos == self.pos[0] or new_y_pos == self.pos[1]:  # Rook code
                if new_x_pos == self.pos[0] or new_y_pos == self.pos[1]:
                    pass
                else:
                    return False

                if new_x_pos == self.pos[0]:  # Rook Code
                    check_pos = self.pos[1]
                    if new_y_pos > self.pos[1]:
                        increment = 1
                    else:
                        increment = -1
                    while True:
                        check_pos += increment
                        if check_pos == new_y_pos:
                            break
                        for piece in total_pieces:
                            if piece.pos == [self.pos[0], check_pos]:
                                return False
                else:
                    check_pos = self.pos[0]
                    if new_x_pos > self.pos[0]:
                        increment = 1
                    else:
                        increment = -1
                    while True:
                        check_pos += increment
                        if check_pos == new_x_pos:
                            break
                        for piece in total_pieces:
                            if piece.pos == [check_pos, self.pos[1]]:
                                return False
                self.has_moved = True
                return True
            else:
                change_in_x = abs(new_x_pos - self.pos[0])  # Bishop code
                change_in_y = abs(new_y_pos - self.pos[1])
                check_x_pos = self.pos[0]
                check_y_pos = self.pos[1]
                if new_x_pos > self.pos[0]:
                    x_increment = 1
                else:
                    x_increment = -1
                if new_y_pos > self.pos[1]:
                    y_increment = 1
                else:
                    y_increment = -1
                while True:
                    check_x_pos += x_increment
                    check_y_pos += y_increment
                    if check_x_pos == new_x_pos:
                        break
                    for piece in total_pieces:
                        if piece.pos == [check_x_pos, check_y_pos]:
                            return False

                if change_in_x == change_in_y:
                    pass
                else:
                    return False
                self.has_moved = True
                return True
        except KeyboardInterrupt:
            return False

    def is_in_check(self, new_x=False, new_y=False):
        if new_x and new_y:
            old_x = self.pos[0]
            old_y = self.pos[1]
            self.pos[0] = new_x
            self.pos[1] = new_y
        if self.color:
            for piece in black_pieces:
                if piece.get_legal_moves(self.pos[0], self.pos[1]):
                    return [True, piece]
        else:
            for piece in white_pieces:
                if piece.get_legal_moves(self.pos[0], self.pos[1]):
                    return [True, piece]
        if new_x and new_y:
            # noinspection PyUnboundLocalVariable
            self.pos[0] = old_x
            # noinspection PyUnboundLocalVariable
            self.pos[1] = old_y
        return [False]

    def blit_object(self):
        if self.hide is False:
            screen.blit(self.image, get_correct_pos_per_square(self.pos[0], self.pos[1]))

    def delete_piece(self):
        try:
            total_pieces.remove(self)
            if self.color:
                white_pieces.remove(self)
            else:
                black_pieces.remove(self)
        except ValueError:
            pass


def set_up_board_in_starting_config():
    redraw_board()
    screen.blit(white_rook, get_correct_pos_per_square(1, 8))
    screen.blit(white_pawn, get_correct_pos_per_square(1, 7))
    screen.blit(white_knight, get_correct_pos_per_square(2, 8))
    screen.blit(white_pawn, get_correct_pos_per_square(2, 7))
    screen.blit(white_bishop, get_correct_pos_per_square(3, 8))
    screen.blit(white_pawn, get_correct_pos_per_square(3, 7))
    screen.blit(white_queen, get_correct_pos_per_square(4, 8))
    screen.blit(white_pawn, get_correct_pos_per_square(4, 7))
    screen.blit(white_king, get_correct_pos_per_square(5, 8))
    screen.blit(white_pawn, get_correct_pos_per_square(5, 7))
    screen.blit(white_bishop, get_correct_pos_per_square(6, 8))
    screen.blit(white_pawn, get_correct_pos_per_square(6, 7))
    screen.blit(white_knight, get_correct_pos_per_square(7, 8))
    screen.blit(white_pawn, get_correct_pos_per_square(7, 7))
    screen.blit(white_rook, get_correct_pos_per_square(8, 8))
    screen.blit(white_pawn, get_correct_pos_per_square(8, 7))
    screen.blit(black_rook, get_correct_pos_per_square(1, 1))
    screen.blit(black_pawn, get_correct_pos_per_square(1, 2))
    screen.blit(black_knight, get_correct_pos_per_square(2, 1))
    screen.blit(black_pawn, get_correct_pos_per_square(2, 2))
    screen.blit(black_bishop, get_correct_pos_per_square(3, 1))
    screen.blit(black_pawn, get_correct_pos_per_square(3, 2))
    screen.blit(black_queen, get_correct_pos_per_square(4, 1))
    screen.blit(black_pawn, get_correct_pos_per_square(4, 2))
    screen.blit(black_king, get_correct_pos_per_square(5, 1))
    screen.blit(black_pawn, get_correct_pos_per_square(5, 2))
    screen.blit(black_bishop, get_correct_pos_per_square(6, 1))
    screen.blit(black_pawn, get_correct_pos_per_square(6, 2))
    screen.blit(black_knight, get_correct_pos_per_square(7, 1))
    screen.blit(black_pawn, get_correct_pos_per_square(7, 2))
    screen.blit(black_rook, get_correct_pos_per_square(8, 1))
    screen.blit(black_pawn, get_correct_pos_per_square(8, 2))
    pygame.display.update()


def redraw_board():
    color_variable = 0
    color_values = [(255, 255, 255), (87, 87, 87)]

    x = 400 / 8  # this equals 57 and is the size we use to get the chessboard
    values = []
    i = 0
    while True:
        values.append(int(x * i))
        i += 1
        if i == 8:
            break

    for i in values:
        for ii in values:
            pygame.draw.rect(background, color_values[color_variable], (int(i), int(ii), 57, 57))
            if color_variable == 0:
                color_variable += 1
            else:
                color_variable -= 1
        if color_variable == 0:
            color_variable += 1
        else:
            color_variable -= 1
    screen.blit(background, (0, 0))


def return_coordinates_from_pos(x, y):
    return [int(x/50)+1, int(y/50)+1]


def start_drag(x, y):  # pass the right piece through to the others for the starter.
    coordinates = return_coordinates_from_pos(x, y)
    for piece in total_pieces:
        if piece.pos == coordinates:
            return piece


def dragging_piece(x, y, piece):  # This is for when the piece is actually being dragged around the screen
    screen.blit(piece.image, (x - 25, y - 25))


class PGN(object):
    x_list = ["a", "b", "c", "d", "e", "f", "g", "h"]
    piece_list = ["R", "N", "B", "Q", "K"]

    def __init__(self):
        self.file = "/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess game 1.pgn"
        self.correct_move = False
        pathlib.Path(self.file).touch()

    def add_move(self, piece_object, piece_starting_pos, piece_ending_pos, piece_type, correct_move, capture_piece=False):
        global white_to_move, black_to_move
        pawn = False
        if correct_move == self.correct_move:
            self.correct_move = not correct_move
            PGN_format = []
            if white_to_move:
                check_white = False
            else:
                check_white = True
            if piece_type == "Rook":
                PGN_format.append("R")
                adding = self.describe_starting_pos(check_white, piece_type, piece_ending_pos, piece_starting_pos)

                if adding[0]:
                    PGN_format.append(self.convert_format(piece_starting_pos[0], piece_starting_pos[1])[0])
                if adding[1]:
                    PGN_format.append(self.convert_format(piece_starting_pos[0], piece_starting_pos[1])[1])

            elif piece_type == "Knight":
                PGN_format.append("N")
            elif piece_type == "Bishop":
                PGN_format.append("B")
            elif piece_type == "Queen":
                PGN_format.append("Q")
            elif piece_type == "King":
                PGN_format.append("K")
            else:
                pawn = True
            break_x = False
            break_y = False
            if piece_object.color:
                for piece in white_pieces:
                    if piece.image_type == piece_object.image_type:
                        white_to_move = not white_to_move
                        if piece.get_legal_moves(piece_ending_pos[0], piece_ending_pos[1]) is True:
                            if piece.pos[0] == piece_starting_pos[0]:
                                if break_y:
                                    break
                                PGN_format.append(self.convert_format(5, piece_starting_pos[1])[1])
                                break_y = True
                            else:
                                if break_x:
                                    break
                                PGN_format.append(self.convert_format(piece_starting_pos[0], 4)[0])
                                print(self.convert_format(piece_starting_pos[0], 4)[0])
                                break_x = True
                        white_to_move = not white_to_move
            else:
                for piece in black_pieces:
                    if piece.image_type == piece_object.image_type:
                        white_to_move = not white_to_move
                        if piece.get_legal_moves(piece_ending_pos[0], piece_ending_pos[1]):
                            if piece.pos[0] == piece_starting_pos[0]:
                                if break_y:
                                    break
                                PGN_format.append(self.convert_format(5, piece_starting_pos[1])[1])
                                break_y = True
                            else:
                                if break_x:
                                    break
                                PGN_format.append(self.convert_format(piece_starting_pos[0], 4)[0])
                                print(self.convert_format(piece_starting_pos[0], 4)[0])
                                break_x = True
                        white_to_move = not white_to_move
            if capture_piece:
                if pawn:
                    PGN_format.append(self.convert_format(piece_starting_pos[0], piece_starting_pos[1])[0])
                PGN_format.append("x")
            PGN_format.append(self.convert_format(piece_ending_pos[0], piece_ending_pos[1])[0])
            PGN_format.append(self.convert_format(piece_ending_pos[0], piece_ending_pos[1])[1])
            if white_to_move:
                white_to_move = not white_to_move
                if white_king_king.is_in_check()[0]:
                    PGN_format.append("+")
                white_to_move = not white_to_move
            else:
                white_to_move = not white_to_move
                if black_king_king.is_in_check()[0]:
                    PGN_format.append("+")
                white_to_move = not white_to_move
            PGN_string_format = ""
            for i in PGN_format:
                PGN_string_format += i
            print(PGN_string_format)
            with open(chess_path, "r") as file:
                lines = file.readlines()
            formatted_moves = ""
            for i in lines:
                formatted_moves += i
                formatted_moves += " "
            formatted_moves += PGN_string_format
            with open(chess_path, "w") as file:
                file.write(formatted_moves)

    def convert_format(self, x, y):
        return_x = self.x_list[x-1]
        return_y = 9-y
        return [str(return_x), str(return_y)]

    @staticmethod
    def describe_starting_pos(check_white, image_type, piece_ending_pos, piece_starting_pos):
        global white_to_move
        add_x = False
        add_y = False
        if check_white:
            white_to_move = not white_to_move
            for piece in white_pieces:
                if piece.get_legal_moves(piece_ending_pos[0], piece_ending_pos[1]):
                    if piece.image_type == image_type:
                        if piece.pos == piece_ending_pos:
                            pass
                        else:
                            if piece.pos[0] == piece_starting_pos[0]:
                                add_y = True
                            elif piece.pos[1] == piece_starting_pos[1]:
                                add_x = True
                            else:
                                add_x = True
            white_to_move = not white_to_move
        else:
            white_to_move = not white_to_move
            for piece in black_pieces:
                if piece.get_legal_moves(piece_ending_pos[0], piece_ending_pos[1]):
                    if piece.image_type == image_type:
                        if piece.pos == piece_ending_pos:
                            pass
                        else:
                            if piece.pos[0] == piece_starting_pos[0]:
                                add_y = True
                            elif piece.pos[1] == piece_starting_pos[1]:
                                add_x = True
                            else:
                                add_x = True
        return [add_x, add_y]


set_up_board_in_starting_config()
chess_game = PGN()
white_pieces = []
black_pieces = []
white_queen_rook = Rook(1, 8, True)
white_queen_knight = Knight(2, 8, True)
white_queen_bishop = Bishop(3, 8, True, False)
white_queen_queen = Queen(4, 8, True)
white_king_king = King(5, 8, True)
white_king_bishop = Bishop(6, 8, True, True)
white_king_knight = Knight(7, 8, True)
white_king_rook = Rook(8, 8, True)

for i in range(1, 9):
    white_pieces.append(Pawn(i, 7, True))


white_pieces.append(white_queen_rook)
white_pieces.append(white_queen_knight)
white_pieces.append(white_queen_bishop)
white_pieces.append(white_queen_queen)
white_pieces.append(white_king_king)
white_pieces.append(white_king_bishop)
white_pieces.append(white_king_knight)
white_pieces.append(white_king_rook)

black_queen_rook = Rook(1, 1, False)
black_queen_knight = Knight(2, 1, False)
black_queen_bishop = Bishop(3, 1, False, True)
black_queen_queen = Queen(4, 1, False)
black_king_king = King(5, 1, False)
black_king_bishop = Bishop(6, 1, False, False)
black_king_knight = Knight(7, 1, False)
black_king_rook = Rook(8, 1, False)

for i in range(1,9):
    black_pieces.append(Pawn(i, 2, False))

black_pieces.append(black_queen_rook)
black_pieces.append(black_queen_knight)
black_pieces.append(black_queen_bishop)
black_pieces.append(black_queen_queen)
black_pieces.append(black_king_king)
black_pieces.append(black_king_bishop)
black_pieces.append(black_king_knight)
black_pieces.append(black_king_rook)

total_pieces = []
for i in white_pieces:
    total_pieces.append(i)
for i in black_pieces:
    total_pieces.append(i)
run = True
pygame.display.update()
mouse_reset = True
while run:
    redraw_board()
    for i in total_pieces:
        i.blit_object()
    mouse_down = pygame.mouse.get_pressed()
    if mouse_down[0]:
        print("going")
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_reset:
            piece = start_drag(mouse_x, mouse_y)
            if piece is not None:
                piece.hide = True
        # noinspection PyUnboundLocalVariable
        # The code is designed to not have this happen
        if piece is not None:
            # noinspection PyUnboundLocalVariable
            dragging_piece(mouse_x, mouse_y, piece)
        mouse_reset = False
    elif mouse_down[0] is not True:
        if mouse_reset is False:
            stop_update = False
            if piece is not None:
                # noinspection PyUnboundLocalVariable
                x, y = return_coordinates_from_pos(mouse_x, mouse_y)
                # noinspection PyUnboundLocalVariable
                piece.hide = False
                for capture_piece in total_pieces:
                    if capture_piece.color != piece.color:
                        if capture_piece.pos == [x, y]:
                            piece_that_should_be_captured = capture_piece
                    else:
                        if stop_update is False:
                            stop_update = not white_to_move == piece.color
                        if capture_piece.pos == [x, y]:
                            stop_update = True
                    if capture_piece.pos == [x, y]:
                        if capture_piece.color == piece.color:
                            stop_update = True
                if piece.get_legal_moves(x, y):
                    pass
                else:
                    stop_update = True
                if piece.pos == [x, y]:
                    stop_update = True
                if stop_update is False:
                    check_move = white_to_move
                    old_pos = piece.pos
                    stop_update_check = False
                    piece.pos = [x, y]
                    if white_to_move:
                        white_to_move = not white_to_move
                        black_to_move = not black_to_move
                        if white_king_king.is_in_check()[0]:
                            try:
                                # noinspection PyUnboundLocalVariable
                                if white_king_king.is_in_check()[1] == piece_that_should_be_captured:
                                    pass
                                else:
                                    piece.pos = old_pos
                                    white_to_move = not white_to_move
                                    black_to_move = not black_to_move
                                    stop_update_check = True
                            except NameError:
                                piece.pos = old_pos
                                white_to_move = not white_to_move
                                black_to_move = not black_to_move
                                stop_update_check = True

                        white_to_move = not white_to_move
                        black_to_move = not black_to_move
                    else:
                        white_to_move = not white_to_move
                        black_to_move = not black_to_move
                        if black_king_king.is_in_check()[0]:
                            try:
                                # noinspection PyUnboundLocalVariable
                                if black_king_king.is_in_check()[1] == piece_that_should_be_captured:
                                    pass
                                else:
                                    piece.pos = old_pos
                                    white_to_move = not white_to_move
                                    black_to_move = not black_to_move
                                    stop_update_check = True
                            except NameError:
                                piece.pos = old_pos
                                white_to_move = not white_to_move
                                black_to_move = not black_to_move
                                stop_update_check = True
                        white_to_move = not white_to_move
                        black_to_move = not black_to_move
                    white_to_move = not white_to_move
                    black_to_move = not black_to_move
                    try:
                        if stop_update_check is False:
                            # noinspection PyUnboundLocalVariable
                            piece_that_should_be_captured.delete_piece()
                        stop_update_check = False
                    except NameError:
                        pass
                else:
                    pass

        mouse_reset = True
        try:
            # noinspection PyUnboundLocalVariable
            if check_move != white_to_move:
                # noinspection PyUnboundLocalVariable
                try:
                    if piece_that_should_be_captured:
                        x = True
                except NameError:
                    x = False
                else:
                    x = True
                # noinspection PyUnboundLocalVariable
                chess_game.add_move(piece, old_pos, piece.pos, piece.image_type, white_to_move, x)
        except NameError:
            pass
        except AttributeError:
            pass

        try:
            del x, y, piece, capture_piece, piece_that_should_be_captured
        except NameError:
            pass
    if mouse_down[2]:
        print('arrows')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
