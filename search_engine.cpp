/*
 * Sequencium Search Engine - C++ Implementation
 * Optimized search algorithm with Stockfish-inspired techniques
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <array>
#include <algorithm>
#include <limits>
#include <unordered_map>
#include <cstring>

namespace py = pybind11;

// Constants
constexpr int MAX_BOARD_SIZE = 10;
constexpr int PLAYER_A = 1;
constexpr int PLAYER_B = 2;
constexpr int EMPTY = 0;

// Move structure
struct Move {
    int row;
    int col;
    int value;
    int score;  // For move ordering
    
    Move() : row(0), col(0), value(0), score(0) {}
    Move(int r, int c, int v) : row(r), col(c), value(v), score(0) {}
    Move(int r, int c, int v, int s) : row(r), col(c), value(v), score(s) {}
};

// Board state representation
struct BoardState {
    int size;
    int board[MAX_BOARD_SIZE][MAX_BOARD_SIZE];
    int player_max_values[3];  // index 0 unused, 1 for A, 2 for B
    
    BoardState() : size(0) {
        std::memset(board, 0, sizeof(board));
        std::memset(player_max_values, 0, sizeof(player_max_values));
    }
    
    BoardState(int sz) : size(sz) {
        std::memset(board, 0, sizeof(board));
        std::memset(player_max_values, 0, sizeof(player_max_values));
    }
    
    // Hash for transposition table
    uint64_t hash() const {
        uint64_t h = 0;
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                h = h * 131 + board[i][j];
            }
        }
        return h;
    }
    
    void copy_from(const BoardState& other) {
        size = other.size;
        std::memcpy(board, other.board, sizeof(board));
        std::memcpy(player_max_values, other.player_max_values, sizeof(player_max_values));
    }
};

// Transposition table entry
struct TTEntry {
    uint64_t hash;
    int depth;
    int score;
    int flag;  // 0: exact, 1: lower bound, 2: upper bound
    Move best_move;
    
    TTEntry() : hash(0), depth(0), score(0), flag(0) {}
};

// Transposition table
class TranspositionTable {
private:
    size_t table_size;
    std::vector<TTEntry> table;
    
public:
    TranspositionTable(size_t size = 1048576) : table_size(size), table(size) {}
    
    void resize(size_t new_size) {
        table_size = new_size;
        table.clear();
        table.resize(new_size);
    }
    
    void store(uint64_t hash, int depth, int score, int flag, const Move& move) {
        size_t index = hash % table_size;
        TTEntry& entry = table[index];
        
        // Replace if deeper or empty
        if (entry.hash == 0 || depth >= entry.depth) {
            entry.hash = hash;
            entry.depth = depth;
            entry.score = score;
            entry.flag = flag;
            entry.best_move = move;
        }
    }
    
    bool probe(uint64_t hash, int depth, int& score, Move& move) {
        size_t index = hash % table_size;
        const TTEntry& entry = table[index];
        
        if (entry.hash == hash && entry.depth >= depth) {
            score = entry.score;
            move = entry.best_move;
            return true;
        }
        return false;
    }
    
    void clear() {
        table.clear();
        table.resize(table_size);
    }
};

// Search engine class
class SearchEngine {
private:
    TranspositionTable tt;
    int nodes_evaluated;
    
    // Get cell value: returns player*100 + value, or 0 for empty
    int get_cell(const BoardState& board, int row, int col) const {
        if (row < 0 || row >= board.size || col < 0 || col >= board.size) {
            return -1;
        }
        return board.board[row][col];
    }
    
    // Extract player from cell value
    int get_player(int cell_value) const {
        if (cell_value == 0) return 0;
        return cell_value / 100;
    }
    
    // Extract value from cell value
    int get_value(int cell_value) const {
        if (cell_value == 0) return 0;
        return cell_value % 100;
    }
    
    // Generate valid moves for a player
    std::vector<Move> generate_moves(const BoardState& board, int player) const {
        std::vector<Move> moves;
        bool visited[MAX_BOARD_SIZE][MAX_BOARD_SIZE] = {};
        
        // Find all cells owned by player and their neighbors
        for (int i = 0; i < board.size; ++i) {
            for (int j = 0; j < board.size; ++j) {
                int cell = board.board[i][j];
                if (cell > 0 && get_player(cell) == player) {
                    int current_value = get_value(cell);
                    int new_value = current_value + 1;
                    
                    // Check all 8 neighbors
                    for (int dr = -1; dr <= 1; ++dr) {
                        for (int dc = -1; dc <= 1; ++dc) {
                            if (dr == 0 && dc == 0) continue;
                            
                            int nr = i + dr;
                            int nc = j + dc;
                            
                            if (nr >= 0 && nr < board.size && 
                                nc >= 0 && nc < board.size && 
                                board.board[nr][nc] == 0 && !visited[nr][nc]) {
                                
                                visited[nr][nc] = true;
                                moves.emplace_back(nr, nc, new_value);
                            }
                        }
                    }
                }
            }
        }
        
        // Keep only moves with maximum value for each position
        std::sort(moves.begin(), moves.end(), 
                 [](const Move& a, const Move& b) {
                     if (a.row != b.row) return a.row < b.row;
                     if (a.col != b.col) return a.col < b.col;
                     return a.value > b.value;
                 });
        
        std::vector<Move> result;
        for (size_t i = 0; i < moves.size(); ++i) {
            if (i == 0 || moves[i].row != moves[i-1].row || moves[i].col != moves[i-1].col) {
                result.push_back(moves[i]);
            }
        }
        
        return result;
    }
    
    // Make a move on the board
    void make_move(BoardState& board, const Move& move, int player) const {
        int cell_value = player * 100 + move.value;
        board.board[move.row][move.col] = cell_value;
        
        // Update max value
        if (move.value > board.player_max_values[player]) {
            board.player_max_values[player] = move.value;
        }
    }
    
    // Unmake a move
    void unmake_move(BoardState& board, const Move& move, int player) const {
        board.board[move.row][move.col] = 0;
        
        // Recompute max value for player (slower but correct)
        board.player_max_values[player] = 0;
        for (int i = 0; i < board.size; ++i) {
            for (int j = 0; j < board.size; ++j) {
                int cell = board.board[i][j];
                if (cell > 0 && get_player(cell) == player) {
                    int val = get_value(cell);
                    if (val > board.player_max_values[player]) {
                        board.player_max_values[player] = val;
                    }
                }
            }
        }
    }
    
    // Fast mobility count (count potential moves without generating full move list)
    int count_mobility(const BoardState& board, int player) const {
        bool visited[MAX_BOARD_SIZE][MAX_BOARD_SIZE] = {};
        int count = 0;
        
        for (int i = 0; i < board.size; ++i) {
            for (int j = 0; j < board.size; ++j) {
                int cell = board.board[i][j];
                if (cell > 0 && get_player(cell) == player) {
                    // Check all 8 neighbors
                    for (int dr = -1; dr <= 1; ++dr) {
                        for (int dc = -1; dc <= 1; ++dc) {
                            if (dr == 0 && dc == 0) continue;
                            
                            int nr = i + dr;
                            int nc = j + dc;
                            
                            if (nr >= 0 && nr < board.size && 
                                nc >= 0 && nc < board.size && 
                                board.board[nr][nc] == 0 && !visited[nr][nc]) {
                                
                                visited[nr][nc] = true;
                                count++;
                            }
                        }
                    }
                }
            }
        }
        return count;
    }
    
    // Evaluate position
    int evaluate(const BoardState& board, int player) const {
        int opponent = (player == PLAYER_A) ? PLAYER_B : PLAYER_A;
        
        // Primary: max value difference
        int max_diff = board.player_max_values[player] - board.player_max_values[opponent];
        
        // Secondary: count cells
        int player_cells = 0, opponent_cells = 0;
        for (int i = 0; i < board.size; ++i) {
            for (int j = 0; j < board.size; ++j) {
                int cell = board.board[i][j];
                if (cell > 0) {
                    if (get_player(cell) == player) {
                        player_cells++;
                    } else if (get_player(cell) == opponent) {
                        opponent_cells++;
                    }
                }
            }
        }
        int cell_diff = player_cells - opponent_cells;
        
        // Tertiary: mobility (use fast count)
        int mobility_diff = count_mobility(board, player) - count_mobility(board, opponent);
        
        return max_diff * 100 + cell_diff * 10 + mobility_diff;
    }
    
    // Move ordering for better pruning (Stockfish-inspired)
    void order_moves(std::vector<Move>& moves, const BoardState& board, int player) const {
        for (auto& move : moves) {
            // Higher value moves first
            move.score = move.value * 1000;
            
            // Center control bonus
            int center = board.size / 2;
            int dist = std::abs(move.row - center) + std::abs(move.col - center);
            move.score += (board.size - dist) * 10;
        }
        
        std::sort(moves.begin(), moves.end(), 
                 [](const Move& a, const Move& b) { return a.score > b.score; });
    }
    
    // Minimax with alpha-beta pruning
    int minimax(BoardState& board, int depth, int alpha, int beta, 
                bool maximizing, int player, Move& best_move) {
        nodes_evaluated++;
        
        // Check transposition table
        uint64_t hash = board.hash();
        Move tt_move;
        int tt_score;
        if (tt.probe(hash, depth, tt_score, tt_move)) {
            best_move = tt_move;
            return tt_score;
        }
        
        int opponent = (player == PLAYER_A) ? PLAYER_B : PLAYER_A;
        int current_player = maximizing ? player : opponent;
        
        // Terminal condition
        if (depth == 0) {
            int score = evaluate(board, player);
            tt.store(hash, depth, score, 0, best_move);
            return score;
        }
        
        auto moves = generate_moves(board, current_player);
        
        // Check if game is over
        if (moves.empty()) {
            auto opponent_moves = generate_moves(board, opponent);
            if (opponent_moves.empty()) {
                int score = evaluate(board, player);
                tt.store(hash, depth, score, 0, best_move);
                return score;
            }
            // Current player has no moves, switch
            return minimax(board, depth - 1, alpha, beta, !maximizing, player, best_move);
        }
        
        // Move ordering
        order_moves(moves, board, current_player);
        
        if (maximizing) {
            int max_eval = std::numeric_limits<int>::min();
            Move local_best;
            
            for (const auto& move : moves) {
                make_move(board, move, current_player);
                Move dummy;
                int eval = minimax(board, depth - 1, alpha, beta, false, player, dummy);
                unmake_move(board, move, current_player);
                
                if (eval > max_eval) {
                    max_eval = eval;
                    local_best = move;
                }
                
                alpha = std::max(alpha, eval);
                if (beta <= alpha) {
                    break;  // Beta cutoff
                }
            }
            
            best_move = local_best;
            tt.store(hash, depth, max_eval, alpha >= beta ? 1 : 0, best_move);
            return max_eval;
        } else {
            int min_eval = std::numeric_limits<int>::max();
            Move local_best;
            
            for (const auto& move : moves) {
                make_move(board, move, current_player);
                Move dummy;
                int eval = minimax(board, depth - 1, alpha, beta, true, player, dummy);
                unmake_move(board, move, current_player);
                
                if (eval < min_eval) {
                    min_eval = eval;
                    local_best = move;
                }
                
                beta = std::min(beta, eval);
                if (beta <= alpha) {
                    break;  // Alpha cutoff
                }
            }
            
            best_move = local_best;
            tt.store(hash, depth, min_eval, alpha >= beta ? 2 : 0, best_move);
            return min_eval;
        }
    }
    
public:
    SearchEngine() : nodes_evaluated(0) {}
    
    // Python interface: find best move
    py::tuple find_best_move(py::list board_2d, int board_size, int player, int depth) {
        nodes_evaluated = 0;
        
        // Convert Python board to internal representation
        BoardState board(board_size);
        board.size = board_size;
        
        for (int i = 0; i < board_size; ++i) {
            py::list row = board_2d[i];
            for (int j = 0; j < board_size; ++j) {
                py::object cell = row[j];
                
                if (cell.is_none()) {
                    board.board[i][j] = 0;
                } else {
                    py::tuple cell_tuple = cell.cast<py::tuple>();
                    int player_id = cell_tuple[0].cast<int>();
                    int value = cell_tuple[1].cast<int>();
                    board.board[i][j] = player_id * 100 + value;
                    
                    // Track max values
                    if (value > board.player_max_values[player_id]) {
                        board.player_max_values[player_id] = value;
                    }
                }
            }
        }
        
        // Run search
        Move best_move;
        minimax(board, depth, 
                std::numeric_limits<int>::min(), 
                std::numeric_limits<int>::max(), 
                true, player, best_move);
        
        // Return (row, col, value, nodes_evaluated)
        return py::make_tuple(best_move.row, best_move.col, best_move.value, nodes_evaluated);
    }
    
    void clear_tt() {
        tt.clear();
    }
    
    int get_nodes_evaluated() const {
        return nodes_evaluated;
    }
};

// Python bindings
PYBIND11_MODULE(search_engine, m) {
    m.doc() = "Fast C++ search engine for Sequencium game";
    
    py::class_<SearchEngine>(m, "SearchEngine")
        .def(py::init<>())
        .def("find_best_move", &SearchEngine::find_best_move,
             "Find the best move using minimax with alpha-beta pruning",
             py::arg("board"), py::arg("board_size"), py::arg("player"), py::arg("depth"))
        .def("clear_tt", &SearchEngine::clear_tt,
             "Clear the transposition table")
        .def("get_nodes_evaluated", &SearchEngine::get_nodes_evaluated,
             "Get the number of nodes evaluated in last search");
}
