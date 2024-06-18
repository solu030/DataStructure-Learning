class Node:
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.color = "RED"

class RedBlackTree:
    def __init__(self):
        self.root = None

    def search(self,value):
        node = self._search(value)
        if node:
            return node 
        print("未找到目标结点" + str(value),type(node))
        return

    def _search(self,value):
        current = self.root
        while current and current.value != value:
            if current.value < value:
                current = current.right
            else :
                current = current.left
        return current

    def minimal(self,node):
        while node.left:
            node = node.left
        return node

    # 主要是连三条线 以node为平辈，连右孩子的左孩子和node的右孩子 连右孩子和node的父节点 连右孩子和node 其中右孩子的左孩子，父节点需要判断是否存在
    # 左旋 即将本结点旋转为右孩子的左孩子 右旋与左旋同理，连好三条线即可
    def left_rotate(self,node):
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

    def right_rotate(self,node):
        left_child = node.left
        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node
        left_child.parent = node.parent
        if not node.parent:
            self.root = left_child
        else:
            if node == node.parent.left:
                node.parent.left = left_child
            else:
                node.parent.right = left_child
        left_child.right = node
        node.parent = left_child

    def insert(self,value):
        node = Node(value)
        if self.root is None:
            self.root = node
            node.color = "BLACK"
        else:
            self.insert_body(node,self.root)
            self.insert_fix(node)

    def insert_body(self,node,current):
        if node.value < current.value:
            if current.left is not None:
                self.insert_body(node,current.left)
            else:
                node.parent = current
                current.left = node
        else:
            if current.right is not None:
                self.insert_body(node,current.right)
            else:
                current.right = node
                node.parent = current

    def insert_fix(self,node):
        while node.parent and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle and uncle.color == "RED":  #case1:node的父节点为祖父结点的左孩子，且uncle存在并为红色 (叔，父节点祖父结点变色，node变为祖父结点继续循环检查)
                    uncle.color = "BLACK"
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:    #case2:node的父节点为祖父结点的左孩子，且uncle不存在或存在为黑色 注意祖父结点父节点node必须在一条直线上，不然旋转掰直
                        node = node.parent           #(若node为父节点的右孩子，则node变为父节点左旋掰直。父节点，祖父结点变色，祖父结点右旋)
                        self.left_rotate(node)
                    node.parent.color == "BLACK"
                    node.parent.parent.color = "RED"
                    self.right_rotate(node.parent.parent) #更新后祖父结点为红色，为了防止祖父结点出现连红，右旋
            else:
                uncle = node.parent.parent.left
                if uncle and uncle.color == "RED":   #case3:node的父节点为祖父结点的右孩子，且uncle存在且为红色  (叔，父节点祖父结点变色，node变为祖父结点继续循环检查)
                    uncle.color = "BLACK"
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:    #case4:node的父节点为祖父结点的右孩子，且uncle不存在或存在为黑色 旋转后node依旧处于原本的深度
                        node = node.parent          #(node为父节点的左孩子，则node变为父节点右旋掰直。父节点，祖父结点变色，祖父结点左旋)
                        self.right_rotate(node)          #右旋 == 顺时针旋转至平行 再平移至结点相连？ 左旋 == 逆时针旋转？ 
                    node.parent.color == "BLACK"
                    node.parent.parent == "RED"
                    self.left_rotate(node.parent.parent)
            self.root.color = "BLACK"

    def delete(self,value):
        node = self.search(value)
        if node is None:
            return
        self.delete_body(node) 

    def delete_body(self,node):
        if node.left and node.right:
            min_node = self.minimal(node.right)  #只可能有右孩子或没有孩子
            node.value = min_node.value
            self.delete_body(min_node)
        else:
            child = node.left if node.left else node.right #
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
                self.delete_fix(child,node.parent)
        if self.root:
            self.root.color = "BLACK"

    def delete_fix(self,node,parent):
        while node != self.root and (not node or node.color == "BLACK"):    #node必须为黑色，不然从根结点出发会少一个黑结点
            if node == parent.left:
                sibling = parent.right
                if not sibling:     #没有兄弟结点,相当于父结点只有一条路径，直接把node置黑即可退出
                    node = self.root
                    continue
                if sibling.color == "RED":  #兄弟为红，父结点变红，兄弟变黑，父结点旋转防止连红
                    parent.color = "RED"
                    sibling.color = "BLACK"
                    self.left_rotate(parent)
                    sibling  = parent.right #新兄弟
                else:
                    if (not sibling.left or sibling.left.color == "BLACK") and (not sibling.right or sibling.right.color == "BLACK"):
                        sibling.color = "RED"
                        node = parent           #兄弟结点，兄弟的左右结点均为黑，兄弟变红，需要fix的结点变为父结点，更新父结点
                        parent = node.parent
                    else:
                        if not sibling.right or sibling.right.color == "BLACK": #兄弟结点，右孩子为黑，左孩子为红，将兄弟置红，左结点置黑，兄弟结点右旋，更新兄弟结点
                            sibling.left.color = "BLACK"
                            sibling.color = "RED"
                            self.left_rotate(sibling)
                            sibling = parent.right
                        sibling.color = parent.color    #兄弟结点为黑，右孩子为红，兄弟结点和父结点交换颜色，右孩子置黑，父结点左旋，fix结束，node置为root
                        parent.color = "BLACK"
                        sibling.right.color = "BLACK"
                        self.left_rotate(parent)
                        node = self.root
            else:
                sibling = parent.left
                if not sibling:
                    node = self.root
                    continue
                if sibling.color == "RED":
                    sibling.color = "BLACK"
                    parent.color = "RED"
                    self.right_rotate(parent)
                    sibling = parent.left
                else:
                    if (not sibling.left or sibling.left.color == "BLACK") and (not sibling.right or sibling.right.color == "BLACK"):
                        sibling.color = "RED"
                        node = parent
                        parent = node.parent
                    else:
                        if not sibling.left or sibling.left.color == "BLACK":   #兄弟结点在左，若右孩子为红，转变为左孩子为红，使红孩子与兄弟平行
                            sibling.color = "RED"
                            sibling.right.color = "BLACK"
                            self.left_rotate(sibling)
                            sibling = parent.left
                        sibling.color = parent.color
                        parent.color = "BLACK"
                        sibling.left.color = "BLACK"
                        self.right_rotate(parent)
                        node = self.root
            if node:
                node.color = "BLACK"


    def show(self):
        current = self.root
        self.show_rbt(current)

    def show_rbt(self,node):
        if node is not None:
            print(node.value,node.color)
            self.show_rbt(node.left)
            self.show_rbt(node.right)


# 插入：uncle为红，叔，父变黑，祖父变红，node变祖父。   uncle为黑，检查node，父，祖父是否平行，不平行旋转掰直，父结点变黑，祖父变红，祖父旋转到父结点下 1(u红) + 1.5(黑)
# 插入规律，父辈结点变黑，祖父结点变红，祖父结点旋转或变为node
# 删除：兄弟为红，兄弟变黑，祖父变红，祖父旋转到兄弟下，更新兄弟。      兄弟三黑，兄弟变红，node变为父结点，更新父结点。    1(s红) + 1(三黑) + 1.5(单红)
# 兄弟红结点不平行，兄弟变红，红结点变黑，兄弟旋转，更新兄弟结点。      兄弟红结点平行，兄弟变为父结点颜色，父结点变黑，红结点变黑，父结点旋转至兄弟下，退出删除循环


# rbt = RedBlackTree()
# data_list = [23,44,34,67,33,43,65,77,98,56]
# delete_list = [23,67,34,77,98,56]
# for i in data_list:
#     rbt.insert(i)
# for i in delete_list:
#     rbt.delete(i)
# rbt.show()