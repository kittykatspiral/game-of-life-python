import pygame
pygame.init()
BG_COLOR=(40,15,75)
WIDTH=600
HEIGHT=600
FPS=60
GAME_WINDOW=pygame.display.set_mode((WIDTH,HEIGHT))
CELL_SIZE=30

def draw():
    GAME_WINDOW.fill(BG_COLOR)
    [pygame.draw.line(GAME_WINDOW, (100, 100, 255), (0, y), (WIDTH, y)) for y in range(0, HEIGHT, CELL_SIZE)]
    pygame.draw.line(GAME_WINDOW,(100,100,255),(HEIGHT-1,0),(HEIGHT-1,WIDTH-1))
    [pygame.draw.line(GAME_WINDOW, (100, 100, 255), (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, CELL_SIZE)]
    pygame.draw.line(GAME_WINDOW, (100, 100, 255), (0,WIDTH-1), (HEIGHT-1,WIDTH-1))
    pygame.display.update()
##### NON PYGAME #####
class Cell:
    def __init__(self,value,i,j):
        self.value=value
        self.i=i
        self.j=j

def create_board(lines,columns):
    cell_board=[]
    for i in range(lines):
        new_line=[]
        for j in range(columns):
            new_cell=Cell(0,i,j)
            new_line.append(new_cell)
        cell_board.append(new_line)
    return cell_board


def count_neighbours(cell,board):
    neighbour_count=0
    for row_index in range(cell.i-1,cell.i+2):
        if row_index>=0 and row_index<len(board):
            for column_index in range(cell.j-1,cell.j+2):
                if column_index>=0 and column_index<len(board[0]):
                    if board[row_index][column_index].value in [1,3] and [row_index,column_index]!=[cell.i,cell.j]:
                        neighbour_count+=1
    return neighbour_count

def CODE_code(board):
    for row in board:
        for cell in row:
            neighbour_no=count_neighbours(cell,board)
            if cell.value==0:
                if neighbour_no==3:
                    cell.value=2
            elif cell.value==1:
                if neighbour_no not in [2,3]:
                    cell.value=3
def decode_code(board):
    for row in board:
        for cell in row:
            if cell.value==2:
                cell.value=1
            elif cell.value==3:
                cell.value=0

def next_generation(board):
    CODE_code(board)
    decode_code(board)

#### BACK TO PYGAME ####
def revive_on_click(BOARD):
    if pygame.mouse.get_pressed()[0]:
        pos=pygame.mouse.get_pos()
        i=pos[0]//CELL_SIZE
        j=pos[1]//CELL_SIZE
        pygame.draw.rect(GAME_WINDOW,(255,255,255),(i*CELL_SIZE+1,j*CELL_SIZE+1,CELL_SIZE-1,CELL_SIZE-1))
        BOARD[i][j].value=1
    pygame.display.update()

def board_update(board):  #<-----works
    for row in board:
        for cell in row:
            if cell.value==1:
                pygame.draw.rect(GAME_WINDOW, (255, 255, 255),(cell.i * CELL_SIZE + 1, cell.j * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1))
            elif cell.value==0:
                pygame.draw.rect(GAME_WINDOW, (40,15,75),(cell.i * CELL_SIZE + 1, cell.j * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1))
    pygame.display.update()

def game_of_life(board):
        next_generation(board)
        board_update(board)

GameOfLife=pygame.USEREVENT+1
pygame.time.set_timer(GameOfLife,2000)

def main():
    running=True
    clock= pygame.time.Clock()
    BOARD=create_board(HEIGHT//CELL_SIZE,WIDTH//CELL_SIZE)
    draw()
    while running:
        clock.tick(FPS)
        revive_on_click(BOARD)
        for event in pygame.event.get():
            if event.type == GameOfLife:
                game_of_life(BOARD)
            if event.type == pygame.QUIT:
                running=False

    pygame.quit()

if __name__=='__main__':
    main()

