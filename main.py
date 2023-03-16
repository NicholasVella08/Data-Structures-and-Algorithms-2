import random
import sys
sys.setrecursionlimit(10**6)  # Set the recursion limit to 1 million



# Binary search tree node
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

# AVL tree
class AVLTree:
    class Node:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
            self.height = 1
            self.comparison_count = 0

    def __init__(self):
        self.root = None
        self.left_rotations = 0
        self.right_rotations = 0

    def insert(self, val):
        self.root = self.insert_helper(self.root, val)

    def insert_helper(self, node, val):
        if node is None:
            return self.Node(val)
        if val < node.val:
            node.left = self.insert_helper(node.left, val)
        else:
            node.right = self.insert_helper(node.right, val)

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balance_factor = self.balance_factor(node)

        if balance_factor > 1 and val < node.left.val:
            return self.right_rotate(node)

        if balance_factor < -1 and val > node.right.val:
            return self.left_rotate(node)

        if balance_factor > 1 and val > node.left.val:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        if balance_factor < -1 and val < node.right.val:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def left_rotate(self, node):
        self.left_rotations += 1
        new_root = node.right
        node.right = new_root.left
        new_root.left = node

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        new_root.height = 1 + max(self.height(new_root.left), self.height(new_root.right))

        return new_root

    def right_rotate(self, node):
        self.right_rotations += 1
        new_root = node.left
        node.left = new_root.right
        new_root.right = node

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        new_root.height = 1 + max(self.height(new_root.left), self.height(new_root.right))

        return new_root

    def balance_factor(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def height(self):
        if self is None:
            return 0
        return self.height

    def node_count(self):
        def node_count_helper(node):
            if node is None:
                return 0
            return node_count_helper(node.left) + node_count_helper(node.right) + 1

        return node_count_helper(self.root)

    def comparison_count(self):
        def comparison_count_helper(node):
            if node is None:
                return 0
            return comparison_count_helper(node.left) + comparison_count_helper(node.right) + node.comparison_count

        return comparison_count_helper(self.root)

    def rotation_count(self):
        return self.left_rotations + self.right_rotations


class RedBlackTree:
    class Node:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
            self.color = "RED"  # new nodes are always colored RED

    def __init__(self):
        self.root = None

    def insert(self, val):
        # create new node with given value and insert it in the tree
        self.root = self.insert_helper(self.root, val)
        # color the root node BLACK to satisfy property 2
        self.root.color = "BLACK"

    def insert_helper(self, node, val):
        # base case: node is None, create a new node with given value
        if node is None:
            return RedBlackTree.Node(val)

        # recursively insert node into the appropriate subtree
        if val < node.val:
            node.left = self.insert_helper(node.left, val)
        else:
            node.right = self.insert_helper(node.right, val)

        # fix violations of the red-black tree properties
        if self.is_red(node.right) and not self.is_red(node.left):
            node = self.rotate_left(node)
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotate_right(node)
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)

        return node

    def is_red(self, node):
        # a node is considered RED if it exists and is colored RED
        if node is None:
            return False
        return node.color == "RED"

    def rotate_left(self, node):
        # perform left rotation on node and return the new root of the subtree
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        # update colors of nodes
        new_root.color = node.color
        node.color = "RED"
        return new_root

    def rotate_right(self, node):
        # perform right rotation on node and return the new root of the subtree
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        # update colors of nodes
        new_root.color = node.color
        node.color = "RED"
        return new_root

    def flip_colors(self, node):
        # flip colors of node and its children
        node.color = "RED"
        node.left.color = "BLACK"
        node.right.color = "BLACK"

    def find(self, val):
        # find node with given value in the tree and return it, or None if it doesn't exist
        return self.find_helper(self.root, val)

    def find_helper(self, node, val):
        # base case: node is None or contains the value we're searching for
        if node is None or node.val == val:
            return node

        # recursively search left or right subtree depending on value
        if val < node.val:
            return self.find_helper(node.left, val)
        else:
            return self.find_helper(node.right, val)

    def height(self):
        def height_helper(node):
            if node is None:
                return 0
            return node.height

        return height_helper(self.root)

    def node_count(self):
        def node_count_helper(node):
            if node is None:
                return 0
            return node_count_helper(node.left) + node_count_helper(node.right) + 1

        return node_count_helper(self.root)

    def comparison_count(self):
        def comparison_count_helper(node):
            if node is None:
                return 0
            return comparison_count_helper(node.left) + comparison_count_helper(node.right) + node.comparison_count

        return comparison_count_helper(self.root)

    def rotation_count(self):
        return self.left_rotations + self.right_rotations


class BinarySearchTree:
    class Node:
        def __init__(self, val):
            self.left = None
            self.right = None
            self.val = val

    def __init__(self):
        self.root = None

    def insert(self, val):
        self.root = self.insert_helper(self.root, val)

    def insert_helper(self, node, val):
        if node is None:
            return self.Node(val)
        elif val < node.val:
            node.left = self.insert_helper(node.left, val)
        else:
            node.right = self.insert_helper(node.right, val)
        return node

    def height(self):
        def height_helper(node):
            if node is None:
                return 0
            return max(height_helper(node.left), height_helper(node.right)) + 1

        return height_helper(self.root)

    def node_count(self):
        def node_count_helper(node):
            if node is None:
                return 0
            return node_count_helper(node.left) + node_count_helper(node.right) + 1

        return node_count_helper(self.root)

    def comparison_count(self):
        def comparison_count_helper(node):
            if node is None:
                return 0
            return comparison_count_helper(node.left) + comparison_count_helper(node.right) + 1

        return comparison_count_helper(self.root)

def in_order_traversal(node):
    if node is None:
        return
    in_order_traversal(node.left)
    print(node.val)
    in_order_traversal(node.right)


# Generating the random numbers and store them in the sets X, Y and Z
p = random.randint(1000, 3000)
X = set(random.sample(range(-3000, 3001), p))

q = random.randint(500, 1000)
Y = set(random.sample(range(-3000, 3001), q))

r = random.randint(500, 1000)
Z = set(random.sample(range(-3000, 3001), r))

# Outputting the size of the random sets.
print(f"Set X contains {len(X)} integers.")
print(f"Set Y contains {len(Y)} integers.")
print(f"Set Z contains {len(Z)} integers.")

print(X)
print(Y)
print(Z)

# Finding the common integers and outputting the number of intersections
XY_intersection = X.intersection(Y)
XZ_intersection = X.intersection(Z)

print(f"Sets X and Y have {len(XY_intersection)} values in common.")
print(f"Sets X and Z have {len(XZ_intersection)} values in common.")

avl_tree = AVLTree()
rb_tree = RedBlackTree()
bst = BinarySearchTree()

# Inputting set X in the three trees
for val in X:
    avl_tree.insert(val)
    rb_tree.insert(val)
    bst.insert(val)

# Output search trees
#print("AVL Tree:")
#in_order_traversal(avl_tree.root)

#print("RB Tree:")
#in_order_traversal(rb_tree.root)

#print("Binary Search Tree:")
#in_order_traversal(bst.root)


print(f"AVL: {avl_tree.rotation_count()} tot. rotations req., height is {avl_tree.height()}, "
      f"#nodes is {avl_tree.node_count()}, #comparisons is {avl_tree.comparison_count()}.")
print(f"RBT: {rb_tree.rotation_count()} tot. rotations req., height is {rb_tree.height()}, "
      f"#nodes is {rb_tree.node_count()}, #comparisons is {rb_tree.comparison_count()}.")
print(f"BST: height is {bst.height()}, #nodes is {bst.node_count()}, "
      f"#comparisons is {bst.comparison_count()}.")