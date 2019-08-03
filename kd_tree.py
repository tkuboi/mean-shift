"""K-D Tree
Author:
    Toshi
"""

class Node:
    """Node for KD tree
    Attributes:
        point (int, int) : a tuple of int
        left (Node) : left subtree
        right (Node) : right subtree
    """
    def __init__(self, point, left=None, right=None):
        self.point = point 
        self.left = left
        self.right = right

    def __repr__(self):
        return "{point(%s, %s), left: %s, right: %s}"\
            % (self.point[0], self.point[1], self.left, self.right)


class KDTree:
    """KD tree wrapper
    Attributes:
        dim (int) : the dimension 
        root (Node) : the root node of the tree 
    """
    def __init__(self, dim):
        self.dim = dim
        self.root = None

    def insert(self, point):
        self.root = self._insert(self.root, point, 0)

    def _insert(self, tree, point, dep):
        if tree is None:
            return Node(point)
        dim = dep % self.dim
        if point[dim] < tree.point[dim]:
            tree.left = self._insert(tree.left, point, dep + 1)
        else:
            tree.right = self._insert(tree.right, point, dep + 1)
        return tree

    def nearest(self, point):
        return self._nearest(self.root, point, 0, 99999, None)

    def _nearest(self, tree, point, dep, dist, nearest):
        if tree is None:
            return 99999, None
        dim = dep % self.dim
        d = self.distance(tree.point, point)
        if d < dist:
            dist = d
            nearest = tree.point
            d, p = self._nearest(tree.left, point, dep + 1, dist, nearest)
            if d < dist:
                dist = d
                nearest = p
            d, p = self._nearest(tree.right, point, dep + 1, dist, nearest)
            if d < dist:
                dist = d
                nearest = p
        return dist, nearest

    def distance(self, p1, p2):
        dist = 0
        for d in range(self.dim):
            dist += (p1[d] - p2[d]) ** 2
        return dist

    def get_neighbors(self, point, dist):
        neighbors = []
        self._get_neighbors(self.root, point, dist, neighbors, 0)
        return neighbors

    def _get_neighbors(self, tree, point, dist, accum, depth):
        if tree is None:
            return

        dim = depth % self.dim
        d = self.distance(point, tree.point)
        if d <= dist:
            accum.append(tree.point)
            self._get_neighbors(tree.left, point, dist, accum, depth + 1)
            self._get_neighbors(tree.right, point, dist, accum, depth + 1)
        elif point[dim] == tree.point[dim]:
            self._get_neighbors(tree.left, point, dist, accum, depth + 1)
            self._get_neighbors(tree.right, point, dist, accum, depth + 1)
        elif point[dim] < tree.point[dim]:
            self._get_neighbors(tree.left, point, dist, accum, depth + 1)
        else:
            self._get_neighbors(tree.right, point, dist, accum, depth + 1)

    def range_search(self, bot_left, top_right):
        return self._range_search(self.root, bot_left, top_right, 0)

    def _range_search(self, tree, bot_left, top_right, dep):
        accum = []
        if tree is None:
            return accum
        dim = dep % self.dim
        if bot_left[dim] <= tree.point[dim] <= top_right[dim]:
            dim2 = (dim + 1) % self.dim
            if bot_left[dim2] <= tree.point[dim2] <= top_right[dim2]:
                accum.append(tree.point)
            return self._range_search(tree.left, bot_left, top_right, dep + 1)\
                + accum\
                + self._range_search(tree.right, bot_left, top_right, dep + 1)
        if top_right[dim] < tree.point[dim]:
            return self._range_search(tree.left, bot_left, top_right, dep + 1)
        return self._range_search(tree.right, bot_left, top_right, dep + 1)


def main():
    kd = KDTree(2)
    kd.insert((1, 1))
    kd.insert((2, 2))
    kd.insert((0, -1))
    kd.insert((2, -1))
    print(kd.root)
    print(kd.nearest((0, 0)))
    print(kd.range_search((0, 0), (2,2)))

if __name__ == '__main__':
    main()

