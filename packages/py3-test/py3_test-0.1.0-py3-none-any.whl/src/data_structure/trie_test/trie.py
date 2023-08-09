class TrieTree:
    def __init__(self):
        self.tree = {}

    def add(self, word):
        """
        添加节点
        :param word:
        :return:
        """
        tree = self.tree
        for char in word:
            if char in tree:
                tree = tree[char]
            else:
                tree[char] = {}
                tree = tree[char]
        tree["_end_"] = True

    def search(self, word):
        """
        搜索子节点
        :param word:
        :return:
        """
        tree = self.tree

        for char in word:
            if char in tree:
                tree = tree[char]
            else:
                return False
        return tree

    def count(self, word):
        """
        统计所有路径个数
        :param word:
        :return:
        """
        tree = self.tree
        for char in word:
            if char in tree:
                tree = tree[char]
            else:
                return 0
        return str(tree).count("True")

    def is_end(self, word):
        """
        判断是不是完整路径
        :param word:
        :return:
        """
        tree = self.tree

        for char in word:
            if char in tree:
                tree = tree[char]
            else:
                return False
        return tree.get("_end_", False)


if __name__ == "__main__":
    tree = TrieTree()
    tree.add(["a", "b", "c"])
    tree.add(["a", "b", "d"])
    tree.add(["a", "b", "c", "d"])
    tree.add(["a", "b", "c", "e"])
    tree.add(["b", "c", "d"])
    print(tree.tree)
    print(tree.search(["a", "b"]))
    print(tree.is_end(["a", "b"]))
    print(tree.is_end(["a", "b", "c"]))
    print(tree.count(["a", "b"]))

    # tree.add("abc")
    # tree.add("bcd")
    # print((tree.is_end("ab")))
    # print((tree.is_end("abc")))
