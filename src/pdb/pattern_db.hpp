#ifndef PATTERN_DB_HPP
#define PATTERN_DB_HPP

#include <vector>
#include <string>
#include <cstdint>
#include "../core/cube.hpp"

namespace rubiks {

class PatternDB {
public:
    PatternDB(const std::string& filename);
    ~PatternDB();
    
    // Load database from file
    bool load_from_file(const std::string& filename);
    
    // Query heuristic value using cube state
    uint8_t lookup(const Cube::State& state) const;
    
    // Statistics
    size_t size() const { return entries_.size(); }
    
private:
    std::vector<uint8_t> entries_;
};

// Builder class for generating PDBs based on Hkociemba algorithm
class PatternDBBuilder {
public:
    // Build corner orientation pattern database (3^7 = 2187 states)
    static void build_corner_orientation_pdb(const std::string& output_file);
    
    // Future PDB types can be added here:
    // static void build_edge_orientation_pdb(const std::string& output_file);
    // static void build_corner_permutation_pdb(const std::string& output_file);
};

} // namespace rubiks

#endif // PATTERN_DB_HPP
