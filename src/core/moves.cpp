#include "moves.hpp"
#include "cube.hpp"
#include <sstream>
#include <unordered_map>

namespace rubiks {

MoveSequence::MoveSequence() = default;

MoveSequence::MoveSequence(const std::string& notation) {
    add_moves(notation);
}

void MoveSequence::add_move(int move_id) {
    if (move_id >= 0 && move_id < NUM_MOVES) {
        moves_.push_back(move_id);
    }
}

void MoveSequence::add_moves(const std::string& notation) {
    std::istringstream iss(notation);
    std::string move;
    
    while (iss >> move) {
        int move_id = string_to_move(move);
        if (move_id >= 0) {
            add_move(move_id);
        }
    }
}

std::string MoveSequence::to_notation() const {
    std::string result;
    for (size_t i = 0; i < moves_.size(); ++i) {
        if (i > 0) result += " ";
        result += move_to_string(moves_[i]);
    }
    return result;
}

void MoveSequence::simplify() {
    // Remove consecutive moves on same face that cancel out
    std::vector<int> simplified;
    
    for (int move : moves_) {
        if (!simplified.empty() && moves::are_opposite_faces(simplified.back(), move)) {
            // Check if moves cancel out
            int last = simplified.back();
            if (moves::get_opposite_move(last) == move) {
                simplified.pop_back(); // Cancel out
                continue;
            }
        }
        simplified.push_back(move);
    }
    
    moves_ = simplified;
}

MoveSequence MoveSequence::reverse() const {
    MoveSequence reversed;
    for (auto it = moves_.rbegin(); it != moves_.rend(); ++it) {
        reversed.add_move(moves::get_opposite_move(*it));
    }
    return reversed;
}

std::string MoveSequence::move_to_string(int move_id) {
    static const std::string move_names[] = {
        "R", "R'", "R2",
        "L", "L'", "L2", 
        "U", "U'", "U2",
        "D", "D'", "D2",
        "F", "F'", "F2",
        "B", "B'", "B2"
    };
    
    if (move_id >= 0 && move_id < NUM_MOVES) {
        return move_names[move_id];
    }
    return "";
}

int MoveSequence::string_to_move(const std::string& move_str) {
    static const std::unordered_map<std::string, int> move_map = {
        {"R", R}, {"R'", R_PRIME}, {"R2", R2},
        {"L", L}, {"L'", L_PRIME}, {"L2", L2},
        {"U", U}, {"U'", U_PRIME}, {"U2", U2},
        {"D", D}, {"D'", D_PRIME}, {"D2", D2},
        {"F", F}, {"F'", F_PRIME}, {"F2", F2},
        {"B", B}, {"B'", B_PRIME}, {"B2", B2}
    };
    
    auto it = move_map.find(move_str);
    return (it != move_map.end()) ? it->second : -1;
}

namespace moves {

std::string sequence_to_string(const std::vector<int>& moves) {
    MoveSequence seq;
    for (int move : moves) {
        seq.add_move(move);
    }
    return seq.to_notation();
}

std::vector<int> string_to_sequence(const std::string& notation) {
    MoveSequence seq(notation);
    return seq.get_moves();
}

bool are_opposite_faces(int move1, int move2) {
    int face1 = move1 / 3;  // R=0, L=1, U=2, D=3, F=4, B=5
    int face2 = move2 / 3;
    
    return (face1 == 0 && face2 == 1) ||  // R-L
           (face1 == 1 && face2 == 0) ||  // L-R
           (face1 == 2 && face2 == 3) ||  // U-D
           (face1 == 3 && face2 == 2) ||  // D-U
           (face1 == 4 && face2 == 5) ||  // F-B
           (face1 == 5 && face2 == 4);    // B-F
}

int get_opposite_move(int move_id) {
    // Return the inverse of a move
    switch (move_id) {
        case R: return R_PRIME;
        case R_PRIME: return R;
        case R2: return R2;
        case L: return L_PRIME;
        case L_PRIME: return L;
        case L2: return L2;
        case U: return U_PRIME;
        case U_PRIME: return U;
        case U2: return U2;
        case D: return D_PRIME;
        case D_PRIME: return D;
        case D2: return D2;
        case F: return F_PRIME;
        case F_PRIME: return F;
        case F2: return F2;
        case B: return B_PRIME;
        case B_PRIME: return B;
        case B2: return B2;
        default: return move_id;
    }
}

} // namespace moves

} // namespace rubiks
