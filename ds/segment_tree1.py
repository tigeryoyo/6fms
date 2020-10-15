# -*- coding: utf-8 -*-
"""
segment tree
https://oi-wiki.org/ds/seg/
https://www.luogu.com.cn/problem/P3372
"""


def build(array_a, array_d, s, t, p):
	# 构建线段树
	if s == t:
		array_d[p] = array_a[s]
	else:
		m = (s + t) >> 1
		build(array_a, array_d, s, m, 2 * p)
		build(array_a, array_d, m + 1, t, 2 * p + 1)
		array_d[p] = array_d[2 * p] + array_d[2 * p + 1]


def get_sum(array_d, l, r, s, t, p):
	# 获取区间 [l,r] 的和
	if l <= s and t <= r:
		return array_d[p]
	m, cnt = (s + t) / 2, 0
	if l <= m:
		cnt += get_sum(array_d, l, r, s, m, p * 2)
	if r > m:
		cnt += get_sum(array_d, l, r, m + 1, t, 2 * p + 1)

	return cnt


# 没有懒标记，效率较慢
class SegmentTree1(object):
	def __init__(self, start, end):
		self.start = start
		self.end = end
		self.max_value = {}
		self.sum_value = {}
		self.len_value = {}
		self._init(start, end)

	def out_of_bounds_check(self, start, end):
		start = max(start, self.start)
		end = min(end, self.end)
		if start > end:
			return None, None
		return start, end

	def add(self, start, end, weight=1):
		start, end = self.out_of_bounds_check(start, end)
		if start is None:
			return False
		self._add(start, end, weight, self.start, self.end)
		return True

	def query_max(self, start, end):
		start, end = self.out_of_bounds_check(start, end)
		if start is None:
			return None
		return self._query_max(start, end, self.start, self.end)

	def query_sum(self, start, end):
		start, end = self.out_of_bounds_check(start, end)
		if start is None:
			return 0
		return self._query_sum(start, end, self.start, self.end)

	def query_len(self, start, end):
		start, end = self.out_of_bounds_check(start, end)
		if start is None:
			return 0
		return self._query_len(start, end, self.start, self.end)

	def _init(self, start, end):
		self.max_value[(start, end)] = 0
		self.sum_value[(start, end)] = 0
		self.len_value[(start, end)] = 0
		if start < end:
			mid = start + int((end - start) / 2)
			self._init(start, mid)
			self._init(mid + 1, end)

	def _add(self, start, end, weight, in_start, in_end):
		key = (in_start, in_end)
		if in_start == in_end:
			self.max_value[key] += weight
			self.sum_value[key] += weight
			self.len_value[key] = 1 if self.sum_value[key] > 0 else 0
			return

		# mid = in_start + int((in_end - in_start) / 2)
		mid = (in_start + in_end) / 2
		if mid >= end:
			self._add(start, end, weight, in_start, mid)
		elif mid + 1 <= start:
			self._add(start, end, weight, mid + 1, in_end)
		else:
			self._add(start, mid, weight, in_start, mid)
			self._add(mid + 1, end, weight, mid + 1, in_end)
		self.max_value[key] = max(self.max_value[(in_start, mid)], self.max_value[(mid + 1, in_end)])
		self.sum_value[key] = self.sum_value[(in_start, mid)] + self.sum_value[(mid + 1, in_end)]
		self.len_value[key] = self.len_value[(in_start, mid)] + self.len_value[(mid + 1, in_end)]

	def _query_max(self, start, end, in_start, in_end):
		if start == in_start and end == in_end:
			ans = self.max_value[(start, end)]
		else:
			mid = in_start + int((in_end - in_start) / 2)
			if mid >= end:
				ans = self._query_max(start, end, in_start, mid)
			elif mid + 1 <= start:
				ans = self._query_max(start, end, mid + 1, in_end)
			else:
				ans = max(self._query_max(start, mid, in_start, mid),
				          self._query_max(mid + 1, end, mid + 1, in_end))
		# print start, end, in_start, in_end, ans
		return ans

	def _query_sum(self, start, end, in_start, in_end):
		if start == in_start and end == in_end:
			ans = self.sum_value[(start, end)]
		else:
			mid = in_start + int((in_end - in_start) / 2)
			if mid >= end:
				ans = self._query_sum(start, end, in_start, mid)
			elif mid + 1 <= start:
				ans = self._query_sum(start, end, mid + 1, in_end)
			else:
				ans = self._query_sum(start, mid, in_start, mid) + self._query_sum(mid + 1, end, mid + 1, in_end)
		return ans

	def _query_len(self, start, end, in_start, in_end):
		if start == in_start and end == in_end:
			ans = self.len_value[(start, end)]
		else:
			mid = in_start + int((in_end - in_start) / 2)
			if mid >= end:
				ans = self._query_len(start, end, in_start, mid)
			elif mid + 1 <= start:
				ans = self._query_len(start, end, mid + 1, in_end)
			else:
				ans = self._query_len(start, mid, in_start, mid) + self._query_len(mid + 1, end, mid + 1, in_end)

		# print start, end, in_start, in_end, ans
		return ans


seg_tree = SegmentTree1(1, 5)
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


# 以下是带懒惰标记的线段树
class TreeNode(object):
	def __init__(self, irange):
		self.lchild = None
		self.rchild = None
		self.irange = irange
		self.sum_value = 0  # 和
		self.lazy = 0  # 懒惰标记
