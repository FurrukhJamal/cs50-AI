class Node():
    def __init__(self, state, parent, action, nodeMovies, movies):
        self.state = state
        self.parent = parent
        self.action = action
        # test adding neighbours
        # self.neighbors = set()
        self.neighbors = []
        for movie in nodeMovies:
            for star in movies[movie]["stars"]:
                if star != state:
                    self.neighbors.append((star, movie))
        # print(f"self.neighbors : {self.neighbors}")
    
    def getNeighbors(self):
        return self.neighbors 

    def __hash__(self):
        return hash(self.state)


    def __eq__(self, other):
        return self.state == other.state and self.action == other.action

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


if __name__ == "__main__":
    print("working")
    test1 = Node(1, None, None)
    test2 = Node(1, "hello", "world")

    print(test1 == test2)