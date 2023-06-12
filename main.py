import pygame
import os
import random


#important global variables
TILE_SIZE = 20
ROWS = 20
COLS = 20
NUM_MINES = 99
FPS = 30
WIDTH = TILE_SIZE*ROWS
HEIGHT = TILE_SIZE*COLS
TITLE = "MINESWEEPER" 
game_state = "start menu"

#pygame colors
BACKGROUND_COLOR = (40, 40, 40)


#put all clue images in assets folder into an array
tile_numbers = []
for i in range(1,8):
  tile_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join("tile_assets", f"Tile{i}.png")),(TILE_SIZE,TILE_SIZE)))

#put all other sprites into their own independant variables
tile_empty = pygame.transform.scale(pygame.image.load(os.path.join("tile_assets","TileEmpty.png")),(TILE_SIZE,TILE_SIZE))
tile_exploded = pygame.transform.scale(pygame.image.load(os.path.join("tile_assets","TileExploded.png")),(TILE_SIZE,TILE_SIZE))
tile_flag = pygame.transform.scale(pygame.image.load(os.path.join("tile_assets","TileFlag.png")),(TILE_SIZE,TILE_SIZE))
tile_mine = pygame.transform.scale(pygame.image.load(os.path.join("tile_assets","TileMine.png")),(TILE_SIZE,TILE_SIZE))
tile_not_mine = pygame.transform.scale(pygame.image.load(os.path.join("tile_assets","TileNotMine.png")),(TILE_SIZE,TILE_SIZE))
tile_unknown = pygame.transform.scale(pygame.image.load(os.path.join("tile_assets","TileUnknown.png")),(TILE_SIZE,TILE_SIZE))

#initialize start screen images
start_image_one = pygame.transform.scale(pygame.image.load(os.path.join("start_images","minesweeper_start_1.png")),(TILE_SIZE*6,TILE_SIZE*6))
start_image_two = pygame.transform.scale(pygame.image.load(os.path.join("start_images","minesweeper_start_2.png")),(TILE_SIZE*4,TILE_SIZE*4))





#game class where the entire thing will be run
class Game:
  def __init__(self): #initialize pygame stuff
    self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) 
    pygame.font.init()
    pygame.display.set_caption(TITLE)
    self.clock = pygame.time.Clock()
    self.sec = 0 #timer

  def new(self): #creates a new board
    self.board = Board()
    self.board.display_board() #prints the board in console for testing
  def run(self): #game loop 
    global game_state
    global ROWS
    global COLS
    global NUM_MINES
    self.playing = True
    while self.playing:
      if game_state == "start menu": #start menu
        pygame.display.set_caption(TITLE)
        self.draw_start_menu() #call draw menu function
        for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: #easy
              ROWS = 9
              COLS = 9
              NUM_MINES = 10
              self.new()
              game_state = "game"
            if event.key == pygame.K_2: #medium
              ROWS = 15
              COLS = 15
              NUM_MINES = 30
              self.new()
              game_state = "game"
            if event.key == pygame.K_3: #hard
              ROWS = 20
              COLS = 20
              NUM_MINES = 50
              self.new() 
              game_state = "game"
      elif game_state == "game":
        self.clock.tick(FPS)
        self.ingame_clock()
        self.events() 
        self.draw() 
    else:
      self.end_screen()
    
  def ingame_clock(self): #in game clock 
    self.sec += 1 #every frame add one
    pygame.display.set_caption(TITLE + "  Time:" + str(self.sec // FPS)) #divide by fps to find seconds
    
  def draw_start_menu(self): #draws the menu
    global TITLE
    global TILE_SIZE
    self.screen.fill((255, 255, 255))
    self.font = pygame.font.SysFont('arial', TILE_SIZE)
    self.start_title = self.font.render('Minesweeper - Ross Wen Final Project', True, (0, 0, 0))
    self.start_level1 = self.font.render('Press [1] for Easy', True, (0, 0, 0))
    self.start_level2 = self.font.render('Press [2] for Medium', True, (0, 0, 0))
    self.start_level3 = self.font.render('Press [3] for Hard', True, (0, 0, 0))
    self.start_return = self.font.render('Press J to return to Menu', True, (0, 0, 0))
    self.screen.blit(self.start_title, (WIDTH/2 - self.start_title.get_width()/2, HEIGHT/2 - self.start_title.get_height()))
    self.screen.blit(self.start_level1, (WIDTH/2 - self.start_level1.get_width()/2, HEIGHT/2 + self.start_level1.get_height()/10))
    self.screen.blit(self.start_level2, (WIDTH/2 - self.start_level2.get_width()/2, HEIGHT/2 + self.start_level2.get_height()))
    self.screen.blit(self.start_level3, (WIDTH/2 - self.start_level3.get_width()/2, HEIGHT/2 + self.start_level3.get_height()*2))
    self.screen.blit(self.start_return, (WIDTH/2 - self.start_return.get_width()/2, HEIGHT/2 + self.start_return.get_height()*3))
    self.screen.blit(start_image_one, (HEIGHT*0.3645, WIDTH*0.1041))
    self.screen.blit(start_image_two, (HEIGHT*0.1041, WIDTH*0.7291))
    pygame.display.update()
    
  #game events
  def events(self):
      global game_state
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
                for row in self.board.board_list: #
                  for tile in row:
                    if tile.flagged and tile.type != "B": #if what you flagged is not a bomb then display image
                      tile.flagged = False
                      tile.revealed = True
                      tile.image = tile_not_mine
                    elif tile.type == "B": #reveal all bombs on the map
                      tile.revealed = True
                pygame.display.set_caption("YOU LOSE!") 
                self.playing = False #stop the loop and goes to the end_screen()function
                

          #if right click
          if event.button == 3:
            if not self.board.board_list[mx][my].revealed: #make sure its not revealed, if it is then do nothign
              if self.board.board_list[mx][my].flagged: #if flagged, then turn unflag, if not flagged, then turn flagged
                self.board.board_list[mx][my].flagged = False
              elif not self.board.board_list[mx][my].flagged:
                self.board.board_list[mx][my].flagged = True

          if self.win_check(): #if player wins
            self.win = True
            self.playing = False
            for row in self.board.board_list: #flag all bombs
              for tile in row:
                if not tile.revealed:
                  tile.flagged = True
            pygame.display.set_caption("YOU WIN! TIME:" + str(self.sec // FPS)) #displays how much time it took to win

        if event.type == pygame.KEYDOWN: #return to menu
          if event.key == pygame.K_j:
            self.sec = 0
            game_state = "start menu"
              
  def win_check(self): #function to check if user has won
    for row in self.board.board_list: #goes through grid and checks if every tile except bombs have been revealed
      for tile in row:
        if tile.type != "B" and not tile.revealed:
          return False
    return True
  
  def end_screen(self): #end screen to pause the loop 
    global game_state
    while True:
      for event in pygame.event.get(): #quit
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)
        if event.type == pygame.MOUSEBUTTONDOWN: #restarts game
            self.sec = 0
            return
        if event.type == pygame.KEYDOWN: #goes back to menu
            if event.key == pygame.K_j:
              self.sec = 0
              game_state = "start menu"
              return
          
  def draw(self): #draw game
    self.screen.fill(BACKGROUND_COLOR)
    self.board.draw(self.screen)
    pygame.display.flip()

  def write_best_time(self): #future function to write best times for each level by writing into a file
    self.filehandle = open("timeScores.txt",'w')
    pass

  def read_best_time(self): #read from the file
    pass

#tile class for tiles
#four different types for the tiles
#unknown = "."
#clue = "C"
#bomb = "B"
#empty

class Tile:
  def __init__(self, x, y, image, type, revealed = False, flagged = False): #initializes each individual tile
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

  #make sure that the display board function prints correctly
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
    self.clicked = [] #list for the tiles that the player has clicked

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

  def place_clues(self): #places clues
    for x in range(ROWS): 
      for y in range(COLS):
        if self.board_list[x][y].type != "B": 
          total_mines = self.neighbor_check(x,y) #calls neighbor check function
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
            total_mines += 1 #if inside grid, and has bomb then add to counter
    return total_mines #returns mines around tile

  def click(self, x, y): #click function
    self.clicked.append((x,y)) #adds to clicked[] list
    if self.board_list[x][y].type == "B": #if its a bomb
      self.board_list[x][y].revealed = True 
      self.board_list[x][y].image = tile_exploded
      return False #return false, so player loses
    elif self.board_list[x][y].type == "C": #reveal clue
      self.board_list[x][y].revealed = True
      return True #return true means its not a bomb
      
    self.board_list[x][y].revealed = True #if not clue and not bomb, reveal tile

    for row in range(max(0,x-1), min(ROWS-1, x+1)+1): #recurse through entire grid to find clues and reveal all empty tiles
      for col in range(max(0,y-1), min(COLS-1, y+1)+1):
        if (row,col) not in self.clicked:
          self.click(row,col) #recurse
    return True #return true, no bomb
      
  def display_board(self): #prints out board in console
    print("Layout of entire Mine Board:")
    for row in self.board_list:
      print(row)



game = Game()
while True: #runs the entire game class in a loop
  game.run()
  game.new()