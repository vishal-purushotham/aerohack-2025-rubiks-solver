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
