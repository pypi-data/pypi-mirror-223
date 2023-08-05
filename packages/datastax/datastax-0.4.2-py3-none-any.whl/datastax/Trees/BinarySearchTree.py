import warnings
from typing import Any, Optional, Self, Sequence

from datastax.Utils.Warnings import (
    DuplicateNodeWarning,
    DeletionFromEmptyTreeWarning,
    NodeNotFoundWarning
)
from datastax.Nodes import TreeNode
from datastax.Trees.BinaryTree import BinaryTree


class BinarySearchTree(BinaryTree):
    def insert(self, data: Any) -> None:
        root = self.root
        if data is None:
            return
        result = self._place(root, data)
        if result:
            self.set_root(result)

    def _construct(self, items: Optional[Sequence] = None) -> Self | None:
        if not items or items[0] is None:
            return None
        for item in items:
            self.insert(item)
        return self

    def search(self, data: Any):
        """
        Searches a node in log2(n) time complexity BinarySearch Algorithm
        :param data: Any type of content in BST to search
        :return: TreeNode if it is found else None
        """
        if data is None:
            return None

        def _search(node):
            if not node:
                return
            if data == node.data:
                return node
            return _search(node.left if data < node.data else node.right)

        if not self.root:
            warnings.warn(
                f"Node was not found with current data '{data}'. "
                f"Tree is empty", NodeNotFoundWarning
            )
            return None
        result = _search(self.root)
        if not result:
            warnings.warn(
                f"Node was not found with current data '{data}'. ",
                NodeNotFoundWarning
            )
        return result

    # Private helper function for inserting
    def _place(self, parent, data) -> Optional[TreeNode]:
        if not parent:
            return TreeNode(data)
        elif parent.data < data:
            parent.set_right(self._place(parent.right, data))
        elif parent.data > data:
            parent.set_left(self._place(parent.left, data))
        else:
            warnings.warn(
                f"Insertion unsuccessful. Item '{data}' already exists "
                "in Tree", DuplicateNodeWarning
            )
        return parent

    @staticmethod
    def inorder_predecessor(node):
        node = node.left
        while node and node.right:
            node = node.right
        return node

    def _delete(self, root, item: Any):
        if not root:
            return None
        if root.data == item:
            # Node with only rightChild, replace with left_child
            if root.left is None:
                return root.right
            # Node with only leftChild, replace with right_child
            if root.right is None:
                return root.left
            # Node with both children, replace with inorder_predecessor
            predecessor = self.inorder_predecessor(root)
            root.data = predecessor.data
            root.set_left(self._delete(root.left, root.data))
        elif item < root.data:
            root.set_left(self._delete(root.left, item))
        elif root.data < item:
            root.set_right(self._delete(root.right, item))
        return root

    def delete(self, data: Any = None) -> None:
        """
        Deletes a node which has the data and replaces with inorder predecessor
        :param data: An item corresponding to the node to be deleted
        :return: returns data if node is found else None and raises warning
        """
        if not self.root:
            warnings.warn(
                "Deletion Unsuccessful. Can't delete from empty Tree",
                DeletionFromEmptyTreeWarning
            )
            return
        if not self.search(data):
            warnings.warn(
                "Deletion unsuccessful. Node was not found with current "
                f"data '{data}'", NodeNotFoundWarning
            )
            return
        self.set_root(self._delete(self.root, data))
