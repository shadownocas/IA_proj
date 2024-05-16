stack = [[0,0]]
            for i in range(state.board.tamanho):
                while(stack != []):
                    #check if outside board, we can prob take it out
                    if(stack[-1][0] < 0 or stack[-1][1] < 0 or stack[-1][0]  > state.board.tamanho-1 or stack[-1][1] > state.board.tamanho-1 ):
                        return False
                    if(state.board.board[stack[-1][0]][stack[-1][1]].cor == 0):
                        current = state.board.board[stack[-1][0]][stack[-1][1]]
                        current.cor = 1
                        cur_pos = stack[-1]
                        for j in range(len(current.dir)):
                            stack.append([current.dir[j][0] + cur_pos[0], current.dir[j][1] + cur_pos[1]])
                    elif(state.board.board[stack[-1][0]][stack[-1][1]].cor == 1):
                        state.board.board[stack[-1][0]][stack[-1][1]].cor = 2
                        pieces += 1
                        stack.pop()
                    else:
                        pieces += 1
                        stack.pop()
            if(pieces < state.board.tamanho * state.board.tamanho):
                return False
            return True