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

def dfs_find_node(this_id,node=tree):
    return_id = 0
    if node.id = this_id:
        return node
    elif node.neighbours == NULL :
        return NULL
    else:
        for nei_node in node.neighbours:
            if dfs_find_node(this_id,nei_node)!= NULL
                return node





def dfs_add_node(parent_id, node_distance, node_direction):
    #add a node at specific parent




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
