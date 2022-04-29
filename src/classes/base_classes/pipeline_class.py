"""
This script contains the buildingblocks used when building a pipeline.
"""

from collections import deque


class DAG:
    """
    Class to create a Directed Acyclic Graph.
    A graph is a pictorial representation or a diagram that represents a data structure that is composed of
    vertices (nodes) and edges (branches). The vertices (nodes) are each point in the graph, and the edges are
    the lines that connect them.
    """
    def __init__(self):
        self.graph = {}  # a dict of list. {node = [pointers to other nodes]}
        self.degrees = {}

    def add(self, node, branches_to=None):
        """
        Adds the given node to the graph dict.
        :param node: The node of the DAG that needs to be added to the graph
        :param branches_to: The node to which the edge of the added node points (or branches) to.
        :return:
        """
        if node not in self.graph:
            self.graph[node] = []
        if branches_to:  # Makes it possible to create nodes with multiple pointers pointed at them
            if branches_to not in self.graph:
                self.graph[branches_to] = []
            self.graph[node].append(branches_to)

        if len(self.sort()) > len(self.graph):  # Validity check.
            raise Exception(f'Cycle found in DAG. {self.sort()}\ngraph = {self.graph}')

    def in_degrees(self):
        """
        The number of in-degrees is the total count of edges pointing towards the node. A root node will always
        have 0 in-degrees.
        For each node, the amount of edges pointing towards that node need to be counted.
        :return:
        """
        self.degrees = {k: 0 for k in self.graph}
        for node in self.graph:
            for value in self.graph[node]:
                if value not in self.degrees:
                    self.degrees[value] = 1
                if value in self.degrees:
                    self.degrees[value] += 1

    def sort(self):
        """
        Sorting the graph dictionary based on their dependencies.
        The hypothesis is: the shorter the path, the more the node is depended on. Another way to state the
        hypothesis is: if there are root nodes, then those nodes are the most important nodes in the tree.
        If roots are the most important nodes, then what we should do is the following:
        1.  Filter all the root nodes, and pop them off the graph.
        2.  Search their pointers, and check if they are the new root nodes.
            - If one is, append it to the root nodes list, and pop it off the graph.
            - If not, then continue.
        3. Once all the nodes have been popped from the graph, return the list of ordered root nodes.
        :return: list of ordered root nodes
        """
        self.in_degrees()
        to_visit = deque()  # deque() = A list-like sequence optimized for data accesses near its endpoints.

        # Finding root nodes
        for node in self.graph:
            if self.degrees[node] == 0:
                to_visit.append(node)

        searched = []
        while to_visit:
            node = to_visit.popleft()
            for pointer in self.graph[node]:
                self.degrees[pointer] -= 1
                if self.degrees[node] == 0:
                    to_visit.append(pointer)
            searched.append(node)
        return searched


class Pipeline:

    def __init__(self):
        self.tasks = DAG()  # list (or graph) of tasks that need to be executed in the pipeline. The order of the list
        # is the order in which the tasks need to be executed.

    def task(self, depends_on=None):  # New version of task to fit with DAG  
        def inner(function):
            self.tasks.add(function)
            if depends_on:
                self.tasks.add(depends_on, function)
            return function
        return inner

    def run(self):
        """
        To run, create a task that begins the pipeline by returning a static object.
        Furthermore, there is no concept of a "last task" in a DAG. Therefore, the way we can represent our
        tasks, and their outputs during a run, is by using a dictionary that maps function: output. With this
        dictionary, it's able to store outputs after task completion so they can be used as inputs for the next tasks
        that require them.
        :return:
        """
        scheduled = self.tasks.sort()
        completed = {}  # dict that maps function: output
        for task in scheduled:
            for node, value in self.tasks.graph.items():  # value is a list of tasks that are dependent of the node

                if task in value:  # if task is found in value, the task needs to be executed with the answer provided by the previous node
                    completed[task] = task(completed[node])  # completed[node] gives the answer of the node that points to the node of the task that needs to be excecuted

            if task not in completed:
                completed[task] = task()

        return completed
