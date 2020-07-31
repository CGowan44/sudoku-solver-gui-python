import pygame
from Sudoku_simplified import Solve, isValid

pygame.font.init()

class Grid:
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.cells = [[Cell(0, i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.selected = None

    def place(self, val):
        row, col = self.selected

        if isValid(val, row, col, self.cells):
            self.cells[row][col].set_val(val)
            return True
        else:
            self.cells[row][col].set_val(0)
            return False

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)
        
        # Draw Cells
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(win)

    def select(self, row, col):
        # Reset all other spaces
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        for row in range(9):
            for col in range(9):
                self.cells[row][col].set_val(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            # must flip x and y to accommodate traditional matrix accessing format
            return (int(y), int(x))
        else:
            return None
            
class Cell:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width ,height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        font = pygame.font.SysFont("comicsans", 40)
        # Font change example
        # font = pygame.font.SysFont("data/coolvetica", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if not(self.value == 0):
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (128,35,31), (x,y, gap, gap), 3)

    def set_val(self, val):
        self.value = val

class Button:
    def __init__(self, color, x, y, width, height, text = ''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            # Font change example
            # font = pygame.font.SysFont("data/coolvetica", 35)

            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

def redraw_window(win, board, button):
    win.fill((255,255,255))
    board.draw(win)
    button.draw(win)

def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 540, 540)
    solveButton = Button((128, 128, 128), 400, 550, 100, 40, 'Solve')
    key = None
    run = True
    redraw_window(win, board, solveButton)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    key = 0
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    # Clear the board when del key pressed
                    board.clear()
                    key = None
                    redraw_window(win, board, solveButton)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # determine position of mouse click
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked: # if clicked on board
                    board.select(clicked[0], clicked[1])
                    key = None
                    redraw_window(win, board, solveButton)
                if solveButton.isOver(pos): # if solve button clicked
                    Solve(board.cells)
                    key = None
                    redraw_window(win, board, solveButton)

            if event.type == pygame.MOUSEMOTION:
                # hover effects for the solve button
                pos = pygame.mouse.get_pos()
                if solveButton.isOver(pos):
                    solveButton.color = (0, 255, 0)
                else:
                    solveButton.color = (128, 128, 128)
                redraw_window(win, board, solveButton)

        if board.selected and key != None:
            # place a number into the board
            board.place(key)
            redraw_window(win, board, solveButton)
            key = None
        pygame.display.update()


main()
pygame.quit()