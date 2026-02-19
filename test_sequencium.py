#!/usr/bin/env python3
"""
Simple tests for Sequencium game logic
"""

from sequencium import GameBoard, Player, SequenciumAI


def test_board_initialization():
    """Test that board initializes correctly"""
    board = GameBoard(6)
    assert board.size == 6
    assert board.get_cell(0, 0) == (Player.A, 1)
    assert board.get_cell(5, 5) == (Player.B, 1)
    assert board.get_cell(3, 3) is None
    print("✓ Board initialization test passed")


def test_valid_moves():
    """Test valid move generation"""
    board = GameBoard(6)
    
    # Player A should have 3 valid moves from (0,0)
    moves_a = board.get_valid_moves(Player.A)
    assert len(moves_a) == 3
    assert (0, 1, 2) in moves_a or (1, 0, 2) in moves_a or (1, 1, 2) in moves_a
    
    # Player B should have 3 valid moves from (5,5)
    moves_b = board.get_valid_moves(Player.B)
    assert len(moves_b) == 3
    
    print("✓ Valid moves test passed")


def test_make_move():
    """Test making moves"""
    board = GameBoard(6)
    
    # Make a move for Player A
    result = board.make_move(1, 1, Player.A, 2)
    assert result is True
    assert board.get_cell(1, 1) == (Player.A, 2)
    
    # Try to make an invalid move (cell already occupied)
    result = board.make_move(1, 1, Player.B, 2)
    assert result is False
    
    print("✓ Make move test passed")


def test_game_over():
    """Test game over detection"""
    board = GameBoard(2)  # Small board
    
    # Initially not over
    assert board.is_game_over() is False
    
    # Fill the board
    board.make_move(0, 1, Player.A, 2)
    board.make_move(1, 0, Player.B, 2)
    
    # Now should be over
    assert board.is_game_over() is True
    
    print("✓ Game over test passed")


def test_winner_determination():
    """Test winner determination"""
    board = GameBoard(4)
    
    # Make some moves
    board.make_move(0, 1, Player.A, 2)
    board.make_move(1, 0, Player.A, 2)
    board.make_move(1, 1, Player.A, 3)
    
    board.make_move(3, 2, Player.B, 2)
    
    # Player A should have max value 3, Player B has 2
    winner = board.get_winner()
    assert winner == Player.A
    
    print("✓ Winner determination test passed")


def test_ai_basic():
    """Test that AI can find a move"""
    board = GameBoard(6)
    ai = SequenciumAI(max_depth=3)
    
    move = ai.get_best_move(board, Player.A)
    assert move is not None
    assert len(move) == 3  # (row, col, value)
    
    print("✓ AI basic test passed")


def test_board_copy():
    """Test board copying"""
    board = GameBoard(6)
    board.make_move(1, 1, Player.A, 2)
    
    board_copy = board.copy()
    
    # Verify copy has the same state
    assert board_copy.get_cell(1, 1) == (Player.A, 2)
    
    # Verify it's a deep copy
    board_copy.make_move(2, 2, Player.A, 3)
    assert board.get_cell(2, 2) is None
    assert board_copy.get_cell(2, 2) == (Player.A, 3)
    
    print("✓ Board copy test passed")


def run_all_tests():
    """Run all tests"""
    print("Running Sequencium Tests...")
    print("=" * 50)
    
    test_board_initialization()
    test_valid_moves()
    test_make_move()
    test_game_over()
    test_winner_determination()
    test_ai_basic()
    test_board_copy()
    
    print("=" * 50)
    print("All tests passed! ✓")


if __name__ == "__main__":
    run_all_tests()
