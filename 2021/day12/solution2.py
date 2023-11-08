import os
year, day = [2021, 12]
root = os.path.join(os.getcwd(), str(year), f"day{day}")

class Cavern:
    ...

class Cavern:
    def __init__(self, name: str):
        self.name = name
        self.isBig = (self.name == self.name.upper())
        self.connections: list[Cavern] = []
        self.routes = []

    def add_con(self, cavern):
        self.connections.append(cavern)

    def routesToEnd(self, enabled_print, stack: list[Cavern]) -> list[list[str]]:
        if (self.name == "end"):
            return [["end"]]

        routes = []
        for connection in self.connections:
            if connection.name == "start":
                continue

            temp_stack = [connection.name] + [self.name] + stack

            unique = []
            for node in temp_stack:
                if node not in unique:
                    unique.append(node)

            counts = [*map(temp_stack.count, [s for s in unique if s.upper() != s])]

            if sum([x == 2 for x in counts]) > 1 or any([x > 2 for x in counts]):
                continue

            connected_routes = connection.routesToEnd(enabled_print, stack+[self.name])
            for route in connected_routes:
                route = [self.name] + route

                visited: list[str] = []
                for node in route:
                    if node not in visited:
                        visited.append(node)
                
                add = 0
                counts = [route.count(node) for node in visited]

                for (node, count) in zip(visited, counts):
                    if node.upper() != node and count == 2:
                        add += 1
                    
                    if node.upper() != node and count > 2:
                        add = 2

                if add <= 1 or self.isBig: 
                    routes.append(route)

        return routes

def main(enabled_print=True, test=False):
    if test:
        with open(os.path.join(root, "test.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]
    else:
        with open(os.path.join(root, "input.txt"), 'r') as f:
            inp = [line.strip() for line in f.readlines()]

    graph = {}
    for line in inp:
        start, end = line.split("-")

        if start not in graph.keys():
            graph[start] = []
        graph[start].append(end)

        if end not in graph.keys():
            graph[end] = []
        graph[end].append(start)

    nodes: list[Cavern] = []
    for key in graph.keys():
        nodes.append(Cavern(key))

    for node in nodes:
        for connection in graph[node.name]:
            for con_node in nodes:
                if con_node.name == connection:
                    node.add_con(con_node)

    start_node = None
    for node in nodes:
        if node.name == "start":
            start_node = node
    
    if start_node == None:
        print("Error finding start node")
        return -1
    
    routes = start_node.routesToEnd(enabled_print, [])

    if enabled_print:
        print(*routes, sep='\n')
    
    return len(routes)

if __name__ == "__main__":
    from aocd import submit

    import bs4
    import copier
    import sys

    if (len(sys.argv) < 3):
        print("Enter command line arguments")
        exit(-1)
    
    arg_list = sys.argv[1:]
    complete = arg_list[0].lower() == "true"
    run_test = arg_list[1].lower() == "true"

    if (len(sys.argv) == 4):
        test_ans = int(sys.argv[3])
    elif (run_test):
        print("Provide answer to test")
        exit(-1)

    if (run_test and not os.path.exists(os.path.join(root, "test.txt"))):
        print("Test file does not exist")
        exit(-1)

    answer = main(not complete, run_test)
    
    if complete:
        r = submit(answer, year=year, day=day)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        message = soup.article.text
        if "That's the right answer" in message:
            Print("YIPPEE!!!!")
    elif run_test:
        print(f"The answer is {test_ans}, you got {answer}.")
        if (test_ans == answer):
            print(f"You got it right! Time to submit!")
        else:
            print("Time to change ur code :(")
    else:
        print(f"You got {answer}")