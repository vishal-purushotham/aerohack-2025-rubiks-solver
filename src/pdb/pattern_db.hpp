#ifndef PATTERN_DB_HPP
#define PATTERN_DB_HPP

#include <vector>
#include <string>
#include <cstdint>

namespace rubiks {

class PatternDB {
public:
    PatternDB(const std::string& filename);
    ~PatternDB();
    
    // Load compressed database
    bool load_from_file(const std::string& filename);
    
    // Query heuristic value
    uint8_t lookup(uint64_t pattern_key) const;
    
    // Statistics
    size_t size() const { return entries_.size(); }
    double compression_ratio() const;
    
private:
    std::vector<uint8_t> entries_;
    void* compressed_data_;
    size_t compressed_size_;
    size_t uncompressed_size_;
    
    uint64_t compute_pattern_key(uint64_t state) const;
};

// Builder class for generating PDBs
class PatternDBBuilder {
public:
    static void build_corner_pdb(const std::string& output_file);
    static void build_edge_pdb(const std::string& output_file);
    
private:
    static void bfs_build(const std::string& output_file, 
                         bool is_corner_db);
};

} // namespace rubiks

#endif // PATTERN_DB_HPP
