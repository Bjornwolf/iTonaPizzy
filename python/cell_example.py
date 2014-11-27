import pygame
import random
from cell_automaton import CellAutomaton

def rule(state, ns):
    rn = random.randint(0,7)
    if rn == 0:
        return random.randint(0,2)
    if ns[1] < 2:
        return 0
    if ns[1] > 3:
        return 0
    if ns[1] == 3 and state == 0:
        return 1
    else:
        return state
        
def rule2(state, ns):
    return random.randint(0,2)
    
def rule3(state, ns):
    rn = random.randint(0,2)
    if rn < 2:
        return state
    ns2 = ns[1:]
    rng = random.randint(0,1)
    if rng == 0:
        return (state + 1) % 3
    else:
        return max(ns) % 3
        
def main():
    size = (40,65)

    board = []
    for i in range(40):
        board.append([(random.randint(0,1), 0) for j in range(40)])
    for i in range(5):
        board.append([(random.randint(0,2), 1) for j in range(40)])    
    for i in range(20):
        board.append([(random.randint(0,2), 2) for j in range(40)])
    print len(board)
        
    pygame.init()
    ca = CellAutomaton(size, board, [rule, rule2, rule3], 2)
    while True:
        screen = pygame.display.set_mode( (size[0] * 10, size[1] * 10) )
        ca.next_state()
        ca.draw(screen)
        pygame.display.update()
if __name__ == "__main__":
    main()

