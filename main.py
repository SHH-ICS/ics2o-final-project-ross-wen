import pygame
import os
import random


#important global variables, will change rows and cols to user input later on if i have time
TILE_SIZE = 32
ROWS = 9
COLS = 9
NUM_MINES = 10
FPS = 30
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

  #this is just to print if the bombs and clues were being loaded correctly
  def new(self):
    self.board = Board()
    self.board.display_board()
    
  def run(self): #game loop 
    self.playing = True
    while self.playing:
      self.clock.tick(FPS)
      self.events() 
      self.draw() 

  #all the events for minesweeper
  def events(self):
      for event in pygame.event.get():
        #quit
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
        #if press mousebutton
        if event.type == pygame.MOUSEBUTTONDOWN:
          mx, my = pygame.mouse.get_pos()
          mx //= TILE_SIZE
          my //= TILE_SIZE

          #if left click, then dig and check if you died
          if event.button == 1:
            if not self.board.board_list[mx][my].flagged: #make sure its not flagged because if its flagged then do nothing
              #click and check if bomb
              if not self.board.click(mx,my): #lose
                for row in self.board.board_list:
                  for tile in row:
                    if tile.flagged and tile.type != "B":
                      tile.flagged = False
                      tile.revealed = True
                      tile.image = tile_not_mine
                    elif tile.type == "B":
                      tile.revealed = True
                self.playing = False
                

          #if right click
          if event.button == 3:
            if not self.board.board_list[mx][my].revealed: #make sure its not revealed, if it is then do nothign
              if self.board.board_list[mx][my].flagged: #if true, turn false, if false turn true
                self.board.board_list[mx][my].flagged = False
              elif not self.board.board_list[mx][my].flagged:
                self.board.board_list[mx][my].flagged = True
              
              
              
              
          
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

  #draw all the images
  def draw(self, board_surface):
    #clue
    if not self.flagged and self.revealed:
      board_surface.blit(self.image, (self.x, self.y))
    #flag
    elif self.flagged and not self.revealed:
      board_surface.blit(tile_flag, (self.x, self.y))
    #unknown
    elif not self.revealed:
      board_surface.blit(tile_unknown, (self.x, self.y))

  #just to print out the array
  def __repr__(self):
    return self.type
    
    
    
#board class for the board
class Board:
  def __init__(self):
    self.board_surface = pygame.Surface((WIDTH,HEIGHT))
    #for inline loop to create grid
    self.board_list = [[Tile(col, row, tile_empty, ".") for row in range(ROWS)] for col in range(COLS)]
    self.place_mines()
    self.place_clues()
    self.clicked = []

  #draws each tile
  def draw(self, screen):
    for row in self.board_list:
      for tile in row:
        tile.draw(self.board_surface)
    screen.blit(self.board_surface,(0,0))

  #places mines 
  def place_mines(self):
    for i in range(NUM_MINES): #runs the loop however many times there are mines
      while True: #while loop to check if theres alreayd a bomb 
        x = random.randint(0, COLS-1)
        y = random.randint(0, ROWS-1)
        
        if self.board_list[x][y].type == ".":
          self.board_list[x][y].image = tile_mine
          self.board_list[x][y].type = "B"
          break

  def place_clues(self):
    for x in range(ROWS):
      for y in range(COLS):
        if self.board_list[x][y].type != "B":
          total_mines = self.neighbor_check(x,y)
          if total_mines > 0:
            self.board_list[x][y].type = "C"
            self.board_list[x][y].image = tile_numbers[total_mines-1]

  #make sure theres no index array errors when it checks outside the array
  @staticmethod
  def inside(x,y):
    return 0 <= x < ROWS and 0 <= y < COLS

  
  def neighbor_check(self, x, y):
    total_mines = 0
    for x_offset in range(-1,2): #x and y offset to check all tiles around the surrounding tile
      for y_offset in range(-1,2):
        neighbor_x = x + x_offset
        neighbor_y = y + y_offset
        if self.inside(neighbor_x, neighbor_y) and self.board_list[neighbor_x][neighbor_y].type == "B":
            total_mines += 1
    return total_mines

  def click(self, x, y):
    self.clicked.append((x,y))
    if self.board_list[x][y].type == "B":
      self.board_list[x][y].revealed = True
      self.board_list[x][y].image = tile_exploded
      return False
    elif self.board_list[x][y].type == "C":
      self.board_list[x][y].revealed = True
      return True

    self.board_list[x][y].revealed = True

    for row in range(max(0,x-1), min(ROWS-1, x+1)+1):
      for col in range(max(0,y-1), min(COLS-1, y+1)+1):
        if (row,col) not in self.clicked:
          self.click(row,col)
    return True
      
  def display_board(self):
    print("Layout of entire Mine Board:")
    for row in self.board_list:
      print(row)



game = Game()
while True: #runs the entire game class in a loop
  game.new()
  game.run()