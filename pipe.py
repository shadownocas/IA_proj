# pipe.py: Template para implementação do projeto de Inteligência Artificial 2023/2024.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 22:
# 106111 Inês Simões
# 104683 Matheus Alves

import sys
import copy
from sys import stdin

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
    
)

WRONG = 0
MAYBE = 1
FINAL = 2
C = 0
B = 1
D = 2
E = 3

class Piece:
    def __init__(self, nome: str):
        type = {"F": 0, "B": 1, "V": 2, "L": 3}
        directions = {"C": 0, "B": 1, "E": 2, "D": 3}
        self.state = WRONG
        self.possibilities = []
        self.cor = 0
        self.coord = []
        self.nome = nome
        if (nome[0] == "L"):
            self.positions = [nome[0] + "H", nome[0] + "V"]
            if (nome[0] == "H"):
                self.dir = (type[nome[0]], 0)
            elif(nome[0] == "V"):
                self.dir = (type[nome[0]], 1)
        else:
            self.positions = [nome[0] + "C", nome[0] + "B", nome[0] + "D", nome[0] + "E"]
            self.dir = (type[nome[0]], directions[nome[1]])
        


class PipeManiaState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.cost = PipeManiaState.state_id
        self.final_pieces = 0
        self.h = 0
        PipeManiaState.state_id += 1

    def __lt__(self, other):
        return self.cost < other.cost
    
    def path_cost(self):
        return self.cost

    def check_possibilities(self, x, y, piece: str):
            if not (self.board.matrix[x][y].possibilities == []):
                return self.board.matrix[x][y].possibilities
            res = list(initial_positions[piece[0]])
            res1 = list(initial_positions[piece[0]])
            last = self.board.tamanho - 1
            if x == 0:
                for pos in res:
                    if not (dict_pos[pos][0] == ""):
                            res1.remove(pos)
            elif x == last:
                for pos in res:
                    if not (dict_pos[pos][1] == ""):
                        if(pos in res1):
                            res1.remove(pos)
            if y == last:
                for pos in res:
                    if not (dict_pos[pos][2] == ""):
                        if(pos in res1):
                            res1.remove(pos)
            elif y == 0:
                for pos in res:
                    if not (dict_pos[pos][3] == ""):
                        if(pos in res1):
                            res1.remove(pos)
                            
            
            self.board.matrix[x][y].possibilities = res1
            self.board.h -= (4 - len(res1))
            return res1


                        
    def check_adj_final(self, stack: list):
        """" !!! 0 = white       1 = gray      2 = black !!!! """
        finals = 0
        side = [C, B, E, D]
        omlll = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        while(len(stack) != 0):
            cur = stack[-1]
            if(cur.cor == 0):
                i = 0
                cur.cor = 1
                horizontal = self.board.adjacent_horizontal_values(cur.coord[0], cur.coord[1])
                pieces = self.board.adjacent_vertical_values(cur.coord[0] , cur.coord[1])
                pieces.append(horizontal[0]) #can prob put at same time/nah you end up with nested lists:(, will try it later
                pieces.append(horizontal[1])
                for side_pieces in pieces :
                    if(side_pieces != ""):  
                        caca = self.board.matrix[cur.coord[0] + omlll[i][0]][cur.coord[1]+omlll[i][1]] #coords of side piece
                        if( caca.state != FINAL):
                            possibli = list(self.check_possibilities(caca.coord[0], caca.coord[1], side_pieces))
                            for possibilities in possibli: #aqui n é do cur
                                if(not isvalid(cur, possibilities,  side[i])):
                                    self.board.h -= 1
                                    caca.possibilities.remove(possibilities)
                            
                        if(len(self.board.matrix[caca.coord[0]][caca.coord[1]].possibilities) == 1 and caca.state != FINAL):
                            #print("piece final: a ser tirada qd adj_final : ", caca.coord[0], caca.coord[1])
                            caca.state = FINAL
                            self.board.p_left.remove([caca.coord[0], caca.coord[1]])
                            stack.append(caca)
                            caca.nome = self.board.matrix[caca.coord[0]][caca.coord[1]].possibilities[0] 
                            self.board.matrix[caca.coord[0]][caca.coord[1]].nome = caca.nome
                            #print("mudou nome final para: ",self.board.matrix[caca.coord[0]][caca.coord[1]].nome )
                    i += 1
                    
            elif(cur.cor == 1):
                    finals += 1
                    cur.cor = 2
                    stack.pop()
            else:
                finals += 1
                stack.pop()

        return finals
        
    def calcs(self):
        #checkar final states e set them on the boarders, clockwise
        finals = 0
        stack = []
        for i in range(self.board.tamanho): 
            if self.board.matrix[0][i].state != FINAL:
                possible = self.check_possibilities(0, i, self.board.matrix[0][i].nome )
                if(len(possible) == 1):
                    self.board.matrix[0][i].nome = possible[0]
                    self.board.matrix[0][i].state = FINAL
                    self.board.p_left.remove([0, i])
                    stack.append(self.board.matrix[0][i])
                    finals += self.check_adj_final(stack)
                else:
                    self.board.matrix[0][i].nome = possible[0]
                    self.board.matrix[0][i].state = MAYBE

        for i in range(1, self.board.tamanho): # dont check first ine of collum, already checked
            if(self.board.matrix[i][- 1].state != FINAL):
                possible = self.check_possibilities(i, self.board.tamanho-1 , self.board.matrix[i][-1].nome )
                if(len(possible) == 1):
                    self.board.matrix[i][-1].nome = possible[0]
                    self.board.matrix[i][-1].state = FINAL
                    self.board.p_left.remove([i, self.board.tamanho - 1])
                    stack.append(self.board.matrix[i][-1])
                    finals += self.check_adj_final(stack)
                else:
                    self.board.matrix[i][-1].nome = possible[0]
                    self.board.matrix[i][-1].state = MAYBE
            
        for i in range(self.board.tamanho - 1, -1, -1):
            size = self.board.tamanho - 1
            if(self.board.matrix[size][i].state != FINAL):
                possible = self.check_possibilities( size, i, self.board.matrix[size][i].nome )
                if(len(possible) == 1):
                    self.board.matrix[size][i].nome = possible[0]
                    self.board.matrix[size][i].state = FINAL
                    self.board.p_left.remove([size, i])
                    stack.append(self.board.matrix[size ][i])
                    finals += self.check_adj_final(stack)
                else:
                    self.board.matrix[size][i].nome = possible[0]
                    self.board.matrix[size][i].state = MAYBE

        for i in range(self.board.tamanho - 1, -1, -1):
            size = self.board.tamanho - 1 
            if(self.board.matrix[i][0].state != FINAL):
                possible = self.check_possibilities(i, 0, self.board.matrix[size ][i].nome )
                if(len(possible) == 1):
                    self.board.matrix[i][0].nome = possible[0]
                    self.board.matrix[i][0].state = FINAL
                    self.board.p_left.remove([i, 0])
                    stack.append(self.board.matrix[i][0])
                    finals += self.check_adj_final(stack)
                else:
                    self.board.matrix[i][0].nome = possible[0]
                    self.board.matrix[i][0].state = MAYBE

        return (self.board, finals)

class Board:
    """Representação interna de um tabuleiro de PipeMania."""
    def __init__(self, board_matrix, tamanho, pieces_left):
        self.matrix = board_matrix
        self.tamanho = tamanho
        self.p_left = pieces_left
        self.h = (tamanho **2) * 4

    
    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.matrix[row][col].nome
    
    def print_board(self):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                #print(self.get_value(i, j), end=" \t")
                print(self.get_value(i, j),  end="\t")
            print("\n", end= "")
           
    def adjacent_vertical_values(self, row: int, col: int):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        if row == 0:
            value1 = ""
        else:
            value1 = str(self.matrix[row-1][col].nome)

        try:
            value2 = str(self.matrix[row+1][col].nome)
        except IndexError:
            value2 = ""
        return [value1, value2]
        
    def adjacent_horizontal_values(self, row: int, col: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if col == 0:
            value1 = ""
        else:
            value1 = str(self.matrix[row][col-1].nome)
        try:
            value2 = str(self.matrix[row][col+1].nome)
        except IndexError:
            value2 = ""

        return [value1, value2]
        

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        board_matrix = []
        pieces_left = []

        # Read the first line from standard input
        line = stdin.readline().split()
        # Convert each piece name into a Piece object and append to board_matrix
        pieces_row = [Piece(piece_name) for piece_name in line]

        # Assign coordinates to each Piece and append the row to board_matrix
        for col in range(len(line)):
            pieces_row[col].coord = [0, col]
            pieces_left.append([0, col])
        board_matrix.append(pieces_row)

        # Read the remaining lines and append Piece objects to board_matrix
        for row in range(1, len(line)):
            line = stdin.readline().split()
            pieces_row = [Piece(piece_name) for piece_name in line]
            
            # Assign coordinates to each Piece and append the row to board_matrix
            for col in range(len(line)):
                pieces_row[col].coord = [row, col]
                pieces_left.append([row, col])
            board_matrix.append(pieces_row)
        
        # Print board_matrix to verify the structure
        return Board(board_matrix, len(line), pieces_left)
        

    # TODO: outros metodos da classe

c = ["BB", "BE", "BD", "VB", "VE", "LV", "FB"]
b = ["BC", "BE", "BD", "VC", "VD", "LV", "FC"]
e = ["BC", "BB", "BD", "VB", "VD", "LH", "FD"]
d = ["BC", "BB", "BE", "VC", "VE", "LH", "FE"]
fc = list(c)
fb = list(b)
fe = list(e)
fd = list(d)
fc.remove("FB")
fb.remove("FC")
fe.remove("FD")
fd.remove("FE")

initial_positions = {"F": ["FC", "FB", "FD", "FE"], "B": ["BC", "BB", "BD", "BE"],
                      "V": ["VC", "VB", "VD", "VE"], "L": ["LH", "LV"]}

dict_pos = {"FC": [fc, "", "", ""], "FB": ["", fb, "", ""], "FE": ["", "", "", fe],
            "FD": ["", "", fd, ""], "BC": [c, "", d, e], "BB": ["", b, d, e],  "BE": [c, b , "", e], "BD": [c, b, d, ""],
            "VC": [c, "", "", e], "VB": ["", b, d, ""], "VE": ["",b, "",  e], "VD": [ c, "", d, ""],                                                                                                                                                                      
            "LH": ["", "", d, e], "LV": [c, b, "", ""]}


def isvalid(piece1: Piece, piece2, direction):
    if (direction == E or direction == B):
        check = direction -1
    else:
        check = direction +1
    hm = True
    if(dict_pos[piece2][check] != ""):
        hm = False
    if (dict_pos[piece1.nome][direction] == "" and hm == True):
        return True
    if(piece2 in dict_pos[piece1.nome][direction]):
        return True
    
    return False

def isvaliddddd(piece1: Piece, piece2, direction):
    if (dict_pos[piece1.nome][direction] == ""):
        return True
    elif(piece2 in dict_pos[piece1.nome][direction]):
        return True
    return False
    
    

class PipeMania(Problem):
    def __init__(self, board: Board):
        self.board = board
        self.initial = None
    
    def get_piece(self, l, c):
        return self.board.matrix[l][c]
    
    def copy_state(self, matrix, p_left, tamanho):
        new_matrix = []
        for i in matrix:
            new_matrix += [i.copy()]
        new_p_left = []
        for i in p_left:
            new_p_left += [i.copy()]
        new_board = Board(new_matrix, tamanho, new_p_left)
        new_state = PipeManiaState(new_board)
        return new_state

    def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        if (len(state.board.p_left) == 0):
            return actions
        coord = state.board.p_left[0]
        p_x = coord[0]
        p_y = coord[1]
        piece_name = state.board.matrix[p_x][p_y].nome
        state.check_possibilities(p_x, p_y, piece_name)
        for possibility in state.board.matrix[p_x][p_y].possibilities:
            actions.append([p_x, p_y, possibility])

        return actions
               
    def result(self, state: PipeManiaState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        p_x = action[0]
        p_y = action[1]
        p_name = action[2]
        new_state = copy.deepcopy(state)
        piece = new_state.board.matrix[p_x][p_y]
        #if(p_name in piece.possibilities):
        piece.possibilities = [p_name]
        piece.nome = p_name
        piece.state = FINAL
        if ([p_x, p_y] in state.board.p_left):
            new_state.board.p_left.remove([p_x, p_y])
        new_state.check_adj_final([piece])
        return new_state
        

    def goal_test(self, state: PipeManiaState):   #CHANGE THIS!!!! we just need to do: tamanho ^2 == state.final_pieces
        #pode dar ciclos fechados.... ex da mati
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema.
        !!! 0 = white       1 = gray      2 = black !!!!
        """
        for i in range(state.board.tamanho): #row
           for j in range(state.board.tamanho): # col
                horizontal = state.board.adjacent_horizontal_values(i, j)
                vertical = state.board.adjacent_vertical_values(i, j)
                if((not isvaliddddd(state.board.matrix[i][j], horizontal[1], D)) or (not isvaliddddd(state.board.matrix[i][j], horizontal[0], E)) or
                   (not isvaliddddd(state.board.matrix[i][j], vertical[1], B)) or (not isvaliddddd(state.board.matrix[i][j], vertical[0], C))):
                    return False
        return True
        #return self.board.h == self.board.tamanho**2
               
                

    def h(self, node: Node):#Node is the same as a pipe mania state in its atribute node.state
        """Função heuristica utilizada para a procura A*."""
        return 1
        

    # TODO: outros metodos da classe
    

        
        
                


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    initial_state = PipeManiaState(board)
    initial_state.calcs()
    """initial_state.board.matrix[0][0].nome = "VC"
    initial_state.board.matrix[0][0].possibilities = ["VC", "VB"]
    initial_state.board.p_left = [[0, 0]]
    initial_state.board.matrix[0][1].nome = "VC"
    initial_state.board.matrix[0][1].possibilities = ["VC", "VE"]
    initial_state.board.p_left.append([0, 1])
    initial_state.board.matrix[1][0].nome = "FD"
    initial_state.board.matrix[1][0].possibilities = ["FC", "FE"]
    initial_state.board.p_left.append([1, 0])"""
    problem = PipeMania(initial_state.board)
    problem.initial = initial_state
    #node = depth_first_tree_search(problem)
    #node = breadth_first_tree_search(problem)
    node = astar_search(problem)
    node.state.board.print_board()
    # Mostrar valor na posição (2, 2):
   
   

   
