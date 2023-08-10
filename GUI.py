import sudoku
import pygame
import time

_FRAME_RATE = 30
_INITIAL_WIDTH = 600
_INITIAL_HEIGHT = 600
_BACKGROUND_COLOR = pygame.Color(255, 255, 255)
_BLACK = (0, 0, 0)
_GRAY = (169, 169, 169)
class SudokuSolve:
    example_board = [
        [0, 9, 0,   1, 4, 0,   0, 0, 0],
        [0, 0, 5,   0, 0, 0,   0, 2, 0],
        [0, 3, 0,   0, 0, 0,   0, 6, 0],
        
        [0, 4, 6,   0, 0, 0,   0, 0, 0],
        [1, 2, 0,   9, 3, 0,   0, 4, 5],
        [0, 0, 3,   0, 0, 4,   0, 0, 6],
        
        [4, 0, 0,   0, 0, 1,   2, 0, 0],
        [0, 8, 0,   4, 0, 0,   0, 0, 3],
        [3, 5, 0,   7, 0, 0,   9, 0, 0]
    ]
    
    def __init__(self) -> None:
        self._running = True
        self._matrix = SudokuSolve.example_board
        self._complete = False
    def run(self) -> None:
        pygame.init()
        self._font = pygame.font.SysFont("Arial", 25)
        try:
            clock = pygame.time.Clock()
            self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))
            self._draw_grid((_INITIAL_WIDTH, _INITIAL_HEIGHT), 9, _GRAY)
            self._draw_grid((_INITIAL_WIDTH, _INITIAL_HEIGHT), 3, _BLACK)
            self._update((_INITIAL_WIDTH, _INITIAL_HEIGHT))
            pygame.display.flip()
            while self._running:
                clock.tick(_FRAME_RATE)
                self._handle_events()
                pygame.event.pump
        finally:
            pygame.quit()
    def _create_surface(self, size: tuple[int, int]) -> None:
        '''Creates the initial surface for the game.'''
        self._surface = pygame.display.set_mode(size)
        self._surface.fill((255, 255, 255))
    def _draw_grid(self, size, boxes, color):
        x = 0
        y = 0
        window_width = size[0]
        window_height = size[1]
        x_blocksize = window_width/boxes
        y_blocksize = window_height/boxes
        for row in self._matrix:
            for column in row:
                rect = pygame.Rect(x, y, x_blocksize, y_blocksize)
                pygame.draw.rect(self._surface, color , rect, 1)
                x += x_blocksize
            y += y_blocksize
            x = 0
    def _solve(self):
        '''Solves the game'''
        if sudoku.determineSolvable(self._matrix) == False:
            return False
        row, col = sudoku.find_empty(self._matrix)
        if row == None and col == None:
            return True
        for guess in range(1, 10):
            if sudoku.determine_valid(self._matrix, guess, row , col):
                self._matrix[row][col] = guess
                self._update((_INITIAL_WIDTH, _INITIAL_HEIGHT))
                #solving speed is too quick to watch the algorithm work
                time.sleep(0.1)
                if self._solve():
                    self._complete = True
                    return True
            self._matrix[row][col] = 0
        return False
    def _handle_events(self) -> None:
        '''Handles the keyboard events.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    success = self._solve()
                    if success == False:
                        self._displayUnsolvable()
                elif event.key == pygame.K_q:
                    pygame.quit()
    def _displayUnsolvable(self):
        '''Display the word unsolvable if the puzzle is unsolvable.'''
        self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))
        text_surface = self._font.render("Unsolvable", False, (0, 0, 0))
        self._surface.blit(text_surface, (250, 250))
        pygame.display.flip()
    def _update(self, size):
        '''Updates the screen for each number tried.'''
        self._create_surface((_INITIAL_WIDTH, _INITIAL_HEIGHT))
        self._draw_grid((_INITIAL_WIDTH, _INITIAL_HEIGHT), 9, _GRAY)
        self._draw_grid((_INITIAL_WIDTH, _INITIAL_HEIGHT), 3, _BLACK)
        if self._complete == False:
            x = 0
            y = 0
            window_width = size[0]
            window_height = size[1]
            x_blocksize = window_width/9
            y_blocksize = window_height/9
            for row in self._matrix:
                for col in row:
                    if col != 0:
                        rect = pygame.Rect(x+10, y+10, x_blocksize-20, y_blocksize-20)
                        pygame.draw.rect(self._surface, (255, 255, 255), rect, 1)
                        rect = pygame.Rect(x + 25, y + 20, x_blocksize, y_blocksize)
                        text = self._font.render(str(col), 1, _BLACK)
                        self._surface.blit(text, rect)
                    x += x_blocksize
                y += y_blocksize
                x = 0
            pygame.display.flip()
            
if __name__ == '__main__':
    SudokuSolve().run()

