# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state
=
        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    "*** YOUR CODE HERE ***"
    from util import Stack

    state = problem.getStartState()
    visited = []
    path_dict = {}    #path dictionary {next : last} i.e. {(4, 5) : (5, 5)}
    act_dict = {}   #action dictionary {node : action} i.e. {(4, 5) : 'West'}
    actions = []
    stack = Stack()
    stack.push(state)

    while not stack.isEmpty():
        state = stack.pop()
        if problem.isGoalState(state):
            break
        if state not in visited:
            visited.append(state)
            for succ in problem.getSuccessors(state):
                if succ[0] not in visited:
                    stack.push(succ[0])
                    path_dict[succ[0]] = state
                    act_dict[succ[0]] = succ[1]

    while state in path_dict:
        actions.append(act_dict[state])
        state = path_dict[state]
    actions.reverse()

    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    state = problem.getStartState()
    visited = [state]
    path_dict = {}    #path dictionary {next : last} i.e. {(4, 5) : (5, 5)}
    act_dict = {}   #action dictionary {node : action} i.e. {(4, 5) : 'West'}
    actions = []
    queue = Queue()
    queue.push(state)

    while not queue.isEmpty():
        state = queue.pop()
        if problem.isGoalState(state):
            break
        for succ in problem.getSuccessors(state):
            if succ[0] not in visited:
                visited.append(succ[0])
                queue.push(succ[0])
                path_dict[succ[0]] = state
                act_dict[succ[0]] = succ[1]
    print path_dict
    print state
    while state in path_dict:
        actions.append(act_dict[state])
        state = path_dict[state]
    actions.reverse()
    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    state = problem.getStartState()
    visited = []
    pq = PriorityQueue()
    actions = []
    pq.push((state, actions), 0)
    while not pq.isEmpty():
        state, actions = pq.pop()
        if problem.isGoalState(state):
            break
        if state not in visited:
            for succ in problem.getSuccessors(state):
                if succ[0] not in visited:
                    cost = problem.getCostOfActions(actions + [succ[1]])
                    pq.push((succ[0], actions + [succ[1]]), cost)
        visited.append(state)
    return actions

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    state = problem.getStartState()
    visited = []
    pq = PriorityQueue()
    actions = []
    pq.push((state, actions), heuristic(state, problem))
    while not pq.isEmpty():
        state, actions = pq.pop()
        if problem.isGoalState(state):
            break
        if state not in visited:
            for succ in problem.getSuccessors(state):
                if succ[0] not in visited:
                    cost = problem.getCostOfActions(actions + [succ[1]]) + heuristic(succ[0], problem)
                    pq.push((succ[0], actions + [succ[1]]), cost)
        visited.append(state)
    return actions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


def greedySearch(problem, heuristic=nullHeuristic):
    path = []
    path_dict = {}
    act_dict = {}
    pq = util.PriorityQueue()

    startstate = problem.getStartState()
    visited = [startstate]
    pq.push(startstate, heuristic(startstate))

    while not pq.isEmpty():

        state = pq.pop()
        if problem.isGoalState(state):
            break

        for succ in problem.getSuccessors(state):
            if succ[0] not in visited:
                priority = heuristic(succ[0])
                pq.push(succ[0], priority)
                visited.append(succ[0])
                path_dict[succ[0]] = state
                act_dict[succ[0]] = succ[1]

    while state in path_dict:
        path.append(act_dict[state])
        state = path_dict[state]
    path.reverse()

    return path