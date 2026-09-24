'''
An unweighted, undirected Graph class based on an adjacency list model.
'''
class GraphHelper:
    def __init__(self, adjacency_list:dict[str, set[str]]):
        '''The Graph class constructor.
          Inititalizes the following data attributes:
            - self.__adjacency_list (dict[str, st[str]]): An adjacency list model of our Graph
            - self.__vertices (set[str]): A set of all the vertices/nodes in the graph
            - self.__edges (set[tuple[str, str]]]): A set of sorted tuples representing all the edges in the graph 

            Args:
              adjacency_list (dict[str, set[str]]): An adjacency list model of our Graph
        '''
        self.__adjacency_list = adjacency_list
        self.__vertices = set(self.adjacency_list.keys()) 

        edges = set()
        for key in self.__adjacency_list:
          vertex1 = key

          for endpoint in self.__adjacency_list[key]:
              vertex2 = endpoint
              
              edges.add(tuple(sorted([vertex1, vertex2])))
        self.__edges = edges


    @property
    def adjacency_list(self):
      return self.__adjacency_list
    
    @property
    def vertices(self):
      return self.__vertices

    @property
    def edges(self):
      return self.__edges
    
    def is_vertex(self, vertex:str) -> bool:
        """Checks if a given vertex exists in the graph.

        Args:
            vertex (str): The vertex to check for existence in the graph.

        Returns:
            bool: True if the vertex exists in the graph, False otherwise.
        
        Examples:
        >>> graph = {'A':['B'],'B':['A', 'E'],'E':['B']}
        >>> graph_helper = GraphHelper(graph)
        >>> graph_helper.is_vertex('A')
        True

        >>> graph = {'A':['B'],'B':['A', 'E'],'E':['B']}
        >>> graph_helper = GraphHelper(graph)
        >>> graph_helper.is_vertex('C')
        False
        """

        for key in self.__adjacency_list:
           if vertex == key:
              return True

        return False 

    def get_neighbors(self, vertex:str) -> set[str]:
        '''Accessor method for the neighbors of an edge

            Args:
              vertex (str): The given vertex

            Returns:
              set[str] : A set of strings representing all the neighbors of the vertex
                         Returns an empty set if the given vertex doesn't exist
            
            Examples:
            >>> graph = {'A':['B'],'B':['A', 'E'],'E':['B']}
            >>> graph_helper = GraphHelper(graph)
            >>> graph_helper.get_neighbors('B') == {'A', 'E'}
            True

            >>> graph = {'A':['B'],'B':['A', 'E'],'E':['B']}
            >>> graph_helper = GraphHelper(graph)
            >>> graph_helper.get_neighbors('C') == set()
            True
        '''
        if not self.is_vertex(vertex):
           return set()
        
        vertex_neighbors = set()

        for neighbor in self.__adjacency_list[vertex]:
           vertex_neighbors.add(neighbor)

        return vertex_neighbors
    
    def get_isolated_nodes(self) -> set[str]:
        '''Accessor method for finding isolated nodes in a graph

            Returns:
              set[str] : A set of strings representing all nodes with no connections
            
            Examples:
            >>> graph = {'A':['B'],'B':['A', 'E'],'E':['B']}
            >>> graph_helper = GraphHelper(graph)
            >>> graph_helper.get_isolated_nodes() == set()
            True

            >>> graph = {'A':[],'B':['A', 'E'],'E':['B']}
            >>> graph_helper = GraphHelper(graph)
            >>> graph_helper.get_isolated_nodes() == {'A'}
            True
        '''
        
        lonely_nodes = set()

        for vertex in self.__adjacency_list:
          if not self.__adjacency_list[vertex]:
            lonely_nodes.add(vertex)

        return lonely_nodes

    def get_connected_nodes(self) -> set[str]:
        '''Accessor method for finding nodes that have at least one edge in a graph

            Returns:
              set[str] : A set of strings representing all nodes with at least one connection
            
            Examples:
            >>> graph = {'A':['B'],'B':['A', 'E'],'E':['B']}
            >>> graph_helper = GraphHelper(graph)
            >>> graph_helper.get_connected_nodes() == {'A', 'E', 'B'}
            True
        '''
        
        return self.__vertices - self.get_isolated_nodes()
    
if __name__ == "__main__":
    friends = {
            'Asa':['Haruki'], 
            'Bear':['Haruki'],
            'Cate':['Haruki'],
            'Dave':['Haruki'], 
            'Eve':['Haruki'], 
            'Finn':['Haruki'], 
            'Ginny':['Haruki'], 
            'Haruki':['Ivan', 'Ginny', 'Finn', 'Eve', 'Dave', 'Cate', 'Bear', 'Asa'], 
            'Ivan':['Haruki']
        }
    graph_helper = GraphHelper(friends)
    print(f"Edges: {graph_helper.edges}")
    print(f"Vertices: {graph_helper.vertices}")
    node='Haruki'
    print(f"Is {node} in the graph?: {graph_helper.is_vertex(node)}")
    print(f"{node} neighbors: {graph_helper.get_neighbors(node)}")
    node='Sasha'
    print(f"Is {node} in the graph?: {graph_helper.is_vertex(node)}")
    print(f"{node} neighbors: {graph_helper.get_neighbors(node)}")
    print(f"Isolated Nodes: {graph_helper.get_isolated_nodes()}")
    print(f"Connected Nodes: {graph_helper.get_connected_nodes()}")
