#ifndef RUBIKS_MOVES_HPP
#define RUBIKS_MOVES_HPP

#include <string>
#include <vector>

namespace rubiks {

class MoveSequence {
public:
    MoveSequence();
    explicit MoveSequence(const std::string& notation);
    
    void add_move(int move_id);
    void add_moves(const std::string& notation);
    std::string to_notation() const;
    
    const std::vector<int>& get_moves() const { return moves_; }
    size_t length() const { return moves_.size(); }
    void clear() { moves_.clear(); }
    
    // Optimization
    void simplify();
    MoveSequence reverse() const;
    
private:
    std::vector<int> moves_;
    static std::string move_to_string(int move_id);
    static int string_to_move(const std::string& move_str);
};

// Utility functions
namespace moves {
    std::string sequence_to_string(const std::vector<int>& moves);
    std::vector<int> string_to_sequence(const std::string& notation);
    bool are_opposite_faces(int move1, int move2);
    int get_opposite_move(int move_id);
}

} // namespace rubiks

#endif // RUBIKS_MOVES_HPP
