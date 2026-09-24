"""This puzzle is partially derived from Programming for the Puzzled by Srini Devadas"""
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

GraphHelper = None
if not GraphHelper:
    from GraphHelper import GraphHelper as GraphHelper 


def remove_problem_friendships(potential_invites: list[set], problem_friendships: set[tuple[str,str]]) -> list:
    '''Removes subsets from potential_invites that contain any pair of friends in a dislike relationship

       Args:
           potential_invites: a list of all possible friend combinations, each represented as a set of strings
           problem_friendships: set of tuples representing problematic friend pairings

       Returns:
           A list containing only sets of friend combinations that exclude dislike pairs
       
       Examples
        >>> potential_invites = [set(),{'Alice'},{'Bob'},{'Eve'},{'Eve', 'Alice'},{'Eve', 'Bob'}, {'Bob','Alice'},{'Bob','Eve', 'Alice'}]
        >>> problem_frienships = {('Bob', 'Eve'), ('Alice', 'Bob')}
        >>> remove_problem_friendships(potential_invites, problem_frienships) == [set(), {'Alice'}, {'Bob'}, {'Eve'}, {'Alice', 'Eve'}]
        True
    '''
    
    good_invites = []

    for invite_list in potential_invites:
        conflict = False
        for person1, person2 in problem_friendships:
            if person1 in invite_list and person2 in invite_list:
                conflict = True
                break

        if not conflict:
            good_invites.append(invite_list)

    return good_invites

def generate_all_subsets(friends: list) -> list[set]:
    '''Converts each number from 0 to 2^n - 1 into binary 
       Uses the binary representation to determine the combination of guests. 
       This produces every possible guest list (even the bad ones) for a given list of friends

       Args:
           friends: a list containing the names of all friends to consider
                    A list is used to preserve the position of each guest since a 1 in the binary representation
                    of a number means to include a guest in that list index

       Returns:
           A list of all possible subsets of friends to invite, represented as sets of strings
    '''
    n = len(friends)
    
    all_subsets = []

    for i in range(2**n):
        num = i  #num traces each digit in the binary version of i
        new_subset = []
        for j in range(n): # to_binary_division approach
            if num % 2 == 1: # 1 indicates the guest is included
                new_subset = [friends[n-1-j]] + new_subset
            num = num // 2
        all_subsets.append(set(new_subset))

    return all_subsets

def invite_to_dinner_exhaustive(graph_helper: GraphHelper)-> set[str]:
    '''Finds the invite combo with the maximum number of guests via the exhaustive approach:
            1. Generate every possible combination of guests
            2. Filter out the combinations that include problem friendships
            3. Find the combination which give you the maximum number of invites

       Args:
           graph_helper: A GraphHelper object with an adjacency list version of the friend graph
       
       Returns:
           A list of friends to invite to dinner which maximizes the number of friends on the list
        
       Examples
        >>> graph = {'Alice':['Bob'],'Bob':['Alice', 'Eve'],'Eve':['Bob']}
        >>> invite_to_dinner_exhaustive(GraphHelper(graph)) == {'Alice', 'Eve'}
        True
    '''
    #Generate all possible invite lists
    all_friends = graph_helper.vertices
    all_subsets = generate_all_subsets(list(all_friends))

    #Get rid of invite lists that include problem friendships
    problem_friendships = graph_helper.edges
    good_invites = remove_problem_friendships(all_subsets, problem_friendships)

    #Pick the invite list which maximizes the number of invites
    invite_list = []
    for i in good_invites:
        if len(i) > len(invite_list):
            invite_list = i

    return invite_list

def invite_to_dinner_better(graph_helper: GraphHelper) -> set[str]:
    '''Finds the invite combo with the maximum number of guests
       
       Args:
           graph_helper: A GraphHelper object with an adjacency list version of the friend graph
       
       Returns:
           A list of friends to invite to dinner which maximizes the number of friends on the list
       
       Examples
        >>> graph = {'Alice':['Bob'],'Bob':['Alice', 'Eve'],'Eve':['Bob']}
        >>> invite_to_dinner_better(GraphHelper(graph)) == {'Alice', 'Eve'}
        True
    '''
    #friends with no problem friendships will always be invited
    definitely_in = graph_helper.get_isolated_nodes()

    #generate all invites with a reduced input: only problematic friends
    problem_friends = graph_helper.get_connected_nodes()
    fewer_friend_subsets = generate_all_subsets(list(problem_friends))

    #Get rid of invite lists that include problem friendships
    #Not all problem friends have problems with everybody
    problem_friendships = graph_helper.edges
    good_invites = remove_problem_friendships(fewer_friend_subsets, problem_friendships)
   
    #find the subset which maximizes number of invites
    invite_list = []
    for i in good_invites:
        if len(i) > len(invite_list):
            invite_list = i

    return set(invite_list).union(definitely_in)

def invite_to_dinner_optimized(graph_helper: GraphHelper) -> set[str]:
    '''Finds the combination with the maximum number of guests without storing all subset combinations. 
       Functions the same as invite_to_dinner_better. However, your solution should not invoke generate_all_subsets 
       or remove_problem_friendships. Instead, you should combine theses implementations with finding the maximum 
       number of guests.
       
       Args:
           graph_helper: A GraphHelper object with an adjacency list version of the friend graph

       Returns:
           A set of friends to invite to dinner which maximizes the number of friends on the list
       
       Examples
        >>> graph = {'Alice':['Bob'],'Bob':['Alice', 'Eve'],'Eve':['Bob']}
        >>> invite_to_dinner_optimized(GraphHelper(graph)) == {'Alice', 'Eve'}
        True
    '''
    
    definitely_in = graph_helper.get_isolated_nodes()

    problem_friends = list(graph_helper.get_connected_nodes())
    problem_friendships = graph_helper.edges
    number_of_problem_friends = len(problem_friends)

    longest_invite_list = set()

    potential_decision_points = [(0, set())]

    while potential_decision_points:
        index, current_list = potential_decision_points.pop()

        if (len(current_list) + (number_of_problem_friends - index)) <= len(longest_invite_list):
            continue

        if index == number_of_problem_friends and (len(current_list) > len(longest_invite_list)):
            longest_invite_list = set(current_list)
            continue

        potential_decision_points.append((index + 1, set(current_list)))

        for person1, person2 in problem_friendships:
            if not any((person1 == problem_friends[index] and person2 in current_list) or (person2 == problem_friends[index] and person1 in current_list) for person1, person2 in problem_friendships):
                included = set(current_list)
                included.add(problem_friends[index])
                potential_decision_points.append((index + 1, included))

    return longest_invite_list.union(definitely_in)
               
if __name__ == "__main__":
    
    friends = {
        'Alice':['Bob'],
        'Bob':['Alice', 'Eve'],
        'Cleo':[],
        'Don':[],
        'Eve':['Bob']
    }
    graph_helper = GraphHelper(friends)
    print(invite_to_dinner_exhaustive(graph_helper))
    print(invite_to_dinner_better(graph_helper))
    print(invite_to_dinner_optimized(graph_helper))
    
    friends_2 = {
        'Alice':['Bob'],
        'Bob':['Alice', 'Eve'],
        'Eve':['Bob']
    }
    graph_helper = GraphHelper(friends_2)
    print(invite_to_dinner_exhaustive(graph_helper))
    print(invite_to_dinner_better(graph_helper))
    print(invite_to_dinner_optimized(graph_helper))

    friends_3 ={
            "F": ['A','E'],
            "E": ['A','F','C'],
            "D": ['B','C'],
            "C": ['D','E'],
            "B": ["A", 'D'],
            "A": ["B","E", "F"]
        }
    graph_helper = GraphHelper(friends_3)
    print(invite_to_dinner_exhaustive(graph_helper))
    print(invite_to_dinner_better(graph_helper))
    print(invite_to_dinner_optimized(graph_helper))
