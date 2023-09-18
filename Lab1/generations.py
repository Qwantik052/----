from typing import Tuple
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys
from PIL import Image as im

class Cell:
    def __init__(self, id : int, health: int = 0, iflife: int = 0) -> None:
        self.health = health
        self.iflife = iflife
        self.id = id

    def set(self, new_health: int = 0, new_iflife : int = 0) -> None:
        self.health = new_health
        self.iflife = new_iflife

class Grid:
    def __init__(self, size : int = 0) -> None:
        self.size = size
        self.field: list[Cell] = []
        for i in range(size * size):
            self.field.append(Cell(i))
        
def alive_neighbours(cell : Cell, grid: Grid) -> int:
    res = 0
    if cell.id % grid.size != 0: 
        if grid.field[cell.id - 1].iflife == 1:
            res += 1
    if cell.id % grid.size != grid.size - 1: 
        if grid.field[cell.id + 1].iflife == 1:
            res += 1
    if cell.id - grid.size > 0:
        if grid.field[cell.id - grid.size].iflife == 1:
            res += 1
    if cell.id + grid.size < grid.size * grid.size:
        if grid.field[cell.id + grid.size].iflife == 1:
            res += 1
    if cell.id % grid.size != 0 and cell.id - grid.size > 0:
        if grid.field[cell.id - 1 - grid.size].iflife == 1:
            res += 1
    if cell.id % grid.size != 0 and cell.id + grid.size < grid.size * grid.size:
        if grid.field[cell.id - 1 + grid.size].iflife == 1:
            res += 1
    if cell.id % grid.size != grid.size - 1 and cell.id - grid.size > 0:
        if grid.field[cell.id + 1 - grid.size].iflife == 1:
            res += 1
    if cell.id % grid.size != grid.size - 1 and cell.id + grid.size < grid.size * grid.size:
        if grid.field[cell.id + 1 + grid.size].iflife == 1:
            res += 1
    return res

class Game:
    def __init__(self, size : int, rule_s : list[int], rule_b: list[int], rule_c: list[int], alive_cells: list[int] = []) -> None:
        self.rule_s = rule_s
        self.rule_b = rule_b
        self.rule_c = rule_c
        self.size = size
        self.grid = Grid(size)
        for i in alive_cells:
            self.grid.field[i].set(self.rule_c, 1)
        self.iterations: list[Grid] = []
        self.iterations.append(self.grid)

    def next_iteration(self) -> None:
        current_iteration = deepcopy(self.iterations[-1])
        new_iteration = deepcopy(current_iteration)
        for i in range(current_iteration.size * current_iteration.size):
            if current_iteration.field[i].iflife == 1:
                if alive_neighbours(current_iteration.field[i], current_iteration) not in self.rule_s:
                    new_iteration.field[i].set(max(0, current_iteration.field[i].health - 1), 0)
                else: 
                    pass
            elif current_iteration.field[i].iflife == 0:
                if current_iteration.field[i].health == 0 and alive_neighbours(current_iteration.field[i], current_iteration) in self.rule_b:
                    new_iteration.field[i].set(self.rule_c, 1)
                elif current_iteration.field[i].health != 0:
                    new_iteration.field[i].set(max(0, current_iteration.field[i].health - 1), 0)
        self.iterations.append(new_iteration)

    def get_current_iteration(self) -> Grid:
        return self.iterations[-1]
    
    def count(self, amount_of_iterations) -> None:
        for i in amount_of_iterations:
            self.next_iteration()
    
def show_grid(grid: Grid) -> None:
    tmp = []
    for cell in grid.field:
        tmp.append(cell.health)
    data = np.reshape(tmp, (grid.size, grid.size))
    fig, ax = plt.subplots()
    i = ax.imshow(data)
    plt.show()
    # fig.colorbar(i)

def save(grid : Grid, name: str) -> None:
    tmp = []
    for cell in grid.field:
        tmp.append(cell.health)
    data = np.reshape(tmp, (grid.size, grid.size))
    fig, ax = plt.subplots()
    i = ax.imshow(data)
    fig.savefig(name + '.PNG',dpi=250)
    im.open(name + ".PNG").save(name + ".bmp")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: " + sys.argv[0] + "amount of iterations" + "if save?[0/1] +" + "Name of th file")
        exit(1)
    game = Game(50, [2], [2], 25, [1224, 1274, 1275])
    for i in range(int(sys.argv[1])):
        show_grid(game.get_current_iteration())
        game.next_iteration()
    if(int(sys.argv[2]) == 1):
        save(game.get_current_iteration(), sys.argv[3])