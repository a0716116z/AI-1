import queue
from board import board
from board import position
from tree import node

def path_list(goal_node):
    ret = []
    tmp_node = goal_node
    while tmp_node != None:
        ret.append(tmp_node)
        tmp_node = tmp_node.parent
    ret.reverse()
    return ret


class agent:
    def __init__(self, start_, goal_):
        self.start = start_
        self.goal = goal_


class bfs(agent):
    def __init__(self, start_, goal_):
        super(bfs, self).__init__(start_, goal_)

    def search(self, b):
        root = node(None, self.start)

        explorered_set = []
        frontier = queue.Queue(maxsize = -1)
        frontier.put(root)
        
        while not frontier.empty():            
            cur_node = frontier.get()
            possible_moves = cur_node.position.available_moves(b)

            for new_pos in possible_moves:
                if new_pos not in explorered_set:
                    child = node(cur_node, new_pos)
                    cur_node.add_child(child)
                    frontier.put(child)
                    explorered_set.append(new_pos)
                    if new_pos == self.goal:
                        return path_list(child)                        
        return []

class dfs(agent):
    def __init__(self, start_, goal_):
        super(dfs, self).__init__(start_, goal_)

    def search(self, b):
        root = node(None, self.start)

        explorered_set = []
        frontier = [root]
        
        while len(frontier):            
            cur_node = frontier.pop()
            possible_moves = cur_node.position.available_moves(b)

            for new_pos in possible_moves:
                if new_pos not in explorered_set:
                    child = node(cur_node, new_pos)
                    cur_node.add_child(child)
                    frontier.append(child)
                    explorered_set.append(new_pos)
                    if new_pos == self.goal:
                        return path_list(child)
        return []


if __name__ == '__main__':
    b = board(8)
    p_start = position(0, 0)
    p_goal = position(2, 2)

    path = bfs(p_start, p_goal).search(b)
    # print(path)
    # b.print_pathway(path)

    path = dfs(p_start, p_goal).search(b)
    b.print_pathway(path)