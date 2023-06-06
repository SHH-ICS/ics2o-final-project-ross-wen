import pygame
import os
import random


#important variables, will change rows and cols to user input later on if i have time
TILE_SIZE = 32
ROWS = 9
COLS = 9
NUM_MINES = 10
FPS = 60
WIDTH = TILE_SIZE*ROWS
HEIGHT = TILE_SIZE*COLS
TITLE = "MINESWEEPER - ROSS FINAL PROJECT" 

#pygame colors
BACKGROUND_COLOR = (40, 40, 40)


#put all clue images in assets folder into an array
tile_numbers = []
for i in range(1,8):
  tile_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", f"Tile{i}.png")),(TILE_SIZE,TILE_SIZE)))

#put all other sprites into their own independant variables
tile_empty = pygame.transform.scale(pygame.image.load(os.path.join("assets","TileEmpty.png")),(TILE_SIZE,TILE_SIZE))
tile_exploded = pygame.transform.scale(pygame.image.load(os.path.join("assets","TileExploded.png")),(TILE_SIZE,TILE_SIZE))
tile_flag = pygame.transform.scale(pygame.image.load(os.path.join("assets","TileFlag.png")),(TILE_SIZE,TILE_SIZE))
tile_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets","TileMine.png")),(TILE_SIZE,TILE_SIZE))
tile_not_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets","TileNotMine.png")),(TILE_SIZE,TILE_SIZE))
tile_unknown = pygame.transform.scale(pygame.image.load(os.path.join("assets","TileUnknown.png")),(TILE_SIZE,TILE_SIZE))


#game class where the entire thing will be run
class Game:
  def __init__(self): #initialize the class
    self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) #basic pygame initialization stuff
    pygame.display.set_caption(TITLE)
    self.clock = pygame.time.Clock()
    
  def new(self):
    self.board = Board()
    self.board.display_board()
    
  def run(self): #game loop 
    self.playing = True
    while self.playing:
      self.clock.tick(FPS)
      self.events() 
      self.draw() 
      
  def events(self):
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
          
  def draw(self):
    self.screen.fill(BACKGROUND_COLOR)
    self.board.draw(self.screen)
    pygame.display.flip()

#tile class for tiles
#four different types for the tiles
#unkown
#clue
#bomb
#empty

class Tile:
  def __init__(self, x, y, image, type, revealed = False, flagged = False):
    self.x, self.y = x * TILE_SIZE, y * TILE_SIZE
    self.image = image
    self.type = type
    self.revealed = revealed
    self.flagged = flagged

  def draw(self, board_surface):
    board_surface.blit(self.image, (self.x, self.y))
    
  def __repr__(self):
    return self.type
    
    
    
#board class for the board
class Board:
  def __init__(self):
    self.board_surface = pygame.Surface((WIDTH,HEIGHT))
    self.board_list = [[Tile(col, row, tile_empty, ".") for row in range(ROWS)] for col in range(COLS)]

  def draw(self, screen):
    for row in self.board_list:
      for tile in row:
        tile.draw(self.board_surface)
    screen.blit(self.board_surface,(0,0))
      
  def place_mines(self):
    for i in range(NUM_MINES):
      while True:
        x = random.randint(0, COLS-1)
        y = random.randint(0, ROWS-1)

        if self.board_list[x][y].type == ".":
          self.board_list[x][y].image = tile_mine
          self.board_list[x][y].type = "bomb"
          break
        
  def display_board(self):
    for row in self.board_list:
      print(row)



game = Game()
while True: #runs the entire game class in a loop
  game.new()
  game.run()