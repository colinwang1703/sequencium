#!/usr/bin/env python3
"""
Performance comparison between Python and C++ implementations
"""

import time
from sequencium import GameBoard, Player, SequenciumAI, CPP_AVAILABLE

def benchmark_search(board_size=6, depth=4, use_cpp=True):
    """Run a benchmark of the search algorithm"""
    board = GameBoard(board_size)
    ai = SequenciumAI(max_depth=depth, use_cpp=use_cpp)
    
    # Make a few moves to get a more interesting position
    moves = [
        (0, 1, Player.A, 2),
        (4, 5, Player.B, 2),
        (1, 1, Player.A, 2),
        (3, 5, Player.B, 3),
    ]
    
    for row, col, player, value in moves:
        board.make_move(row, col, player, value)
    
    start_time = time.time()
    best_move = ai.get_best_move(board, Player.A)
    elapsed = time.time() - start_time
    
    return elapsed, ai.nodes_evaluated, best_move

def run_comparison():
    """Compare Python vs C++ performance"""
    print("=" * 70)
    print("SEQUENCIUM PERFORMANCE COMPARISON")
    print("=" * 70)
    print()
    
    if not CPP_AVAILABLE:
        print("⚠ C++ engine not available. Cannot run comparison.")
        return
    
    configs = [
        (6, 3, "6x6 board, depth 3"),
        (6, 4, "6x6 board, depth 4"),
        (6, 5, "6x6 board, depth 5"),
    ]
    
    for board_size, depth, description in configs:
        print(f"\n{description}")
        print("-" * 70)
        
        # Python implementation
        print("Python implementation:")
        py_time, py_nodes, py_move = benchmark_search(board_size, depth, use_cpp=False)
        print(f"  Time: {py_time:.4f}s")
        print(f"  Nodes evaluated: {py_nodes:,}")
        print(f"  Best move: {py_move}")
        
        # C++ implementation
        print("C++ implementation:")
        cpp_time, cpp_nodes, cpp_move = benchmark_search(board_size, depth, use_cpp=True)
        print(f"  Time: {cpp_time:.4f}s")
        print(f"  Nodes evaluated: {cpp_nodes:,}")
        print(f"  Best move: {cpp_move}")
        
        # Speedup
        speedup = py_time / cpp_time if cpp_time > 0 else 0
        print(f"\n  ⚡ Speedup: {speedup:.2f}x faster")
        print(f"  📊 Node reduction: {py_nodes - cpp_nodes:,} fewer nodes ({100*(1-cpp_nodes/py_nodes):.1f}% reduction)")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    run_comparison()
