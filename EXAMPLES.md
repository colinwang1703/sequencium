# Example Game Outputs

This file contains example outputs from running the Sequencium game with different configurations.

## Example 1: 4x4 Board (Quick Game)

```bash
$ python3 sequencium.py 4 4
```

**Result:** Player A wins with maximum value 7 vs Player B's 6

```
Final Board:
    0  1  2  3
  +------------+
 0|A1A7A6A7|
 1|B5A2A3A5|
 2|B4B3B2A4|
 3|B6B5B6B1|
  +------------+

Player A maximum value: 7
Player B maximum value: 6
Total moves played: 14
🎉 Winner: Player A!
```

## Example 2: 6x6 Board with Depth 3 (Balanced Game)

```bash
$ python3 sequencium.py 6 3
```

**Result:** Tie game, both players reached 17

```
Final Board:
    0  1  2  3  4  5
  +------------------+
 0|A1B13B14B15B16A17|
 1|B12A2B6B5A16B17|
 2|B11B7A3A4B4A15|
 3|B8B10A7B3A5A14|
 4|B9A9A8A6B2A13|
 5|B10A11A10A11A12B1|
  +------------------+

Player A maximum value: 17
Player B maximum value: 17
Total moves played: 34
🤝 Game ended in a tie!
```

## Example 3: 6x6 Board with Depth 4 (Strategic Play)

```bash
$ python3 sequencium.py 6 4
```

**Result:** Tie game, both players reached 10

```
Final Board:
    0  1  2  3  4  5
  +------------------+
 0|A1A3A5B6A7A9|
 1|B7A2B5A4A6A8|
 2|B8B6A3B4A5A7|
 3|B10B7A9B3A6B3|
 4|B9B8A8A7B2B4|
 5|A10A9A10B3B5B1|
  +------------------+

Player A maximum value: 10
Player B maximum value: 10
Total moves played: 34
🤝 Game ended in a tie!
```

## Example 4: 8x8 Board (Larger Game)

```bash
$ python3 sequencium.py 8 3
```

**Result:** Longer game with more strategic depth

The 8x8 board provides more room for maneuvering and typically results in higher maximum values (often 20+).

## Performance Metrics

### Nodes Evaluated by Search Depth

| Board Size | Depth | Avg Nodes/Move | Game Duration |
|------------|-------|----------------|---------------|
| 4x4        | 3     | ~50-200        | ~10 seconds   |
| 4x4        | 4     | ~100-500       | ~15 seconds   |
| 6x6        | 3     | ~200-2000      | ~20 seconds   |
| 6x6        | 4     | ~1000-20000    | ~45 seconds   |
| 8x8        | 3     | ~200-1500      | ~35 seconds   |
| 8x8        | 4     | ~1000-15000    | ~90 seconds   |

### Strategy Notes

The AI's evaluation function considers:

1. **Maximum Value Difference** (most important)
   - Directly affects the winning condition
   - Weight: 100

2. **Territory Control**
   - Number of cells controlled
   - Weight: 10

3. **Mobility**
   - Number of available moves
   - Weight: 1

As the search depth increases, the AI plays more strategically:
- Depth 2-3: Focuses on immediate gains
- Depth 4-5: Balances short-term and long-term strategy
- Depth 6+: Very strategic but slower

## Interactive Mode

To see the game play step-by-step:

```bash
$ python3 sequencium.py 6 4 interactive
```

This pauses after each move, allowing you to press Enter to continue.

## Key Observations

1. **Symmetry**: On symmetric boards with equally skilled AI players, ties are common
2. **Board Control**: Early board control often leads to higher maximum values
3. **Strategic Blocking**: The AI learns to block opponent expansion paths
4. **Edge Effects**: Corner starting positions create interesting asymmetries in smaller boards
