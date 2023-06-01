import pygame

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

class Game:
  def __init__(self): #initialize the class
    self.screen = pygame.display.set_mode((WIDTH,HEIGHT)) #basic pygame initialization stuff
    pygame.display.set_caption(TITLE)
    self.clock = pygame.time.Clock()
    
  def new(self):
    pass #just for now
    
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
    pygame.display.flip()

game = Game()
while True: #runs the entire game class in a loop
  game.new()
  game.run()