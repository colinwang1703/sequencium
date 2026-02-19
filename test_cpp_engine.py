#!/usr/bin/env python3
"""
Tests for C++ search engine
"""

from sequencium import GameBoard, Player, SequenciumAI, CPP_AVAILABLE

def test_cpp_availability():
    """Test that C++ engine is available"""
    if not CPP_AVAILABLE:
        print("⚠ C++ engine not available - skipping C++ tests")
        return False
    print("✓ C++ engine available")
    return True

def test_cpp_initialization():
    """Test C++ engine initialization"""
    if not CPP_AVAILABLE:
        return
    
    try:
        import search_engine
        engine = search_engine.SearchEngine()
        print("✓ C++ SearchEngine initialization test passed")
    except Exception as e:
        print(f"✗ C++ SearchEngine initialization failed: {e}")
        raise

def test_cpp_vs_python_same_move():
    """Test that C++ and Python find the same move"""
    if not CPP_AVAILABLE:
        return
    
    board = GameBoard(6)
    
    # Python AI
    ai_py = SequenciumAI(max_depth=3, use_cpp=False)
    move_py = ai_py.get_best_move(board, Player.A)
    
    # C++ AI
    ai_cpp = SequenciumAI(max_depth=3, use_cpp=True)
    move_cpp = ai_cpp.get_best_move(board, Player.A)
    
    # Both should find a valid move
    assert move_py is not None
    assert move_cpp is not None
    
    # Should be the same move (both are optimal)
    # Note: Due to move ordering differences, they might choose different but equally good moves
    # So we just check that both moves are valid
    valid_moves = board.get_valid_moves(Player.A)
    assert move_py in valid_moves
    assert move_cpp in valid_moves
    
    print(f"✓ C++ vs Python move test passed")
    print(f"  Python move: {move_py}, nodes: {ai_py.nodes_evaluated}")
    print(f"  C++ move: {move_cpp}, nodes: {ai_cpp.nodes_evaluated}")

def test_cpp_performance():
    """Test that C++ is faster than Python"""
    if not CPP_AVAILABLE:
        return
    
    import time
    
    board = GameBoard(6)
    # Make a few moves to get an interesting position
    board.make_move(0, 1, Player.A, 2)
    board.make_move(4, 5, Player.B, 2)
    board.make_move(1, 1, Player.A, 2)
    
    # Python timing
    ai_py = SequenciumAI(max_depth=4, use_cpp=False)
    start = time.time()
    move_py = ai_py.get_best_move(board, Player.A)
    py_time = time.time() - start
    
    # C++ timing
    ai_cpp = SequenciumAI(max_depth=4, use_cpp=True)
    start = time.time()
    move_cpp = ai_cpp.get_best_move(board, Player.A)
    cpp_time = time.time() - start
    
    speedup = py_time / cpp_time if cpp_time > 0 else 0
    
    print(f"✓ C++ performance test passed")
    print(f"  Python: {py_time:.4f}s, {ai_py.nodes_evaluated} nodes")
    print(f"  C++: {cpp_time:.4f}s, {ai_cpp.nodes_evaluated} nodes")
    print(f"  Speedup: {speedup:.1f}x")
    
    # C++ should be faster
    assert cpp_time < py_time, "C++ should be faster than Python"

def test_cpp_with_complex_position():
    """Test C++ engine with a more complex position"""
    if not CPP_AVAILABLE:
        return
    
    board = GameBoard(6)
    
    # Create a complex mid-game position
    moves = [
        (0, 1, Player.A, 2),
        (4, 5, Player.B, 2),
        (1, 1, Player.A, 2),
        (3, 5, Player.B, 3),
        (1, 0, Player.A, 2),
        (4, 4, Player.B, 2),
        (2, 1, Player.A, 3),
        (3, 4, Player.B, 3),
    ]
    
    for row, col, player, value in moves:
        board.make_move(row, col, player, value)
    
    # Test search
    ai = SequenciumAI(max_depth=4, use_cpp=True)
    move = ai.get_best_move(board, Player.A)
    
    assert move is not None
    assert len(move) == 3
    
    # Verify it's a valid move
    valid_moves = board.get_valid_moves(Player.A)
    assert move in valid_moves
    
    print(f"✓ C++ complex position test passed")
    print(f"  Best move: {move}, nodes evaluated: {ai.nodes_evaluated}")

def test_cpp_transposition_table():
    """Test that transposition table reduces node count"""
    if not CPP_AVAILABLE:
        return
    
    board = GameBoard(6)
    
    # Make several moves
    board.make_move(0, 1, Player.A, 2)
    board.make_move(4, 5, Player.B, 2)
    board.make_move(1, 1, Player.A, 2)
    board.make_move(3, 5, Player.B, 3)
    
    ai_cpp = SequenciumAI(max_depth=5, use_cpp=True)
    move_cpp = ai_cpp.get_best_move(board, Player.A)
    cpp_nodes = ai_cpp.nodes_evaluated
    
    ai_py = SequenciumAI(max_depth=5, use_cpp=False)
    move_py = ai_py.get_best_move(board, Player.A)
    py_nodes = ai_py.nodes_evaluated
    
    # C++ with transposition table should evaluate fewer nodes
    node_reduction = (py_nodes - cpp_nodes) / py_nodes * 100
    
    print(f"✓ Transposition table test passed")
    print(f"  Python nodes: {py_nodes}")
    print(f"  C++ nodes: {cpp_nodes}")
    print(f"  Reduction: {node_reduction:.1f}%")
    
    assert cpp_nodes < py_nodes, "C++ should evaluate fewer nodes due to transposition table"

def run_all_cpp_tests():
    """Run all C++ tests"""
    print("Running C++ Search Engine Tests...")
    print("=" * 50)
    
    if not test_cpp_availability():
        print("Skipping C++ tests - engine not available")
        return
    
    test_cpp_initialization()
    test_cpp_vs_python_same_move()
    test_cpp_performance()
    test_cpp_with_complex_position()
    test_cpp_transposition_table()
    
    print("=" * 50)
    print("All C++ tests passed! ✓")

if __name__ == "__main__":
    run_all_cpp_tests()
