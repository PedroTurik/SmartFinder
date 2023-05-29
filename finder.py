from queue import PriorityQueue
import pygame as pg
import pyautogui
from MazeGen import Kruskal


WIDTH, HEIGHT = 900, 500
GRID_WIDTH, GRID_HEIGHT = WIDTH//20, HEIGHT//20
WIN = pg.display.set_mode((900, 500))
pg.display.set_caption('Smart Finder')
clock = pg.time.Clock()


class Cell:
    def __init__(self):
        self.clicked = False
        self.color = None


board = [[Cell() for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

start, end = None, None
DARK_BLUE = (0, 26, 77)
LIGHT_BLUE = (98,141,228)
LIGHT_GREY = (64, 64, 64)
DARK_GREY = (164, 164, 164)
BORDO = (112,0,0)

def get_neighbors(y, x):
    for yi, xi in [(y-1, x), (y+1, x), (y, x+1), (y, x-1)]:
        if 0 <= yi < GRID_HEIGHT and 0 <= xi < GRID_WIDTH:
            yield (yi, xi)


def refresh():
    global start, end
    start, end = None, None
    for row in board:
        for cell in row:
            cell.color = None
            cell.clicked = False


def BFS_DFS(type):
    index = -type
    global start, end
    if not start or not end:
        pyautogui.alert("You havent set your start and end points")
        return
    else:
        seen = set()
        seen.add(start)
        queue = [(start, 0)]
        board[end[0]][end[1]].clicked = False
        run = True
        explore = -1
        while queue:
            if not run: break
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            clock.tick(60)
            explore += 1
            cur, steps = queue.pop(index)
            board[cur[0]][cur[1]].color = BORDO
            if end == cur:
                pyautogui.alert(f"Found the target in a path of {steps} blocks! {explore} blocks were investigated in total")
                break

            for yk, xk in get_neighbors(cur[0], cur[1]):
                if not board[yk][xk].clicked and (yk, xk) not in seen:
                    seen.add((yk, xk))
                    queue.append(((yk, xk), steps+1))


            for y, rowOfCells in enumerate(board):
                for x, cell in enumerate(rowOfCells):
                    if (y, x) in (start, end):
                        color = DARK_BLUE
                    elif cell.color:
                        color = cell.color
                    else:
                        color = LIGHT_GREY if cell.clicked else DARK_GREY
                    pg.draw.rect(WIN, color, (x*20+1, y*20+1, 18, 18))
            pg.display.update()
        else:
            pyautogui.alert(f"Its impossible to find the target")
        
        refresh()

def man(pos, end):
    return abs(pos[0] - end[0]) + abs(pos[1] - end[1])

def A_star():
    global start, end
    if not start or not end:
        pyautogui.alert("You havent set your start and end points")
        return
    else:
        seen = set()
        heap = PriorityQueue()
        heap.put((man(start, end), 0, start))
        board[end[0]][end[1]].clicked = False
        run = True
        explore = -1
        while not heap.empty():
            if not run: break
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            clock.tick(60)
            explore += 1
            _, steps, cur = heap.get()
            board[cur[0]][cur[1]].color = BORDO
            if end == cur:
                pyautogui.alert(f"Found the target in a path of {steps} blocks! {explore} blocks were investigated in total")
                break

            for yk, xk in get_neighbors(cur[0], cur[1]):
                if not board[yk][xk].clicked and (yk, xk) not in seen:
                    seen.add((yk, xk))
                    heap.put((5*(man((yk, xk), end))+steps+1, steps+1, (yk, xk)))

            for y, rowOfCells in enumerate(board):
                for x, cell in enumerate(rowOfCells):
                    if (y, x) in (start, end):
                        color = DARK_BLUE
                    elif cell.color:
                        color = cell.color
                    else:
                        color = LIGHT_GREY if cell.clicked else DARK_GREY
                    pg.draw.rect(WIN, color, (x*20+1, y*20+1, 18, 18))
            pg.display.update()
        else:
            pyautogui.alert(f"Its impossible to find the target")
        
        refresh()

def Maze():
    refresh()
    maze = Kruskal(GRID_HEIGHT, GRID_WIDTH).generate()
    for i, row in enumerate(maze):
        for j, n in  enumerate(row):
            board[i][j].clicked = (True if n else False)



def main():
    global start, end
    run = True
    while run:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif pg.mouse.get_pressed()[0]:
                col, row = pg.mouse.get_pos()
                board[row//20][col//20].clicked = True

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if not start:
                        start = (event.pos[1] // 20, event.pos[0] // 20)
                    else:
                        end = (event.pos[1] // 20, event.pos[0] // 20)

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_b:
                    BFS_DFS(0)
                elif event.key == pg.K_d:
                    BFS_DFS(1)
                elif event.key == pg.K_a:
                    A_star()
                elif event.key == pg.K_m:
                    Maze()
                elif event.key == pg.K_r:
                    refresh()

        for y, rowOfCells in enumerate(board):
            for x, cell in enumerate(rowOfCells):
                if (y, x) in (start, end):
                    color = DARK_BLUE
                else:
                    color = LIGHT_GREY if cell.clicked else DARK_GREY
                pg.draw.rect(WIN, color, (x*20+1, y*20+1, 18, 18))
        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()
