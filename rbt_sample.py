# 红黑树是一种自平衡的二叉搜索树，它具有以下特性：
# 1. 每个节点要么是红色，要么是黑色。
# 2. 根节点是黑色。
# 3. 每个叶子节点（NIL节点，空节点）是黑色。
# 4. 如果一个节点是红色的，则它的两个子节点都是黑色的。
# 5. 对于每个节点，从该节点到其所有后代叶子节点的简单路径上，均包含相同数目的黑色节点。

# 下面是用Python实现红黑树的插入、删除和查找操作的基本思路：

# 插入操作：
# 1. 将新节点插入到红黑树中的合适位置，并将其标记为红色。
# 2. 根据红黑树的特性，对插入的节点进行调整，以保持红黑树的平衡性和特性。

# 删除操作：
# 1. 找到要删除的节点，并将其替换为其后继节点或前驱节点。
# 2. 根据红黑树的特性，对替换后的节点进行调整，以保持红黑树的平衡性和特性。

# 查找操作：
# 从根节点开始，比较要查找的值与当前节点的值，根据比较结果选择左子树或右子树进行进一步查找，直到找到目标值或遍历到叶子节点为止。

# 下面是用Python实现红黑树的插入、删除和查找操作的示例代码：

# ```python
# 红黑树节点类
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.color = "RED"  # 初始插入的节点为红色

# 红黑树类
class RedBlackTree:
    def __init__(self):
        self.root = None

    # 插入操作
    def insert(self, value):
        node = Node(value)
        if self.root is None:
            self.root = node
            node.color = "BLACK"  # 根节点为黑色
        else:
            self._insert_helper(node, self.root)
            self._insert_fixup(node)

    def _insert_helper(self, node, current):
        if node.value < current.value:
            if current.left is None:
                current.left = node
                node.parent = current
            else:
                self._insert_helper(node, current.left)
        else:
            if current.right is None:
                current.right = node
                node.parent = current
            else:
                self._insert_helper(node, current.right)

    def _insert_fixup(self, node):
        while node.parent and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle and uncle.color == "RED":  #case1:node的父节点为祖父结点的左孩子，且uncle存在并为红色 (叔，父节点祖父结点变色，node变为祖父结点继续循环检查)
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:   #case2:node的父节点为祖父结点的左孩子，且uncle不存在或存在为黑色 注意祖父结点父节点node必须在一条直线上，不然旋转掰直
                        node = node.parent          #(若node为父节点的右孩子，则node变为父节点左旋掰直。父节点，祖父结点变色，祖父结点右旋)
                        self._left_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left 
                if uncle and uncle.color == "RED":  #case3:node的父节点为祖父结点的右孩子，且uncle存在且为红色  (叔，父节点祖父结点变色，node变为祖父结点继续循环检查)
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:   
                    if node == node.parent.left:    #case4:node的父节点为祖父结点的右孩子，且uncle不存在或存在为黑色 旋转后node依旧处于原本的深度
                        node = node.parent          #(node为父节点的左孩子，则node变为父节点右旋掰直。父节点，祖父结点变色，祖父结点左旋)
                        self._right_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._left_rotate(node.parent.parent)
        self.root.color = "BLACK"

    # 删除操作
    def delete(self, value):
        node = self._search(value)
        if node is None:
            return
        self._delete_node(node)

    def _delete_node(self, node):
        if node.left and node.right:
            successor = self._minimum(node.right)
            node.value = successor.value
            self._delete_node(successor)
        else:
            child = node.left if node.left else node.right
            if child:
                child.parent = node.parent
            if not node.parent:
                self.root = child
            else:
                if node == node.parent.left:
                    node.parent.left = child    #child不存在会直接指向None
                else:
                    node.parent.right = child
            if node.color == "BLACK":
                self._delete_fixup(child, node.parent)

    def _delete_fixup(self, node, parent):
        while node != self.root and (not node or node.color == "BLACK"): #node必须为黑色，不然从根结点出发会少一个黑结点
            if node == parent.left:
                sibling = parent.right
                if sibling.color == "RED":  #兄弟为红，父结点变红，兄弟变黑，父节点旋转防止连红
                    sibling.color = "BLACK"
                    parent.color = "RED"
                    self._left_rotate(parent)
                    sibling = parent.right
                if (not sibling.left or sibling.left.color == "BLACK") and \
                        (not sibling.right or sibling.right.color == "BLACK"):  #兄弟结点，兄弟的左右结点均为黑，兄弟变红，需要fix的结点变为父结点，更新父结点
                    sibling.color = "RED"
                    node = parent
                    parent = node.parent
                else:
                    if not sibling.right or sibling.right.color == "BLACK": #兄弟结点，右孩子为黑，左孩子为红，将兄弟置红，左结点置黑，兄弟结点右旋，更新兄弟结点
                        sibling.left.color = "BLACK"
                        sibling.color = "RED"
                        self._right_rotate(sibling)
                        sibling = parent.right
                    sibling.color = parent.color    #兄弟结点为黑，右孩子为红，兄弟结点和父结点交换颜色，右孩子置黑，父结点左旋，fix结束，node置为root
                    parent.color = "BLACK"
                    sibling.right.color = "BLACK"
                    self._left_rotate(parent)
                    node = self.root
            else:
                sibling = parent.left
                if sibling.color == "RED":
                    sibling.color = "BLACK"
                    parent.color = "RED"
                    self._right_rotate(parent)
                    sibling = parent.left
                if (not sibling.right or sibling.right.color == "BLACK") and \
                        (not sibling.left or sibling.left.color == "BLACK"):
                    sibling.color = "RED"
                    node = parent
                    parent = node.parent
                else:
                    if not sibling.left or sibling.left.color == "BLACK":
                        sibling.right.color = "BLACK"
                        sibling.color = "RED"
                        self._left_rotate(sibling)
                        sibling = parent.left
                    sibling.color = parent.color
                    parent.color = "BLACK"
                    sibling.left.color = "BLACK"
                    self._right_rotate(parent)
                    node = self.root
        if node:
            node.color = "BLACK"

    # 查找操作
    def search(self, value):
        node = self._search(value)
        return node is not None

    def _search(self, value):
        current = self.root
        while current and current.value != value:
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return current

    def _minimum(self, node):
        while node.left:
            node = node.left
        return node

    # 左旋转操作
    def _left_rotate(self, node):
        right_child = node.right
        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node
        right_child.parent = node.parent
        if not node.parent:
            self.root = right_child
        else:
            if node == node.parent.left:
                node.parent.left = right_child
            else:
                node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    # 右旋转操作
    def _right_rotate(self, node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node
        left_child.parent = node.parent
        if not node.parent:
            self.root = left_child
        else:
            if node == node.parent.right:
                node.parent.right = left_child
            else:
                node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

# 示例代码使用：
# tree = RedBlackTree()
# tree.insert(10)
# tree.insert(20)
# tree.insert(30)
# tree.insert(40)
# tree.insert(50)

# print(tree.search(30))  # True
# print(tree.search(60))  # False

# tree.delete(30)
# print(tree.search(30))  # False


