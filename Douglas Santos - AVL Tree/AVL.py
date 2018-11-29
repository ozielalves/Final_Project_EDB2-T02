class Node(object):
	left_rotation_count = 0
	right_rotation_count = 0
	def __init__(self, value = None, left = None, right = None):
		self.value = value
		self.parent = None
		self.left = left
		self.right = right
		self.height = 1

	def _str(self):		
		label = str(self.value) + '^' + str(self.height)
		if self.left is None:
			left_lines, left_pos, left_width = [], 0, 0
		else:
			left_lines, left_pos, left_width = self.left._str()
		if self.right is None:
			right_lines, right_pos, right_width = [], 0, 0
		else:
			right_lines, right_pos, right_width = self.right._str()
		middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
		pos = left_pos + middle // 2
		width = left_pos + middle + right_width - right_pos
		while len(left_lines) < len(right_lines):
			left_lines.append(' ' * left_width)
		while len(right_lines) < len(left_lines):
			right_lines.append(' ' * right_width)
		if (middle - len(label)) % 2 == 1 and self.parent is not None and \
		   self is self.parent.left and len(label) < middle:
			label += ' '
		label = label.center(middle, '.')
		if label[0] == '.': label = ' ' + label[1:]
		if label[-1] == '.': label = label[:-1] + ' '
		lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
				 ' ' * left_pos + '/' + ' ' * (middle-2) +
				 '\\' + ' ' * (right_width - right_pos)] + \
		  [left_line + ' ' * (width - left_width - right_width) + right_line
		   for left_line, right_line in zip(left_lines, right_lines)]
		return lines, pos, width
 
	def __str__(self):
		return '\n'.join(self._str()[0])

	def search(self, value):
		if self.value == value:
			return self
		else:
			if value < self.value:
				if self.left != None:
					return self.left.search(value)
				else:
					return None
			else:
				if self.right != None:
					return self.right.search(value)
				else:
					return None

	
	def insert(self, item):
		if self.value == None:
			self.value = item
			return self
			
		if self.value == item:
			return self
		else:
			if item < self.value:
				if self.left != None:
					self.left = self.left.insert(item)
					self.left.parent = self
				else:
					self.left = Node(item)
					self.left.parent = self
			else:
				if self.right != None:
					self.right = self.right.insert(item)
					self.right.parent = self
				else:
					self.right = Node(item)
					self.right.parent = self

			self.height = max(0 if self.left == None else self.left.height, 0 if self.right == None else self.right.height) + 1

			balance = self.balance()

			if balance > 1 and self.left != None and item < self.left.value:
				return self.rightRotate()
			if balance < -1 and self.right != None and item > self.right.value:
				return self.leftRotate()
			if balance > 1 and self.left != None and item > self.left.value:
				self.left = self.left.leftRotate()
				self.left.parent = self
				return self.rightRotate()
			if balance < -1 and self.right != None and item < self.right.value:
				self.right = self.right.rightRotate()
				self.right.parent = self
				return self.leftRotate()
		return self

	def delete(self, value):
		if not self:
			return self
		elif value < self.value:
			self.left = self.left.delete(value)
		elif value > self.value:
			self.right = self.right.delete(value)
		else:
			if self.left == None:
				temp, self = self.right, None
				return temp
			elif self.right is None:
				temp, self = self.left, None
				return temp
			temp = self.left.highest()
			self.value = temp.value
			self.left = self.left.delete(temp.value)
		
		if self is None:
			return self

		self.height = max(0 if self.left == None else self.left.height, 0 if self.right == None else self.right.height) + 1

		balance = self.balance()

		if balance > 1 and (self.left == None or self.left.balance() >= 0):
			return self.rightRotate()
		if balance > 1 and self.left != None and self.left.balance() < 0:
			self.left = self.left.leftRotate()
			self.left.parent = self
			return self.rightRotate()
		if balance < -1 and (self.right == None or self.right.balance() < 0):
			return self.leftRotate()
		if balance < -1 and self.right != None and self.right.balance() > 0:
			self.right = self.right.rightRotate()
			self.right.parent = self
			return self.leftRotate()
		return self


	def balance(self):
		left = 0
		right = 0
		if self.left != None:
			left = self.left.height
		if self.right != None:
			right = self.right.height
		return left - right

	def rightRotate(self):
		Node.right_rotation_count += 1
		y = self
		x = y.left
		if x == None:
			T2 = None
		else:
			T2 = x.right

		x.right = y
		if y != None:
			y.parent = x
		y.left = T2
		if T2 != None:
			T2.parent = y

		y.height = max(0 if y.left == None else y.left.height, 0 if y.right == None else y.right.height) + 1
		x.height = max(0 if x.left == None else x.left.height, 0 if x.right == None else x.right.height) + 1
		x.parent = None
		return x

	def leftRotate(self):
		Node.left_rotation_count += 1
		x = self
		y = x.right
		T2 = y.left

		y.left = x
		if x != None:
			x.parent = y
		x.right = T2
		if T2 != None:
			T2.parent = x

		x.height = max(0 if x.left == None else x.left.height, 0 if x.right == None else x.right.height) + 1
		y.height = max(0 if y.left == None else y.left.height, 0 if y.right == None else y.right.height) + 1
		y.parent = None
		return y

	def lowest(self):
		if self.left != None:
			return self.left.lowest()
		else:
			return self
		

	def highest(self):
		if self.right != None:
			return self.right.highest()
		else:
			return self

	def successor(self):
		if self.right != None:
			return self.right.highest()

		x = self
		y = self.parent

		while y != None and x == y.right:
			x = y
			y = y.parent
		return y

	def predecessor(self):
		if self.left != None:
			return self.left.lowest()
		
		x = self
		y = self.parent

		while y != None and x == y.left:
			x = y
			y = y.parent

		return y
	
'''print("Insert - Left/Right Rebalance")
case1 = [20, 4, 26, 3, 9, 21, 30, 2, 7, 11]
tree1 = Node()
for i in case1:
	tree1 = tree1.insert(i)
print("Tree1: \n", tree1, '\n')'''

print("Insert - Left/Right Rebalance")
case1 = [20, 4]
case2 = [20, 4, 26, 3, 9]
case3 = [20, 4, 26, 3, 9, 21, 30, 2, 7, 11]
tree1 = Node()
tree2 = Node()
tree3 = Node()
for i in case1:
	tree1 = tree1.insert(i)
print("Tree1: \n", tree1, '\n')
for i in case2:
	tree2 = tree2.insert(i)
print("Tree2: \n",tree2, '\n')
for i in case3:
	tree3 = tree3.insert(i)
print("Tree3: \n", tree3, '\n')
print("Case1a: Insert 15")
case1a = tree1.insert(15)
print(case1a)
#------------------
print("Case2a: Insert 15")
case2a = tree2.insert(15)
print(case2a)
#------------------
print("Case3a: Insert 15")
case3a = tree3.insert(15)
print(case3a)
#------------------
tree1 = Node()
tree2 = Node()
tree3 = Node()
for i in case1:
	tree1 = tree1.insert(i)
for i in case2:
	tree2 = tree2.insert(i)
for i in case3:
	tree3 = tree3.insert(i)
print("Case2a: Insert 8")
tree1 = tree1.insert(8)
print(tree1)
#------------------
print("Case2b: Insert 8")
tree2 = tree2.insert(8)
print(tree2)
#------------------
print("Case3b: Insert 8")
tree3 = tree3.insert(8)
print(tree3)
#------------------

print("Delete - Double Rebalancing")
case1 = [5, 2, 8, 1, 3, 7, 4, 6, 9]
tree1 = Node()
for i in case1:
	tree1 = tree1.insert(i)
print("Tree1: \n", tree1, '\n')

print("Case1: Delete root(5)")
tree1 = tree1.delete(5)
print(tree1)
print("Case2: Delete node with two siblings(2)")
tree1 = tree1.delete(2)
print(tree1)
print("Case3: Delete node with one sibling(1) and rotation")
tree1 = tree1.delete(1)
print(tree1)

print("Search")
print(tree3)
print("Case3: Search 1")
for x in range(13):
	print("search(",x,"): ", end= "")
	result = tree3.search(x)
	if result is not None:
		print("encontrado")
	else:
		print("não encontrado")
print(tree3)
print(tree3.search(2).parent.value)


