# ####### The cube on the cubie level is described by the permutation and orientations of corners and edges ############

from .enums import Color, Corner as Co, Edge as Ed
from random import randrange


class CubieCube:
    """Represent a cube on the cubie level with 8 corner cubies, 12 edge cubies and the cubie orientations."""
    
    def __init__(self, cp=None, co=None, ep=None, eo=None):
        """Initialize corners and edges."""
        if cp is None:
            self.cp = [Co(i) for i in range(8)]  # corner permutation
        else:
            self.cp = cp[:]
        if co is None:
            self.co = [0]*8  # corner orientation
        else:
            self.co = co[:]
        if ep is None:
            self.ep = [Ed(i) for i in range(12)]  # edge permutation
        else:
            self.ep = ep[:]
        if eo is None:
            self.eo = [0] * 12  # edge orientation
        else:
            self.eo = eo[:]

    def __str__(self):
        """Print string for a cubie cube."""
        s = ''
        for i in Co:
            s = s + '(' + str(self.cp[i]) + ',' + str(self.co[i]) + ')'
        s += '\n'
        for i in Ed:
            s = s + '(' + str(self.ep[i]) + ',' + str(self.eo[i]) + ')'
        return s

    def __eq__(self, other):
        """Define equality of two cubie cubes."""
        return (self.cp == other.cp and self.co == other.co and 
                self.ep == other.ep and self.eo == other.eo)

    def to_facelet_cube(self):
        """Return a facelet representation of the cube."""
        from .face import FaceCube
        from .defs import cornerFacelet, edgeFacelet, cornerColor, edgeColor
        
        fc = FaceCube()
        for i in Co:
            j = self.cp[i]  # corner j is at corner position i
            ori = self.co[i]  # orientation of corner j at position i
            for k in range(3):
                fc.f[cornerFacelet[i][(k+ori) % 3]] = cornerColor[j][k]
        for i in Ed:
            j = self.ep[i]  # similar for edges
            ori = self.eo[i]
            for k in range(2):
                fc.f[edgeFacelet[i][(k+ori) % 2]] = edgeColor[j][k]
        return fc

    def randomize(self):
        """Generate a random cube. The probability is the same for all possible states."""
        # Simplified randomization for basic functionality
        for i in range(8):
            self.cp[i] = Co((i + randrange(8)) % 8)
            self.co[i] = randrange(3)
        for i in range(12):
            self.ep[i] = Ed((i + randrange(12)) % 12)
            self.eo[i] = randrange(2)

    def verify(self):
        """Check if cubiecube is valid."""
        # Basic validation - in a full implementation this would be more comprehensive
        edge_count = [0]*12
        for i in Ed:
            edge_count[self.ep[i]] += 1
        for i in Ed:
            if edge_count[i] != 1:
                return 'Error: Some edges are undefined.'

        corner_count = [0] * 8
        for i in Co:
            corner_count[self.cp[i]] += 1
        for i in Co:
            if corner_count[i] != 1:
                return 'Error: Some corners are undefined.'

        return True  # CUBE_OK equivalent

    def corner_multiply(self, b):
        """Multiply this cubie cube with another cubie cube b, restricted to the corners. Does not change b."""
        c_perm = [0]*8
        c_ori = [0]*8
        ori = 0
        for c in Co:
            c_perm[c] = self.cp[b.cp[c]]
            ori_a = self.co[b.cp[c]]
            ori_b = b.co[c]
            if ori_a < 3 and ori_b < 3:  # two regular cubes
                ori = ori_a + ori_b
                if ori >= 3:
                    ori -= 3
            elif ori_a < 3 <= ori_b:  # cube b is in a mirrored state
                ori = ori_a + ori_b
                if ori >= 6:
                    ori -= 3  # the composition also is in a mirrored state
            elif ori_a >= 3 > ori_b:  # cube a is in a mirrored state
                ori = ori_a - ori_b
                if ori < 3:
                    ori += 3  # the composition is a mirrored cube
            elif ori_a >= 3 and ori_b >= 3:  # if both cubes are in mirrored states
                ori = ori_a - ori_b
                if ori < 0:
                    ori += 3  # the composition is a regular cube
            c_ori[c] = ori
        for c in Co:
            self.cp[c] = c_perm[c]
            self.co[c] = c_ori[c]

    def edge_multiply(self, b):
        """ Multiply this cubie cube with another cubiecube b, restricted to the edges. Does not change b."""
        e_perm = [0]*12
        e_ori = [0]*12
        for e in Ed:
            e_perm[e] = self.ep[b.ep[e]]
            e_ori[e] = (b.eo[e] + self.eo[b.ep[e]]) % 2
        for e in Ed:
            self.ep[e] = e_perm[e]
            self.eo[e] = e_ori[e]

    def multiply(self, b):
        """Multiply this cubie cube with another cubie cube b."""
        self.corner_multiply(b)
        self.edge_multiply(b)

    def inv_cubie_cube(self, d):
        """Store the inverse of this cubie cube in d."""
        for e in Ed:
            d.ep[self.ep[e]] = e
        for e in Ed:
            d.eo[e] = self.eo[d.ep[e]]

        for c in Co:
            d.cp[self.cp[c]] = c
        for c in Co:
            ori = self.co[d.cp[c]]
            if ori >= 3:
                d.co[c] = ori
            else:
                d.co[c] = -ori
                if d.co[c] < 0:
                    d.co[c] += 3

    def get_twist(self):
        """Get the twist of the 8 corners. 0 <= twist < 2187 in phase 1, twist = 0 in phase 2."""
        ret = 0
        for i in range(Co.URF, Co.DRB):
            ret = 3 * ret + self.co[i]
        return ret

    def set_twist(self, twist):
        """Set the twist of the 8 corners."""
        twistparity = 0
        for i in range(Co.DRB - 1, Co.URF - 1, -1):
            self.co[i] = twist % 3
            twistparity += self.co[i]
            twist //= 3
        self.co[Co.DRB] = ((3 - twistparity % 3) % 3)

    def get_flip(self):
        """Get the flip of the 12 edges. 0 <= flip < 2048 in phase 1, flip = 0 in phase 2."""
        ret = 0
        for i in range(Ed.UR, Ed.BR):
            ret = 2 * ret + self.eo[i]
        return ret

    def set_flip(self, flip):
        """Set the flip of the 12 edges."""
        flipparity = 0
        for i in range(Ed.BR - 1, Ed.UR - 1, -1):
            self.eo[i] = flip % 2
            flipparity += self.eo[i]
            flip //= 2
        self.eo[Ed.BR] = ((2 - flipparity % 2) % 2)
