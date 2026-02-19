#!/usr/bin/env python3
"""
Sequencium Game Implementation with AI Search Algorithm
Based on the game by Walter Joris

This implementation includes:
- Complete game logic
- Minimax search algorithm with Alpha-Beta pruning
- Command-line interface
"""

import sys
from typing import List, Tuple, Optional, Set
from copy import deepcopy
from enum import Enum


class Player(Enum):
    """Enumeration for players"""
    A = 1  # Player A (starts at top-left)
    B = 2  # Player B (starts at bottom-right)


class GameBoard:
    """Represents the Sequencium game board"""
    
    def __init__(self, size: int = 6):
        """
        Initialize the game board
        
        Args:
            size: Size of the square board (default 6x6)
        """
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]
        self.player_positions = {Player.A: set(), Player.B: set()}
        
        # Initialize starting positions
        self.board[0][0] = (Player.A, 1)
        self.player_positions[Player.A].add((0, 0))
        
        self.board[size-1][size-1] = (Player.B, 1)
        self.player_positions[Player.B].add((size-1, size-1))
    
    def get_cell(self, row: int, col: int) -> Optional[Tuple[Player, int]]:
        """Get the value at a cell"""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.board[row][col]
        return None
    
    def set_cell(self, row: int, col: int, player: Player, value: int):
        """Set a cell value"""
        self.board[row][col] = (player, value)
        self.player_positions[player].add((row, col))
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all 8-directional neighbors of a cell"""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    neighbors.append((nr, nc))
        return neighbors
    
    def get_valid_moves(self, player: Player) -> List[Tuple[int, int, int]]:
        """
        Get all valid moves for a player
        
        Returns:
            List of tuples (row, col, value) representing valid moves
        """
        valid_moves = []
        
        # Check all positions owned by the player
        for pos_row, pos_col in self.player_positions[player]:
            _, current_value = self.board[pos_row][pos_col]
            new_value = current_value + 1
            
            # Check all neighbors
            for nr, nc in self.get_neighbors(pos_row, pos_col):
                # If neighbor is empty, it's a valid move
                if self.board[nr][nc] is None:
                    valid_moves.append((nr, nc, new_value))
        
        # Remove duplicates (a cell might be adjacent to multiple player positions)
        # Keep the one with maximum value
        move_dict = {}
        for row, col, value in valid_moves:
            key = (row, col)
            if key not in move_dict or value > move_dict[key]:
                move_dict[key] = value
        
        return [(row, col, value) for (row, col), value in move_dict.items()]
    
    def make_move(self, row: int, col: int, player: Player, value: int) -> bool:
        """
        Make a move on the board
        
        Returns:
            True if move was valid and made, False otherwise
        """
        if self.board[row][col] is not None:
            return False
        
        # Verify this is a valid move
        valid_moves = self.get_valid_moves(player)
        if (row, col, value) not in valid_moves:
            return False
        
        self.set_cell(row, col, player, value)
        return True
    
    def get_max_value(self, player: Player) -> int:
        """Get the maximum value for a player"""
        max_val = 0
        for row, col in self.player_positions[player]:
            _, value = self.board[row][col]
            max_val = max(max_val, value)
        return max_val
    
    def is_game_over(self) -> bool:
        """Check if the game is over"""
        # Game is over if both players have no valid moves
        return (len(self.get_valid_moves(Player.A)) == 0 and 
                len(self.get_valid_moves(Player.B)) == 0)
    
    def get_winner(self) -> Optional[Player]:
        """
        Get the winner of the game
        
        Returns:
            Player.A, Player.B, or None for tie
        """
        max_a = self.get_max_value(Player.A)
        max_b = self.get_max_value(Player.B)
        
        if max_a > max_b:
            return Player.A
        elif max_b > max_a:
            return Player.B
        else:
            return None
    
    def copy(self):
        """Create a deep copy of the board"""
        new_board = GameBoard(self.size)
        new_board.board = deepcopy(self.board)
        new_board.player_positions = deepcopy(self.player_positions)
        return new_board
    
    def __str__(self) -> str:
        """String representation of the board"""
        result = []
        result.append("   " + " ".join(f"{i:2d}" for i in range(self.size)))
        result.append("  +" + "---" * self.size + "+")
        
        for i, row in enumerate(self.board):
            row_str = f"{i:2d}|"
            for cell in row:
                if cell is None:
                    row_str += "  ."
                else:
                    player, value = cell
                    symbol = "A" if player == Player.A else "B"
                    row_str += f"{symbol}{value:1d}" if value < 10 else f"{symbol}{value}"
            row_str += "|"
            result.append(row_str)
        
        result.append("  +" + "---" * self.size + "+")
        return "\n".join(result)


class SequenciumAI:
    """AI player using Minimax with Alpha-Beta pruning"""
    
    def __init__(self, max_depth: int = 4):
        """
        Initialize the AI
        
        Args:
            max_depth: Maximum search depth for minimax
        """
        self.max_depth = max_depth
        self.nodes_evaluated = 0
    
    def evaluate_position(self, board: GameBoard, player: Player) -> float:
        """
        Evaluate the current board position
        
        Heuristic:
        - Primary: max value difference
        - Secondary: number of cells controlled
        - Tertiary: number of valid moves available
        """
        opponent = Player.B if player == Player.A else Player.A
        
        # Max value difference (most important)
        max_diff = board.get_max_value(player) - board.get_max_value(opponent)
        
        # Number of cells controlled
        cell_diff = len(board.player_positions[player]) - len(board.player_positions[opponent])
        
        # Number of valid moves (mobility)
        mobility_diff = len(board.get_valid_moves(player)) - len(board.get_valid_moves(opponent))
        
        # Combined score
        score = max_diff * 100 + cell_diff * 10 + mobility_diff
        
        return score
    
    def minimax(self, board: GameBoard, depth: int, alpha: float, beta: float, 
                maximizing_player: bool, player: Player) -> Tuple[float, Optional[Tuple[int, int, int]]]:
        """
        Minimax algorithm with alpha-beta pruning
        
        Returns:
            Tuple of (score, best_move)
        """
        self.nodes_evaluated += 1
        
        opponent = Player.B if player == Player.A else Player.A
        current_player = player if maximizing_player else opponent
        
        # Terminal conditions
        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board, player), None
        
        valid_moves = board.get_valid_moves(current_player)
        
        if not valid_moves:
            # Current player has no moves, switch to opponent
            return self.minimax(board, depth - 1, alpha, beta, not maximizing_player, player)
        
        best_move = None
        
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                row, col, value = move
                new_board = board.copy()
                new_board.make_move(row, col, current_player, value)
                
                eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, False, player)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                row, col, value = move
                new_board = board.copy()
                new_board.make_move(row, col, current_player, value)
                
                eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, True, player)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval, best_move
    
    def get_best_move(self, board: GameBoard, player: Player) -> Optional[Tuple[int, int, int]]:
        """
        Get the best move for the current player
        
        Returns:
            Tuple (row, col, value) or None if no valid moves
        """
        self.nodes_evaluated = 0
        valid_moves = board.get_valid_moves(player)
        
        if not valid_moves:
            return None
        
        _, best_move = self.minimax(board, self.max_depth, float('-inf'), float('inf'), True, player)
        
        return best_move


def play_game(board_size: int = 6, ai_depth: int = 4, interactive: bool = False):
    """
    Play a complete game of Sequencium
    
    Args:
        board_size: Size of the game board
        ai_depth: Search depth for AI
        interactive: If True, pause between moves
    """
    board = GameBoard(board_size)
    ai = SequenciumAI(max_depth=ai_depth)
    
    current_player = Player.A
    move_count = 0
    
    print("="*50)
    print("SEQUENCIUM GAME")
    print(f"Board Size: {board_size}x{board_size}")
    print(f"AI Search Depth: {ai_depth}")
    print("="*50)
    print()
    
    print("Initial Board:")
    print(board)
    print()
    
    while not board.is_game_over():
        valid_moves = board.get_valid_moves(current_player)
        
        if not valid_moves:
            print(f"Player {current_player.name} has no valid moves. Switching to opponent.")
            current_player = Player.B if current_player == Player.A else Player.A
            continue
        
        move_count += 1
        print(f"\n{'='*50}")
        print(f"Move {move_count}: Player {current_player.name}'s turn")
        print(f"Valid moves available: {len(valid_moves)}")
        
        # Get best move from AI
        best_move = ai.get_best_move(board, current_player)
        
        if best_move:
            row, col, value = best_move
            board.make_move(row, col, current_player, value)
            print(f"AI chooses: Row {row}, Col {col}, Value {value}")
            print(f"Nodes evaluated: {ai.nodes_evaluated}")
            print()
            print(board)
        
        # Switch player
        current_player = Player.B if current_player == Player.A else Player.A
        
        if interactive:
            input("\nPress Enter to continue...")
    
    print("\n" + "="*50)
    print("GAME OVER!")
    print("="*50)
    print()
    print("Final Board:")
    print(board)
    print()
    
    max_a = board.get_max_value(Player.A)
    max_b = board.get_max_value(Player.B)
    
    print(f"Player A maximum value: {max_a}")
    print(f"Player B maximum value: {max_b}")
    print(f"Total moves played: {move_count}")
    print()
    
    winner = board.get_winner()
    if winner:
        print(f"🎉 Winner: Player {winner.name}!")
    else:
        print("🤝 Game ended in a tie!")
    
    print("="*50)
    
    return board, winner


def main():
    """Main entry point"""
    print("""
╔══════════════════════════════════════════════════════════╗
║         SEQUENCIUM - AI Search Algorithm Demo            ║
║              Based on Walter Joris' Game                 ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # Parse command line arguments
    board_size = 6
    ai_depth = 4
    interactive = False
    
    if len(sys.argv) > 1:
        try:
            board_size = int(sys.argv[1])
        except ValueError:
            print("Invalid board size. Using default 6x6.")
    
    if len(sys.argv) > 2:
        try:
            ai_depth = int(sys.argv[2])
        except ValueError:
            print("Invalid AI depth. Using default 4.")
    
    if len(sys.argv) > 3 and sys.argv[3].lower() in ['true', 'yes', '1', 'interactive']:
        interactive = True
    
    print(f"Configuration:")
    print(f"  Board Size: {board_size}x{board_size}")
    print(f"  AI Search Depth: {ai_depth}")
    print(f"  Interactive Mode: {interactive}")
    print()
    
    play_game(board_size, ai_depth, interactive)


if __name__ == "__main__":
    main()
