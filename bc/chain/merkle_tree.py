import hashlib
from typing import List
import bc.transactions as Transactions


class Node:
    def __init__(self, left, right, value=None, content: Transactions.Transaction = None):
        self.left: Node = left
        self.right: Node = right
        self.value = str(content.hash) or str(value)
        self.content = content

    @staticmethod
    def hash(val) -> str:
        return str(hashlib.sha256(str(val).encode('utf-8')).hexdigest())

    def __str__(self):
        return str(self.value)


class MerkleTree:
    def __init__(self, values: List[Transactions.Transaction]):
        self.__buildTree(values)

    def __buildTree(self, values: List[Transactions.Transaction]):

        leaves: List[Node] = [Node(None, None, e.hash, e) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1:][0])  # duplicate last elem if odd number of elements
            self.root: Node = self.__buildTreeRec(leaves)

    def __buildTreeRec(self, nodes: List[Node]) -> Node:
        half: int = len(nodes) // 2

        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], Node.hash(nodes[0].value + nodes[1].value))
        left: Node = self.__buildTreeRec(nodes[:half])
        right: Node = self.__buildTreeRec(nodes[half:])
        value: str = Node.hash(left.value + right.value)
        content: Transactions = None
        return Node(left, right, value, content)

    def printTree(self):
        self.__printTreeRec(self.root)

    def __printTreeRec(self, node):
        if node is not None:
            if node.left is not None:
                print("Left: " + str(node.left))
                print("Right: " + str(node.right))
            else:
                print("Input")

            print("Value: " + str(node.value))
            print("Content: " + node.content)
            print("")
            self.__printTreeRec(node.left)
            self.__printTreeRec(node.right)

    def getRootHash(self) -> str:
        return self.root.value
