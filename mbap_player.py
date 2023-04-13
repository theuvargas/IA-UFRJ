from math import inf
from models.board import Board

class MbapPlayer:
    depth = 3

    def __init__(self, color):
        self.color = color

    def play(self, board):
        moves = board.valid_moves(self.color)
        
        children = []
        for move in moves:
            child = Board(board).board
            child.play(move, self.color)
            children.append(child)

        maximizing = self.color == Board.WHITE

        scores = []
        for child in children:
            scores.append(self.minimax(child, self.depth, not maximizing, -inf, inf))
        
        index = scores.index(max(scores)) if maximizing else scores.index(min(scores))
        
        move_tuples = [(mov.x, mov.y) for mov in moves]
        print(list(zip(move_tuples, scores)), index)
        print('-----------------------------',(moves[index].x, moves[index].y))
        
        return moves[index]

    def mobility(self, board):
        white_mobility = len(board.valid_moves(Board.WHITE))
        black_mobility = len(board.valid_moves(Board.BLACK))

        heuristic = 0
        if white_mobility + black_mobility != 0:
            heuristic = 100 * (white_mobility-black_mobility) / (white_mobility+black_mobility)

        return heuristic

    def player_corner_heuristic(self, board, player):
        heuristic = 0

        corner_moves = [(1, 1), (1, 8), (8, 1), (8, 8)]
        for l, c in corner_moves:
            if board.get_square_color(l, c) == player:
                heuristic += 3
        
        valid_moves = board.valid_moves(player)
        valid_moves = [(move.x, move.y) for move in valid_moves]

        for corner in corner_moves:
            if corner in valid_moves:
                heuristic += 1

        return heuristic

    def corners(self, board):
        heuristic = 0

        white_corners = self.player_corner_heuristic(board, Board.WHITE)
        black_corners = self.player_corner_heuristic(board, Board.BLACK)

        if white_corners + black_corners != 0:
            heuristic = 100 * (white_corners-black_corners) / (white_corners+black_corners)

        return heuristic

    # não implementado
    def stability(self, board):
        heuristic = 0
        return heuristic

    def score(self, board):
        white_score, black_score = board.score()

        return 100 * (white_score-black_score) / (white_score+black_score)

    def evaluate_board(self, board):
        remaining = 64 - sum(board.score())
        if remaining <= 6:
            return self.score(board)
        
        return 0.1 * self.score(board) + 0.2 * self.mobility(board) + 0.7 * self.corners(board)

    def minimax(self, board, depth, maximizing, alpha, beta):
        white_moves = board.valid_moves(Board.WHITE)
        black_moves = board.valid_moves(Board.BLACK)

        if depth == 0 or (len(white_moves) == 0 and len(black_moves) == 0):
            return self.evaluate_board(board)

        if len(white_moves) == 0:
            maximizing = False
        if len(black_moves) == 0:
            maximizing = True

        if maximizing:
            value = -inf

            for move in white_moves:
                child = Board(board).board
                child.play(move, Board.WHITE)
                value = max(value, self.minimax(child, depth - 1, False, alpha, beta))
                
                alpha = max(alpha, value)
                
                if value >= beta:
                    break
            
            return value

        else:
            value = inf

            for move in black_moves:
                child = Board(board).board
                child.play(move, Board.BLACK)
                value = min(value, self.minimax(child, depth - 1, True, alpha, beta))

                beta = min(beta, value)

                if value <= alpha:
                    break
            
            return value
