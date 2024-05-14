def actions(self, state: PipeManiaState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        actions = []
        for coord in state.board.p_left:
            p_x = coord[0]
            p_y = coord[1]
            piece_name = state.board.matrix[p_x][p_y].nome
            state.check_possibilities(p_x, p_y, piece_name)
            for possibility in state.board.matrix[p_x][p_y].possibilities:
                actions.append([p_x, p_y, possibility])
        print("These are the possible actions", actions)
        return actions