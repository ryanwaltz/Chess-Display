import pygame

pygame.init()

path = "/Users/ryanwaltz/Desktop/Desktop - MacBook Pro (3)/Chess timer/Chess_pieces/"
window = (400, 400)
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


def flip_move():  # called after each move
    global white_to_move
    white_to_move = not white_to_move  # flips white_to_move variable
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
                if condition:
                    if i.move(ii, iii):
                        i.move(initial_pos[0], initial_pos[1])
                        return
    print(("White" if white_to_move else "Black"), "just got checkmated.")
    exit()


def draw_screen():

    color_values = [(255, 255, 255), (87, 87, 87)]  # first is for the white squares and second is for black squares

    for i in range(0, 8):
        for j in range(0, 8):
            pygame.draw.rect(background, color_values[(i+j) % 2], (int(i*(400/8)), int(j*(400/8)), 57, 57))  # drawing rectangles to create the chessboard

    screen.blit(background, (0, 0))  # blit to screen
    for i in white_pieces+black_pieces:
        i.blit_piece()  # blit each piece


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
        self.image_setup()
        self.hide = False  # variable used for when user is dragging piece on screen
        self.has_moved = False  # used for en passant and castling
        self.en_passantable = False

    def image_setup(self):  # used as a template and overwritten in each class
        pass

    def move(self, new_x, new_y):  # this checks a move for possible checks and acts accordingly
        old_pos = self.pos  # store old position in case it needs to revert
        self.pos = [new_x, new_y]  # update position
        flip_move()  # flip the move (temporarily or may become permanent)
        for i in (white_pieces if not self.color else black_pieces):  # checking in the opposite list
            if i.pos == self.pos:  # it's fine if you're trying to capture the piece that has your king in check
                pass
            else:  # otherwise...  # todo can't check for capture when there's already two pieces there  # DONE
                condition, _ = i.check_move((white_king if self.color else black_king).pos[0], (white_king if self.color else black_king).pos[1])
                if condition:  # basically make sure that your enemy can't capture your king after this move
                    self.pos = old_pos  # if so, revert to the old position and flip the move back
                    flip_move()
                    return False  # returning false makes sure that you don't capture the piece
        self.has_moved = True  # all's well let's proceed with the moving
        return True

    def check_move(self, new_x, new_y):  # placeholder method that gets overwritten in each class
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


class Pawn(Piece):

    def image_setup(self):
        self.image = (white_pawn if self.color else black_pawn)

    def check_move(self, new_x, new_y):  # logic for moves
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

    def move(self, new_x, new_y):
        if (new_y - self.pos[1])*(1 if self.color else -1) == -2:
            self.en_passantable = True
        old_pos = self.pos
        self.pos = [new_x, new_y]
        flip_move()
        for i in (white_pieces if not self.color else black_pieces):
            condition, _ = i.check_move((white_king if self.color else black_king).pos[0], (white_king if self.color else black_king).pos[1])
            if condition:
                self.pos = old_pos
                flip_move()
                return False

        self.has_moved = True
        return True


class Knight(Piece):

    def image_setup(self):
        self.image = (white_knight if self.color else black_knight)

    def check_move(self, new_x, new_y):
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

    def check_move(self, new_x, new_y):
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

    def check_move(self, new_x, new_y):
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

    def check_move(self, new_x, new_y):
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

    def check_move(self, new_x, new_y):
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


def mouse_click(x, y):
    piece = None
    pos_x, pos_y = coords_to_grid(x, y)
    for i in black_pieces+white_pieces:
        if i.pos == [pos_x, pos_y]:
            piece = i
    return [pos_x, pos_y], piece


def dragging(x, y, piece):
    if piece:
        screen.blit(piece.image, (x-25, y-25))


def run():
    run = True
    while run:
        mouse_down = pygame.mouse.get_pressed()
        if mouse_down[0]:
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
                    if piece.move(new_x, new_y):
                        check_for_mate()
                        if piece_to_capture:
                            piece_to_capture.delete()
                        if piece.image == (white_pawn if piece.color else black_pawn) and (piece.pos[1] == (1 if piece.color else 8)):
                            piece.promotion()
                piece.hide = False

        draw_screen()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


if __name__ == "__main__":
    for i in range(1, 9):
        Pawn([i, 7], True)
        Pawn([i, 2], False)
    Bishop([3, 1], False)
    Bishop([6, 1], False)
    Bishop([3, 8], True)
    Bishop([6, 8], True)
    Rook([1, 1], False)
    Rook([8, 1], False)
    Rook([1, 8], True)
    Rook([8, 8], True)
    Knight([2, 1], False)
    Knight([7, 1], False)
    Knight([2, 8], True)
    Knight([7, 8], True)
    black_king = King([5, 1], False)
    white_king = King([5, 8], True)
    Queen([4, 1], False)
    Queen([4, 8], True)
    run()

