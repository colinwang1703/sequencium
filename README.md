# Sequencium - AI Search Algorithm Implementation

A command-line implementation of **Sequencium** by Walter Joris, featuring an AI player using Minimax search with Alpha-Beta pruning.

## Game Rules

### Objective
Two players expand their number sequences on a grid board. The player with the highest number at the end wins.

### Setup
- **Board**: Square grid (default 6×6, configurable)
- **Players**: 2 players (A and B)
- **Starting Position**:
  - Player A places `1` in top-left corner (0,0)
  - Player B places `1` in bottom-right corner

### Core Rules
1. **Each Turn**: Choose an empty cell adjacent (8 directions) to any of your numbers
2. **New Number**: Place a number that equals adjacent number + 1
3. **Constraints**:
   - One cell can only contain one number
   - Can only extend from your own numbers
   - Cannot skip turns if valid moves exist
   - Diagonal moves allowed

### Game End
- Game ends when both players have no valid moves
- Winner is the player with the highest number on the board
- Tie if both players have the same maximum number

## Features

- ✅ Complete game logic implementation
- ✅ Minimax search algorithm with Alpha-Beta pruning
- ✅ Configurable board size
- ✅ Configurable AI search depth
- ✅ Command-line interface with visual board display
- ✅ Move analysis and statistics

## Installation

No external dependencies required! Just Python 3.6+

```bash
# Make the script executable
chmod +x sequencium.py
```

## Usage

### Basic Usage
```bash
python3 sequencium.py
```

### With Custom Board Size
```bash
python3 sequencium.py 8  # 8x8 board
```

### With Custom AI Depth
```bash
python3 sequencium.py 6 5  # 6x6 board, depth 5 search
```

### Interactive Mode (pause between moves)
```bash
python3 sequencium.py 6 4 interactive
```

## Command-Line Arguments

```
python3 sequencium.py [board_size] [ai_depth] [interactive]

Arguments:
  board_size  - Size of the square board (default: 6)
  ai_depth    - Search depth for AI algorithm (default: 4)
  interactive - Enable interactive mode (pause after each move)
```

## Example Output

```
╔══════════════════════════════════════════════════════════╗
║         SEQUENCIUM - AI Search Algorithm Demo            ║
║              Based on Walter Joris' Game                 ║
╚══════════════════════════════════════════════════════════╝

Configuration:
  Board Size: 6x6
  AI Search Depth: 4
  Interactive Mode: False

==================================================
SEQUENCIUM GAME
Board Size: 6x6
AI Search Depth: 4
==================================================

Initial Board:
    0  1  2  3  4  5
  +------------------+
 0|A1  .  .  .  .  .|
 1| .  .  .  .  .  .|
 2| .  .  .  .  .  .|
 3| .  .  .  .  .  .|
 4| .  .  .  .  .  .|
 5| .  .  .  .  . B1|
  +------------------+

==================================================
Move 1: Player A's turn
Valid moves available: 3
AI chooses: Row 0, Col 1, Value 2
Nodes evaluated: 1234

    0  1  2  3  4  5
  +------------------+
 0|A1 A2  .  .  .  .|
 1| .  .  .  .  .  .|
 2| .  .  .  .  .  .|
 3| .  .  .  .  .  .|
 4| .  .  .  .  .  .|
 5| .  .  .  .  . B1|
  +------------------+

...

==================================================
GAME OVER!
==================================================

Final Board:
    0  1  2  3  4  5
  +------------------+
 0|A1 A2 A3 A4 A5 A6|
 1|A2 A3 A4 A5 A6 A7|
 2|A3 A4 A5 A6 A7 A8|
 3|B4 B5 B6 B7 A8 A9|
 4|B3 B4 B5 B6 B7 A8|
 5|B2 B3 B4 B5 B6 B7|
  +------------------+

Player A maximum value: 9
Player B maximum value: 7
Total moves played: 34

🎉 Winner: Player A!
==================================================
```

## Algorithm Details

### Search Algorithm
The AI uses **Minimax** with **Alpha-Beta pruning** to find optimal moves.

### Evaluation Function
The position evaluation considers:
1. **Max Value Difference** (weight: 100) - Primary winning condition
2. **Cell Control** (weight: 10) - Number of cells controlled
3. **Mobility** (weight: 1) - Number of valid moves available

### Performance
- Search depth 4: ~1000-5000 nodes per move (fast)
- Search depth 5: ~10000-50000 nodes per move (slower but smarter)
- Search depth 6+: May be slow for larger boards

## Implementation Details

### Key Classes

- **`Player`**: Enum for Player A and Player B
- **`GameBoard`**: Manages the game state, valid moves, and game rules
- **`SequenciumAI`**: Implements Minimax with Alpha-Beta pruning

### Board Representation

The board uses a 2D array where each cell contains:
- `None` for empty cells
- `(Player, value)` tuple for occupied cells

## License

MIT License - See LICENSE file for details

## Author

Implementation by Colin Wang (2026)
Based on Sequencium by Walter Joris
