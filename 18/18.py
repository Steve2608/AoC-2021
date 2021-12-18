import itertools as it
from dataclasses import dataclass


@dataclass(slots=True)
class Node:
    parent: 'Node' = None
    left: 'Node' = None
    right: 'Node' = None
    value: int = None
    height: int = None

    def __str__(self):
        sb = ['']
        self._recursive_string('', True, sb)
        return sb[0]

    def _recursive_string(self, prefix: str, is_tail: bool, sb):
        if self.right:
            self.right._recursive_string(prefix + ("│   " if is_tail else "    "), False, sb)
        sb[0] += prefix + ("└── " if is_tail else "┌── ") + (str(self.value) if isinstance(self.value, int) else '') + '\n'
        if self.left:
            self.left._recursive_string(prefix + ("    " if is_tail else "│   "), True, sb)      

    __repr__ = __str__


def in_order_by_node(root: Node):
    if root:
        yield from in_order_by_node(root.left)
        if root.value is not None:
            yield root
        yield from in_order_by_node(root.right)


def in_order(root: Node):
    yield from map(lambda n: n.value, in_order_by_node(root))


def in_order_predecessor(root: Node, target: Node):
    it = in_order_by_node(root)
    prev = next(it)
    for curr in it:
        if curr is target:
            return prev
        prev = curr


def in_order_successor(root: Node, target: Node):
    it = in_order_by_node(root)
    prev = next(it)
    for curr in it:
        if prev is target:
            return curr
        
        prev = curr
    # return nothing if target is last node


def magintude(root: Node) -> int:
    if not root:
        return 0

    if root.value is None:
        left = magintude(root.left)
        right = magintude(root.right)
        return 3 * left + 2 * right
    else:
        return root.value 


def construct_tree(snail_number: list):
    def _construct_tree(root: Node, number: list | int):
        if isinstance(number, list):
            left_value = number[0] if isinstance(number[0], int) else None
            right_value = number[1] if isinstance(number[1], int) else None
            root.left = Node(parent=root, value=left_value)
            root.right = Node(parent=root, value=right_value)

            _construct_tree(root.left, number[0])
            _construct_tree(root.right, number[1])
    
    def set_heights(root: Node) -> int:
        if root:
            left_height = set_heights(root.left)
            right_height = set_heights(root.right)
            
            root.height = max(left_height, right_height) + 1
            return root.height
        else:
            return -1

    root = Node()
    _construct_tree(root, snail_number)
    set_heights(root)
    return root


def set_height_upwards(leaf: Node):
    if leaf:
        left_height = leaf.left.height if leaf.left else -1
        right_height = leaf.right.height if leaf.right else -1

        leaf.height = max(left_height, right_height) + 1
        set_height_upwards(leaf.parent)


def reduce(root: Node, other: Node = None):
    def addition(root: Node, other: Node):
        if other:
            new_root = Node(left=root, right=other)
            root.parent = other.parent = new_root
            set_height_upwards(root)
            return new_root
        else:
            return root

    def split(root: Node):
        if not root:
            return False

        if isinstance(root.value, int) and root.value >= 10:
            sub = Node(parent=root.parent, height=1)
            sub.left = Node(parent=sub, value=root.value // 2, height=0)
            sub.right = Node(parent=sub, value=(root.value + 1) // 2, height=0)

            if root is root.parent.left:
                root.parent.left = sub
            else:
                root.parent.right = sub
            set_height_upwards(sub)
            return True
        else:
            return split(root.left) or split(root.right)
    
    def explode(tree: Node, depth=int):
        if not tree:
            return False

        if depth <= 0 and tree.left and tree.left.value is not None and tree.right and tree.right.value is not None:
            if pred := in_order_predecessor(root, target=tree.left):
                pred.value += tree.left.value
            if succ := in_order_successor(root, target=tree.right):
                succ.value += tree.right.value

            new_child = Node(parent=tree.parent, value=0)
            if tree.parent.left is tree:
                tree.parent.left = new_child
            else:
                tree.parent.right = new_child
            set_height_upwards(new_child)
            return True
        else:
            return explode(tree.left, depth=depth - 1) or explode(tree.right, depth=depth - 1)

    root = addition(root, other)
    while True:
        if root.height > 4:
            explode(root, depth=4)
        elif any(x >= 10 for x in in_order(root)):
            split(root)
        else:
            break

    return root


def part1(lines: list) -> int:
    root = construct_tree(lines[0])
    for line in lines[1:]:
        root = reduce(root, construct_tree(line))

    return magintude(root)


def part2(lines: list) -> int:
    max_ = -1
    for a, b in it.permutations(lines, r=2):
        pair = reduce(construct_tree(a), construct_tree(b))
        max_ = max(max_, magintude(pair))
    
    return max_


if __name__ == '__main__':
    if __debug__:
        root = construct_tree([[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]])
        assert magintude(root) == 4140

        with open('example.txt') as in_file:
            lines = [eval(line.strip()) for line in in_file]
        
        assert part1(lines) == 4140
        assert part2(lines) == 3993

    with open('input.txt') as in_file:
        lines = [eval(line) for line in in_file]

    print(part1(lines))
    print(part2(lines))
