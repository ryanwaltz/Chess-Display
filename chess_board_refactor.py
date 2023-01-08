import pygame
import time
import pathlib
import math

pygame.init()


path = "/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/"
window = (400, 600)
screen = pygame.display.set_mode(window)
background = pygame.Surface(window)
white_rook = pygame.image.load(path+"wr.png")
white_queen = pygame.image.load(path+"wq.png")
white_pawn = pygame.image.load(path+"wp.png")
white_knight = pygame.image.load(path+"wn.png")
white_king = pygame.image.load(path+"wk.png")
white_bishop = pygame.image.load(path+"wb.png")
black_rook = pygame.image.load(path+"br.png")
black_queen = pygame.image.load(path+"bq.png")
black_pawn = pygame.image.load(path+"bp.png")
black_knight = pygame.image.load(path+"bn.png")
black_king = pygame.image.load(path+"bk.png")
black_bishop = pygame.image.load(path+"bb.png")

white_to_move = True
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

white_pieces = []
black_pieces = []
white_to_move = True
font = pygame.font.SysFont("timesnewromanttf", 50, True)
L_SHIFT = 1
L_CTRL = 64
L_CMD = 1024
L_CAPS = 8192
L_OPTION = 256
R_SHIFT = 1*2
R_CTRL = 64*2
R_CMD = 1024*2
R_OPTION = 256*2

list_of_mods = {"L_CAPS": L_CAPS, "R_CMD": R_CMD, "L_CMD": L_CMD, "R_OPTION": R_OPTION, "L_OPTION": L_OPTION, "R_CTRL": R_CTRL, "L_CTRL": L_CTRL, "R_SHIFT": R_SHIFT, "L_SHIFT": L_SHIFT}

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
list_of_colors = [RED, GREEN, BLUE]


def flip_move(en_passant_check=True):  # called after each move
    global white_to_move
    white_to_move = not white_to_move  # flips white_to_move variable
    if en_passant_check:
        for i in white_pieces+black_pieces:  # making sure enpassant is slowly phased out - you only get one chance to en passant
            if i.en_passantable is True:
                i.en_passantable = 5
            else:
                i.en_passantable = False


def check_for_mate():
    for i in (white_pieces if white_to_move else black_pieces):
        for ii in range(1, 9):
            for iii in range(1, 9):
                condition, _ = i.check_move(ii, iii)
                initial_pos = i.pos
                en_passant_status = i.en_passantable
                if condition:
                    if i.move(ii, iii, False, False, False):
                        i.move(initial_pos[0], initial_pos[1], False, False, False)
                        i.en_passantable = en_passant_status
                        return

    flip_move(False)
    for i in (white_pieces if white_to_move else black_pieces):  # checking in the opposite list
        print(i)
        condition, _ = i.check_move((white_king if not white_to_move else black_king).pos[0],
                                    (white_king if not white_to_move else black_king).pos[1])

        if condition:  # basically make sure that your enemy can't capture your king after this move
            print(("White" if not white_to_move else "Black"), "just got checkmated.")
            pgn_descriptor.complete(True)
            exit()
    print(("White" if white_to_move else "Black"), "just got stalemated.")

    for i in (black_pieces if white_to_move else white_pieces):
        flip_move()
        condition, _ = i.check_move((white_king if white_to_move else black_king).pos[0], (white_king if white_to_move else black_king).pos[1])
        if condition:
            print(f"Checkmated by {i} at {i.pos}")
    exit()


def check_for_check():
    flip_move(False)
    for i in (white_pieces if white_to_move else black_pieces):  # checking in the opposite list
        condition, _ = i.check_move((white_king if not white_to_move else black_king).pos[0],
                                    (white_king if not white_to_move else black_king).pos[1])
        if condition:
            flip_move(False)
            return True
    flip_move(False)
    return False


def draw_screen():

    color_values = [(255, 255, 255), (87, 87, 87)]  # first is for the white squares and second is for black squares

    size = 50
    for i in range(0, 8):
        for j in range(0, 8):
            pygame.draw.rect(background, color_values[(i+j) % 2], (int(i*size), int(j*size), size, size))  # drawing rectangles to create the chessboard

    for i in list_of_squares:
        pygame.draw.rect(background, i[2], (size*(i[0]-1), size*(i[1]-1), size, size))

    for i in lines:
        pygame.draw.line(i[0], i[1], i[2], i[3], i[4])
        x1, y1 = i[2]
        x2, y2 = i[3]
        delta_x = x2-x1
        delta_y = y2-y1
        angle = -math.atan2(delta_y, delta_x)
        delta_x_2 = 25*math.sin(angle-math.pi/3)
        delta_y_2 = 25*math.cos(angle-math.pi/3)
        delta_x_3 = -25*math.sin(angle+math.pi/3)
        delta_y_3 = -25*math.cos(angle+math.pi/3)
        delta_x_2 += x2
        delta_y_2 += y2
        delta_x_3 += x2
        delta_y_3 += y2
        triangle_x_1, triangle_y_1 = delta_x_2, delta_y_2
        triangle_x_2, triangle_y_2 = delta_x_3, delta_y_3

        pygame.draw.polygon(background, i[1], ((triangle_x_1, triangle_y_1), (triangle_x_2, triangle_y_2), (x2, y2)))

    screen.blit(background, (0, 0))  # blit to screen
    for i in white_pieces+black_pieces:
        i.blit_piece()  # blit each piece

    timer.tick()


def grid_to_coords(pos_x, pos_y):  # used for when blitting pieces to screen
    return [(pos_x * size - size), pos_y * size - size]


def coords_to_grid(pos_x, pos_y):  # used for conversions when user clicks
    return [int(pos_x/size)+1, int(pos_y/size)+1]


class Piece(object):  # base class for each subsequent piece

    def __init__(self, starting_pos, color):
        self.starting_pos = starting_pos  # find starting position and initalize position
        self.pos = self.starting_pos
        self.color = color  # color is important for coordinating with other pieces/when you can make moves
        (white_pieces if self.color else black_pieces).append(self)  # append to correct list
        self.image = None  # image will be set up later
        self.abbreviation = ""
        self.image_setup()
        self.hide = False  # variable used for when user is dragging piece on screen
        self.has_moved = False  # used for en passant and castling
        self.en_passantable = False

    def image_setup(self):  # used as a template and overwritten in each class
        pass

    def move(self, new_x, new_y, enpassant=True, update=True, capture=False):  # this checks a move for possible checks and acts accordingly
        self.en_passant_update(new_y)
        old_pos = self.pos  # store old position in case it needs to revert
        self.pos = [new_x, new_y]  # update position
        flip_move(False)  # flip the move (temporarily or may become permanent)
        for i in (white_pieces if not self.color else black_pieces):  # checking in the opposite list
            if i.pos == self.pos:  # it's fine if you're trying to capture the piece that has your king in check
                pass
            else:  # otherwise...  # todo can't check for capture when there's already two pieces there  # DONE
                condition, _ = i.check_move((white_king if self.color else black_king).pos[0], (white_king if self.color else black_king).pos[1])

                if condition:  # basically make sure that your enemy can't capture your king after this move
                    self.pos = old_pos  # if so, revert to the old position and flip the move back
                    flip_move(False)
                    return False  # returning false makes sure that you don't capture the piece
        flip_move(False)
        flip_move(enpassant)
        if update:
            pgn_descriptor.update(new_x, new_y, old_pos[0], old_pos[1], self, capture=capture)
        self.has_moved = True  # all's well let's proceed with the moving
        return True

    def check_move(self, new_x, new_y, check_castle=False):  # placeholder method that gets overwritten in each class
        return False, False

    def blit_piece(self):  # used to blit each piece to the screen.
        if not self.hide:  # might be hidden if it's getting dragged
            screen.blit(self.image, grid_to_coords(self.pos[0], self.pos[1]))

    def delete(self):  # when the piece gets captured
        (white_pieces if self.color else black_pieces).remove(self)

    def check_if_occupied(self, new_x, new_y):  # logic to make sure a square isn't occupied
        new_pos = [new_x, new_y]
        piece_to_return = False
        returning_false = False
        for piece in (white_pieces if self.color else black_pieces):  # in your own pieces
            if piece == self:
                pass  # it's fine if you already occupy that square with yourself.
            elif piece.pos == new_pos:
                returning_false = True  # returns False if you already occupy that square with a different piece
        for piece in (black_pieces if self.color else white_pieces):  # in your opponent's pieces
            if piece.pos == new_pos:
                piece_to_return = piece
                break
        if piece_to_return and returning_false:
            return True
        elif piece_to_return:
            return piece_to_return
        elif returning_false:
            return False
        return True

    def en_passant_update(self, new_y):
        pass


class Pawn(Piece):

    def image_setup(self):
        self.image = (white_pawn if self.color else black_pawn)

    def check_move(self, new_x, new_y, check_for_castle=False):  # logic for moves
        old_x = self.pos[0]  # it's easier with old_x and old_y as opposed to referencing lists
        old_y = self.pos[1]
        if self.color is not white_to_move:  # make sure it's your turn
            return False, False
        if new_x == old_x:  # checking normal moves

            for i in white_pieces + black_pieces:  # make sure there's not a piece where you want to move
                if i.pos == [new_x, new_y]:
                    return False, False
            if (new_y - old_y)*(1 if self.color else -1) == -2:  # for moving two squares at once
                if old_y == 7 if self.color else 2:  # making sure it's on the right level
                    if not self.check_if_occupied(new_x, (6 if self.color else 3)) or (type(self.check_if_occupied(new_x, 6 if self.color else 3)) is not bool):
                        return False, False
                    return True, False
            if (new_y - old_y)*(1 if self.color else -1) == -1:  # for moving one square
                return True, False
        elif abs(new_x - old_x) == 1 and (new_y - old_y)*(1 if self.color else -1) == -1:  # checking captures
            for i in (white_pieces if not self.color else black_pieces):
                if i.pos == [new_x, new_y]:  # check if a piece is there
                    if (new_y - old_y)*(1 if self.color else -1) == -1:  # make sure it's going diagonally the right way
                        return True, i
                elif [i.pos[0], i.pos[1] - (1 if self.color else -1)] == [new_x, new_y]:  # en passant
                    if i.en_passantable:
                        return True, i
        return False, False

    def promotion(self):  # assumes promotion to a queen
        (white_pieces if self.color else black_pieces).append(Queen(self.pos, self.color))
        (white_pieces if self.color else black_pieces).remove(self)

    def en_passant_update(self, new_y):
        if (new_y - self.pos[1])*(1 if self.color else -1) == -2:
            self.en_passantable = True


class Knight(Piece):

    def image_setup(self):
        self.image = (white_knight if self.color else black_knight)
        self.abbreviation = "N"

    def check_move(self, new_x, new_y, check_for_castle=False):
        old_x = self.pos[0]
        old_y = self.pos[1]
        if self.color is not white_to_move:
            return False, False
        if old_x == new_x or old_y == new_y:
            return False, False
        if abs(old_x - new_x) + abs(old_y - new_y) == 3:
            occupied = self.check_if_occupied(new_x, new_y)
            if type(occupied) is not bool:
                return True, occupied
            elif occupied:
                return True, False
        return False, False


class Rook(Piece):

    def image_setup(self):
        self.image = (white_rook if self.color else black_rook)
        self.abbreviation = "R"

    def check_move(self, new_x, new_y, check_for_castle=False):
        old_x = self.pos[0]
        old_y = self.pos[1]
        if self.color is not white_to_move:
            return False, False
        if not (old_x == new_x and old_y == new_y) and (old_x == new_x or old_y == new_y):
            for i in range((old_x if old_x < new_x else new_x)+1, (old_x if old_x > new_x else new_x)):
                if not self.check_if_occupied(i, new_y) or (type(self.check_if_occupied(i, new_y)) is not bool):
                    return False, False
            for i in range((old_y if old_y < new_y else new_y)+1, (old_y if old_y > new_y else new_y)):
                if not self.check_if_occupied(new_x, i) or (type(self.check_if_occupied(new_x, i)) is not bool):
                    return False, False
        else:
            return False, False
        occupied = self.check_if_occupied(new_x, new_y)
        if type(occupied) is not bool:
            return True, occupied
        elif occupied:
            return True, False
        return False, False


class Bishop(Piece):

    def image_setup(self):
        self.image = (white_bishop if self.color else black_bishop)
        self.abbreviation = "B"

    def check_move(self, new_x, new_y, check_for_castle=False):
        old_x = self.pos[0]
        old_y = self.pos[1]
        if self.color is not white_to_move:
            return False, False
        if not (old_x == new_x or old_y == new_y) and abs(old_x-new_x)-abs(old_y-new_y) == 0:  # diagonals
            for i in range(1, abs(old_x-new_x)):
                x, y = (old_x+(i if old_x<new_x else -i)), (old_y+(i if old_y<new_y else -i))
                if not self.check_if_occupied(x, y) or (type(self.check_if_occupied(x,y)) is not bool):
                    return False, False
        else:
            return False, False
        occupied = self.check_if_occupied(new_x, new_y)
        if type(occupied) is not bool:
            return True, occupied
        elif occupied:
            return True, False
        return False, False


class Queen(Piece):

    def image_setup(self):
        self.image = (white_queen if self.color else black_queen)
        self.abbreviation = "Q"

    def check_move(self, new_x, new_y, check_for_castle=False):
        if self.color is not white_to_move:
            return False, False
        condition, piece = Rook.check_move(self, new_x, new_y)
        if condition:
            return condition, piece
        condition, piece = Bishop.check_move(self, new_x, new_y)
        if condition:
            return condition, piece
        return False, False


class King(Piece):

    def image_setup(self):
        self.image = (white_king if self.color else black_king)
        self.abbreviation = "K"

    def check_move(self, new_x, new_y, check_castle=False):
        old_x = self.pos[0]
        old_y = self.pos[1]
        if self.color is not white_to_move:
            return False, False
        if 0 < abs(new_x-old_x) + abs(new_y-old_y) < 3 and not (abs(new_x-old_x)==2 or abs(new_y-old_y)==2):
            occupied = self.check_if_occupied(new_x, new_y)
            if type(occupied) is not bool:
                return True, occupied
            elif occupied:
                return True, False
        if check_castle:
            if self.has_moved is False:  # castling is pain to implement
                if [new_x, new_y] == [7, (8 if self.color else 1)]:
                    for i in range(6, 8):
                        if type(self.check_if_occupied(i, (8 if self.color else 1))) is not bool or self.check_if_occupied(i, (8 if self.color else 1)) is False:
                            return False, False
                    if self.move(6, (8 if self.color else 1)):
                        self.move(5, (8 if self.color else 1))
                    else:
                        return False, False
                    self.castle(new_x, new_y, True)
                    return False, False
                if (new_x, new_y) == (3, (8 if self.color else 1)):
                    for i in range(2, 4):
                        if type(self.check_if_occupied(i, (8 if self.color else 1))) is not bool or self.check_if_occupied(i, (8 if self.color else 1)) is False:
                            return False, False
                    if self.move(4, (8 if self.color else 1)):
                        self.move(5, (8 if self.color else 1))
                    else:
                        return False, False
                    self.castle(new_x, new_y, False)
                    return False, False
        return False, False

    def castle(self, new_x, new_y, king_side):  # assumes all measures have been taken and this is just the actually castling bit
        if king_side:
            for i in (white_pieces if self.color else black_pieces):
                if i.image == (white_rook if self.color else black_rook) and i.pos == [8, new_y]:
                    if self.move(new_x, new_y):
                        i.pos = [6, new_y]
        else:
            for i in (white_pieces if self.color else black_pieces):
                if i.image == (white_rook if self.color else black_rook) and i.pos == [1, new_y]:
                    if self.move(new_x, new_y):
                        i.pos = [4, new_y]


class Timer(object):
    def __init__(self, starting_time_white, starting_time_black=False):
        self.starting_time = time.time()
        self.white_time = starting_time_white
        self.black_time = starting_time_black if starting_time_black else starting_time_white
        self.alpha_time = self.starting_time
        self.background = pygame.Surface((400, 200))

    def tick(self):
        difference_time = time.time() - self.alpha_time
        if white_to_move:
            self.white_time -= difference_time
        else:
            self.black_time -= difference_time
        self.alpha_time = time.time()
        self.draw()

    def draw(self):
        pygame.draw.rect(self.background, (255, 255, 255), (0, 0, 200, 200))
        pygame.draw.rect(self.background, (0, 0, 0), (200, 0, 200, 200))
        text_white = int(self.white_time)
        text_black = int(self.black_time)
        text_white = self.format_text(text_white)
        text_black = self.format_text(text_black)
        text_width_white, text_height_white = font.size(text_white)  # txt being whatever str you're rendering
        text_width_black, text_height_black = font.size(text_white)  # txt being whatever str you're rendering
        text_white = font.render(text_white, 1, (0, 0, 0))
        text_black = font.render(text_black, 1, (255, 255, 255))
        screen.blit(self.background, (0, 400))
        screen.blit(text_white, (100-(text_width_white/2), 500-(text_height_white/2)))
        screen.blit(text_black, (300-(text_width_black/2), 500-(text_height_black/2)))

    @staticmethod
    def format_text(raw_time):
        minute = int(raw_time/60)
        second = int(raw_time%60)
        return str(minute) + ":" + ("0" if len(str(second)) == 1 else "") + str(second)


class PGN(object):
    list_of_letters = "abcdefgh"
    list_of_pieces = [Rook, Knight, Bishop, Queen, King]

    def __init__(self, file_path):
        self.file_path = file_path
        pathlib.Path(file_path).touch()
        self.PGN_list = []
        self.output_string = ""

    def check_for_other_pieces(self, pos_x, pos_y, old_x, old_y, piece, type_to_check):
        addition = ""
        if isinstance(piece, type_to_check):
            flip_move(False)
            piece.delete()
            for i in (white_pieces if piece.color else black_pieces):
                if i != piece:
                    if isinstance(i, type_to_check):
                        piece.move(old_x, old_y, update=False, enpassant=False)
                        flip_move(False)
                        condition, _ = i.check_move(pos_x, pos_y)
                        if condition:
                            addition = self.grid_to_notation(old_x, old_y)[1 if pos_x == i.pos[0] else 0]
                            piece.move(pos_x, pos_y, update=False, enpassant=False)
                            flip_move(False)
                            break
                        piece.move(pos_x, pos_y, update=False, enpassant=False)
                        flip_move(False)
            (white_pieces if piece.color else black_pieces).append(piece)
            flip_move(False)
            addition = piece.abbreviation + addition
        return addition

    def update(self, pos_x, pos_y, old_x, old_y, piece, capture=False, specials=None):
        return_string = self.grid_to_notation(pos_x, pos_y)
        if capture:
            return_string = "x" + return_string
            if isinstance(piece, Pawn):
                return_string = self.grid_to_notation(old_x, old_y)[0] + return_string
        addition = ""
        for i in self.list_of_pieces:
            addition = self.check_for_other_pieces(pos_x, pos_y, old_x, old_y, piece, i)
            if addition:
                break
        return_string = addition + return_string
        if check_for_check():
            return_string += "+"

        self.PGN_list.append(return_string)

    @staticmethod
    def grid_to_notation(pos_x, pos_y):
        return PGN.list_of_letters[pos_x-1] + str(9-pos_y)

    def complete(self, checkmate=False):
        if checkmate:
            last_string = self.PGN_list[-1]
            last_string = last_string.replace("+", "#")
            self.PGN_list.pop(-1)
            self.PGN_list.append(last_string)
        iterator = 0
        for i in self.PGN_list:
            if self.PGN_list.index(i) % 2 == 0:
                iterator += 1
                self.output_string += str(iterator) + ". "
            self.output_string += i + " "
        with open(self.file_path, "w") as file:
            file.write(self.output_string)


def mouse_click(x, y):
    piece = None
    pos_x, pos_y = coords_to_grid(x, y)
    for i in black_pieces+white_pieces:
        if i.pos == [pos_x, pos_y]:
            piece = i
    return [pos_x, pos_y], piece


def right_click(x, y):
    pos_x, pos_y = coords_to_grid(x, y)
    return pos_x, pos_y


def dragging(x, y, piece):
    if piece:
        screen.blit(piece.image, (x-25, y-25))


def run():
    global lines, list_of_squares
    run = True
    while run:
        mouse_down = pygame.mouse.get_pressed()
        if mouse_down[0]:
            lines = []
            list_of_squares = []

            mouse_x, mouse_y = pygame.mouse.get_pos()
            position, piece = mouse_click(mouse_x, mouse_y)
            if piece:
                piece.hide = True
            while mouse_down[0]:
                mouse_down = pygame.mouse.get_pressed()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                mouse_x, mouse_y = pygame.mouse.get_pos()
                draw_screen()
                if piece:
                    dragging(mouse_x, mouse_y, piece)
                pygame.display.flip()
            if piece:
                new_x, new_y = coords_to_grid(mouse_x, mouse_y)
                condition, piece_to_capture = piece.check_move(new_x, new_y)
                if condition:
                    if piece.move(new_x, new_y, capture=bool(piece_to_capture)):
                        check_for_mate()
                        if piece_to_capture:
                            piece_to_capture.delete()
                        if piece.image == (white_pawn if piece.color else black_pawn) and (piece.pos[1] == (1 if piece.color else 8)):
                            piece.promotion()
                piece.hide = False
        if mouse_down[2]:
            mods = pygame.key.get_mods()
            list_of_mods_pressed = []
            for i in list_of_mods:
                if mods == list_of_mods[i]:
                    list_of_mods_pressed.append(i)
                elif 0 < mods - list_of_mods[i] < list_of_mods[i]:
                    mods -= list_of_mods[i]
                    list_of_mods_pressed.append(i)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            square_x, square_y = right_click(mouse_x, mouse_y)
            while mouse_down[2]:
                mouse_down = pygame.mouse.get_pressed()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

            mouse_x, mouse_y = pygame.mouse.get_pos()
            square_x_2, square_y_2 = right_click(mouse_x, mouse_y)
            if square_x_2 == square_x and square_y_2 == square_y:
                appendage = [square_x, square_y, list_of_colors[len(list_of_mods_pressed)]]
                if appendage in list_of_squares:
                    list_of_squares.remove([square_x, square_y, list_of_colors[len(list_of_mods_pressed)]])
                else:
                    list_of_squares.append([square_x, square_y, list_of_colors[len(list_of_mods_pressed)]])

            else:
                try:
                    x1, y1 = grid_to_coords(square_x, square_y)
                    x2, y2 = grid_to_coords(square_x_2, square_y_2)
                    x1 += 25
                    y1 += 25
                    x2 += 25
                    y2 += 25
                    for i in lines:
                        if i[2] == (x1, y1) and i[3] == (x2, y2):
                            lines.remove(i)
                            raise DuplicateArrow

                    lines.append([background, list_of_colors[len(list_of_mods_pressed)], (x1, y1), (x2, y2), 5])
                except DuplicateArrow:
                    pass

        draw_screen()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


class DuplicateArrow(Exception):
    pass


if __name__ == "__main__":
    pgn_descriptor = PGN("/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess game 1.pgn")
    lines = []
    list_of_squares = []
    for i in range(1, 9):
        Pawn([i, 7], True)
        Pawn([i, 2], False)
    Bishop([3, 1], False)
    Bishop([3, 8], True)
    Bishop([6, 1], False)
    Rook([1, 1], False)
    Rook([8, 1], False)
    Rook([1, 8], True)
    Rook([8, 8], True)
    Knight([2, 1], False)
    Knight([7, 1], False)
    Knight([2, 8], True)
    Knight([7, 8], True)
    Bishop([6, 8], True)
    black_king = King([5, 1], False)
    white_king = King([5, 8], True)
    Queen([4, 1], False)
    Queen([4, 8], True)
    timer = Timer(300)  # I know I'm playing with fire with the naming schemes
    try:
        run()
    except KeyboardInterrupt:
        pgn_descriptor.complete()
