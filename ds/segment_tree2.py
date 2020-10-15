# -*- coding: utf-8 -*-

# 以下是带懒惰标记的线段树
class TreeNode(object):
	def __init__(self, irange):
		self.lchild = None
		self.rchild = None
		self.irange = irange
		self.sum_value = 0  # 和
		self.lazy = 0  # 懒惰标记


class SegmentTree2(object):
	def __init__(self, irange):
		self.root = TreeNode(irange)
		self.build_tree()

	def build_tree(self):
		self._build(self.root, self.root.irange)

	def add(self, l, r, w):
		l, r = self.bounds_check(l, r)
		if l is None:
			return
		self._add(self.root, l, r, w)

	def query_sum(self, l, r):
		l, r = self.bounds_check(l, r)
		if l is None:
			return
		return self._query_sum(self.root, l, r)

	def bounds_check(self, l, r):
		l = max(l, self.root.irange[0])
		r = min(r, self.root.irange[1])
		if l > r:
			return None, None
		return l, r

	def _build(self, node, irange):
		l, r = irange
		if l == r:
			return
		mid = (l + r) / 2
		node.lchild = TreeNode((l, mid))
		self._build(node.lchild, (l, mid))
		node.rchild = TreeNode((mid + 1, r))
		self._build(node.rchild, (mid + 1, r))

	def _add(self, node, l, r, w):
		cl, cr = node.irange
		if l <= cl and cr <= r:
			node.sum_value += (cr - cl + 1) * w
			# 叶子节点不能加懒惰标记
			if cl != cr:
				node.lazy += w
			return

		# 下放懒惰标记
		if node.lazy and l != r:
			node.lchild.sum_value += node.lazy
			node.lchild.lazy += node.lazy

			node.rchild.sum_value += node.lazy
			node.rchild.lazy += node.lazy

			node.lazy = 0

		mid = (cl + cr) / 2
		# 如果左孩子需要下传标记
		if l <= mid:
			self._add(node.lchild, l, r, w)

		# 如果右孩子需要下传标记
		if r > mid:
			self._add(node.rchild, l, r, w)

		node.sum_value = node.lchild.sum_value + node.rchild.sum_value

	def _query_sum(self, node, l, r):
		cl, cr = node.irange
		if l <= cl and cr <= r:
			return node.sum_value

		if node.lazy and l != r:
			lchild = node.lchild
			lchild.sum_value += node.lazy * (lchild.irange[1] - lchild.irange[0] + 1)
			lchild.lazy += node.lazy

			rchild = node.rchild
			rchild.sum_value += node.lazy * (rchild.irange[1] - rchild.irange[0] + 1)
			rchild.lazy += node.lazy

			node.lazy = 0

		_sum = 0
		mid = (cl + cr) / 2
		# 如果左孩子符合范围
		if l <= mid:
			_sum += self._query_sum(node.lchild, l, r)

		# 如果右孩子符合范围
		if r > mid:
			_sum += self._query_sum(node.rchild, l, r)

		return _sum


seg_tree = SegmentTree2((1, 5))
seg_tree.add(1, 1, 1)
seg_tree.add(2, 2, 5)
seg_tree.add(3, 3, 4)
seg_tree.add(4, 4, 2)
seg_tree.add(5, 5, 3)

print seg_tree.query_sum(2, 4)
seg_tree.add(2, 3, 2)
print seg_tree.query_sum(3, 4)
seg_tree.add(1, 5, 1)
# print seg_tree.query_sum(1, 4)
print seg_tree.query_sum(1, 5)
print seg_tree.query_sum(2, 5)
