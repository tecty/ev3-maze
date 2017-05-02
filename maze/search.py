class Node:

	def __init__(self, id, neighbours):
		self.id = id
		self.neighbours = neighbours

def dfs_recursive(node):
	print 'Node ', node.id
	if node.neighbours == []:
		return
	for next in node.neighbours:
		dfs_recursive(next)

def dfs_open_list(start):
	open_list = [start]
	while open_list != []:
		first, rest = open_list[0], open_list[1:]
		print 'Node ', first.id
		open_list = first.neighbours + rest

def bfs_open_list(start):
	open_list = [start]
	while open_list != []:
		first, rest = open_list[0], open_list[1:]
		print 'Node ', first.id
		open_list = rest + first.neighbours

def dfs_stack(start):

	stack = [None]*10
	stack[0] = start
	stack_pointer = 0

	while stack_pointer >= 0:
		current = stack[stack_pointer]
		stack_pointer -= 1
		print 'Node ', current.id
		if current.neighbours != []:
			for n in reversed(current.neighbours):
				stack_pointer += 1
				stack[stack_pointer] = n

tree = Node(1,
		[Node(2,
			[Node(3, []),
			 Node(4, [])]),
		 Node(5,
			[Node(6, [])])])

print "Recursive Depth First Search"
dfs_recursive(tree)
print "Iterative Depth First Search"
dfs_open_list(tree)
print "Breadth First Search"
bfs_open_list(tree)
print "Depth First Search with Stack"
dfs_stack(tree)
