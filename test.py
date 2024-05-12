def check_possibilities(self, x, y, piece):
        #convinha verificar com nome.. ( piece is string)
        #Check just if you need to remove the directions, retorna list/tuplo
        res = initial_positions[piece[0]]
        last = self.board.tamanho - 1
        if x == 0:
            for pos in res:
                if not (dict_pos[pos][0] == ""):
                    res.remove(pos)
        elif x == last:
            for pos in res:
                if not (dict_pos[pos][1] == ""):
                    res.remove(pos) 
        if y == last:
            for pos in res:
                if not (dict_pos[pos][2] == ""):
                    res.remove(pos)
        elif y == 0:
            for pos in res:
                if not (dict_pos[pos][3] == ""):
                    res.remove(pos)
        print("Whats left :", res)
        return res
