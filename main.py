import random
import sys
sys.setrecursionlimit(10**6)  # Set the recursion limit to 1 million

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

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
        self.root = self.insertHelper(self.root, val)

    def insertHelper(self, node, val):
        if node is None:
            return self.Node(val)
        if val < node.val:
            node.left = self.insertHelper(node.left, val)
            node.comparison_count += 1  # increment comparison count
        else:
            node.right = self.insertHelper(node.right, val)
            node.comparison_count += 1  # increment comparison count

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balanceFactor = self.balanceFactor(node)

        if balanceFactor > 1 and val < node.left.val:
            return self.rightRotate(node)

        if balanceFactor < -1 and val > node.right.val:
            return self.leftRotate(node)

        if balanceFactor > 1 and val > node.left.val:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)

        if balanceFactor < -1 and val < node.right.val:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)

        return node


    def delete(self, val):
        self.root = self.deleteHelper(self.root, val)

    def deleteHelper(self, node, val):
        if node is None:
            return None

        if val < node.val:
            node.left = self.deleteHelper(node.left, val)
        elif val > node.val:
            node.right = self.deleteHelper(node.right, val)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            min_right = self.find_min(node.right)
            node.val = min_right.val
            node.right = self.deleteHelper(node.right, min_right.val)

        if node is None:
            return None

        node.height = 1 + max(self.height(node.left), self.height(node.right))

        balanceFactor = self.balanceFactor(node)

        if balanceFactor > 1 and self.balanceFactor(node.left) >= 0:
            return self.rightRotate(node)

        if balanceFactor < -1 and self.balanceFactor(node.right) <= 0:
            return self.leftRotate(node)

        if balanceFactor > 1 and self.balanceFactor(node.left) < 0:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)

        if balanceFactor < -1 and self.balanceFactor(node.right) > 0:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)

        return node

    def find_min(self, node):
        while node.left is not None:
            node = node.left
        return node


    def leftRotate(self, node):
        self.left_rotations += 1
        new_root = node.right
        node.right = new_root.left
        new_root.left = node

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        new_root.height = 1 + max(self.height(new_root.left), self.height(new_root.right))

        return new_root

    def rightRotate(self, node):
        self.right_rotations += 1
        new_root = node.left
        node.left = new_root.right
        new_root.right = node

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        new_root.height = 1 + max(self.height(new_root.left), self.height(new_root.right))

        return new_root

    def balanceFactor(self, node):
        if node is None:
            return 0
        return self.height(node.left) - self.height(node.right)

    def height(self, node):
        if node is None:
            return -1
        return node.height

    def nodeCount(self):
        def nodeCountHelper(node):
            if node is None:
                return 0
            return nodeCountHelper(node.left) + nodeCountHelper(node.right) + 1

        return nodeCountHelper(self.root)

    def get_comparison_count(self):
        def comparisonCountHelper(node):
            if node is None:
                return 0
            left_count = comparisonCountHelper(node.left)
            right_count = comparisonCountHelper(node.right)
            total_count = left_count + right_count + node.comparison_count
            return total_count

        return comparisonCountHelper(self.root)

    def rotationCount(self):
        return self.left_rotations + self.right_rotations


class RedBlackTree:
    class Node:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
            self.height = 1
            self.color = "RED"  # new nodes are always colored RED
            self.comparison_count = 0  # initialize comparison count to 0

    def __init__(self):
        self.root = None
        self.left_rotations = 0  # initialize left rotation count to 0
        self.right_rotations = 0  # initialize right rotation count to 0

    def insert(self, val):
        # create new node with given value and insert it in the tree
        self.root = self.insertHelper(self.root, val)
        # color the root node BLACK to satisfy property 2
        self.root.color = "BLACK"

    def insertHelper(self, node, val):

        if node is None:
            return RedBlackTree.Node(val)

        # recursively insert node into the appropriate subtree
        if val < node.val:
            node.left = self.insertHelper(node.left, val)
        else:
            node.right = self.insertHelper(node.right, val)

        # fix violations of the red-black tree properties
        if self.is_red(node.right) and not self.is_red(node.left):
            node = self.rotateLeft(node)
            self.left_rotations += 1
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotateRight(node)
            self.right_rotations += 1
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)

        # increment comparison count
        node.comparison_count += 1

        return node

    def is_red(self, node):
        # a node is considered RED if it exists and is colored RED
        if node is None:
            return False
        return node.color == "RED"

    def rotateLeft(self, node):
        # perform left rotation on node and return the new root of the subtree
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        # update colors of nodes
        new_root.color = node.color
        node.color = "RED"
        return new_root

    def rotateRight(self, node):
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
        return self.findHelper(self.root, val)

    def findHelper(self, node, val):

        if node is None or node.val == val:
            return node

        # recursively search left or right subtree depending on value
        if val < node.val:
            return self.findHelper(node.left, val)
        else:
            return self.findHelper(node.right, val)

    def delete(self, val):
        # delete node with given value from the tree, if it exists
        self.root = self.deleteHelper(self.root, val)
        # color the root node BLACK to satisfy property 2
        self.root.color = "BLACK"

    def deleteHelper(self, node, val):

        if node is None:
            return None

        # recursively search for node with given value in the tree
        if val < node.val:
            node.left = self.deleteHelper(node.left, val)
        elif val > node.val:
            node.right = self.deleteHelper(node.right, val)
        else:

            if node.left is None and node.right is None:
                return None


            if node.left is None:
                return node.right
            if node.right is None:
                return node.left


            successor = self.get_successor(node.right)
            node.val = successor.val
            node.right = self.deleteHelper(node.right, successor.val)

        # fix violations of the red-black tree properties
        if self.is_red(node.right) and not self.is_red(node.left):
            node = self.rotateLeft(node)
            self.left_rotations += 1
        if self.is_red(node.left) and self.is_red(node.left.left):
            node = self.rotateRight(node)
            self.right_rotations += 1
        if self.is_red(node.left) and self.is_red(node.right):
            self.flip_colors(node)

        # increment comparison count
        node.comparison_count += 1

        return node

    def get_successor(self, node):
        # find the node with the smallest value in the right subtree of node
        while node.left is not None:
            node = node.left
        return node

    def height(self):
        def height_helper(node):
            if node is None:
                return -1
            else:
                return max(height_helper(node.left), height_helper(node.right)) + 1

        return height_helper(self.root)

    def nodeCount(self):
        def nodeCountHelper(node):
            if node is None:
                return 0
            return nodeCountHelper(node.left) + nodeCountHelper(node.right) + 1

        return nodeCountHelper(self.root)

    def comparison_count(self):
        def comparisonCountHelper(node):
            if node is None:
                return 0
            return comparisonCountHelper(node.left) + comparisonCountHelper(node.right) + node.comparison_count

        return comparisonCountHelper(self.root)

    def rotationCount(self):
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
        self.root = self.insertHelper(self.root, val)

    def insertHelper(self, node, val):
        if node is None:
            return self.Node(val)

        elif val < node.val:
            node.left = self.insertHelper(node.left, val)
        else:
            node.right = self.insertHelper(node.right, val)
        return node

    def delete(self, val):
        self.root = self.deleteHelper(self.root, val)

    def deleteHelper(self, node, val):
        if node is None:
            return None
        elif val < node.val:
            node.left = self.deleteHelper(node.left, val)
        elif val > node.val:
            node.right = self.deleteHelper(node.right, val)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                # Find the minimum value in the right subtree
                min_node = node.right
                while min_node.left is not None:
                    min_node = min_node.left

                # Replace the node's value with the minimum value
                node.val = min_node.val

                # Delete the minimum node in the right subtree
                node.right = self.deleteHelper(node.right, min_node.val)

        return node

    def height(self):
        def height_helper(node):
            if node is None:
                return 0
            return max(height_helper(node.left), height_helper(node.right)) + 1

        return height_helper(self.root)

    def nodeCount(self):
        def nodeCountHelper(node):
            if node is None:
                return 0
            return nodeCountHelper(node.left) + nodeCountHelper(node.right) + 1

        return nodeCountHelper(self.root)

    def comparison_count(self):
        def comparisonCountHelper(node):
            if node is None:
                return 0
            return comparisonCountHelper(node.left) + comparisonCountHelper(node.right) + 1

        return comparisonCountHelper(self.root)


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

print()

print(f"AVL: {avl_tree.rotationCount()} tot. rotations req., height is {avl_tree.height(avl_tree.root)}, #nodes is {avl_tree.nodeCount()}, #comparisons is {avl_tree.get_comparison_count()}.")
print(f"RBT: {rb_tree.rotationCount()} tot. rotations req., height is {rb_tree.height()}, #nodes is {rb_tree.nodeCount()}, #comparisons is {rb_tree.comparison_count()}.")
print(f"BST: height is {bst.height()}, #nodes is {bst.nodeCount()}, #comparisons is {bst.comparison_count()}.")

for val in Y:
    avl_tree.delete(val)
    rb_tree.delete(val)
    bst.delete(val)

# Outputting search trees after deletion
#print("AVL Tree:")
#in_order_traversal(avl_tree.root)

#print("RB Tree:")
#in_order_traversal(rb_tree.root)


#print("BST Tree:")
#in_order_traversal(bst.root)

print()
print(f"AVL: {avl_tree.rotationCount()} tot. rotations req., height is {avl_tree.height(avl_tree.root)}, #nodes is {avl_tree.nodeCount()}, #comparisons is {avl_tree.get_comparison_count()}.")
print(f"RBT: {rb_tree.rotationCount()} tot. rotations req., height is {rb_tree.height()}, #nodes is {rb_tree.nodeCount()}, #comparisons is {rb_tree.comparison_count()}.")
print(f"BST: height is {bst.height()}, #nodes is {bst.nodeCount()}, #comparisons is {bst.comparison_count()}.")

found_count = 0
not_found_count = 0
total_comparisons = 0

for val in Z:
    node = avl_tree.root
    comparisons = 0
    while node is not None:
        comparisons += 1
        if val == node.val:
            found_count += 1
            break
        elif val < node.val:
            node = node.left
        else:
            node = node.right
    if node is None:
        not_found_count += 1
    total_comparisons += comparisons

# Print results
print()
print("AVL:")
print(f"Total comparisons required: {total_comparisons}")
print(f"Numbers found: {found_count}")
print(f"Numbers not found: {not_found_count}")

total_comparisons = 0
found_count = 0
not_found_count = 0

for val in Z:
    node = rb_tree.find(val)
    if node is not None:
        total_comparisons += node.comparison_count
        found_count += 1
    else:
        total_comparisons += rb_tree.root.comparison_count
        not_found_count += 1

print()
print("RBT:")
print(f"Total comparisons required: {total_comparisons}")
print(f"Numbers found: {found_count}")
print(f"Numbers not found: {not_found_count}")

total_comparisons = 0
found_count = 0
not_found_count = 0

for val in Z:
    current = bst.root
    comparisons = 0
    while current is not None:
        comparisons += 1
        if current.val == val:
            found_count += 1
            total_comparisons += comparisons
            break
        elif val < current.val:
            current = current.left
        else:
            current = current.right
    else:
        not_found_count += 1

print()
print("BST:")
print(f"Total comparisons required: {total_comparisons}")
print(f"Numbers found: {found_count}")
print(f"Numbers not found: {not_found_count}")