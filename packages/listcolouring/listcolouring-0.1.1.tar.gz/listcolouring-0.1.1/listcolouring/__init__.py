import random

import networkx as nx

def list_init(G, colours, k, seed):
    random.seed(seed)
    # assign a random subset of colours to the list of permissible colours for every edge
    for u, v, permissible in G.edges.data("permissible"):
        G[u][v]["permissible"] = random.sample(colours, 3)
        
    # initialise the colour of every edge to None
    for u, v, colour in G.edges.data("colour"):
        G[u][v]["colour"] = None

    return(G)

# colours_incident_with
def colours_incident_with(G, u):
    return(set([G[u][v]["colour"] for v in nx.neighbors(G, u)]))

# first_permissible_or_none
# given G, u and v this function returns the first element of A if A is not empty otherwise None
# A is P minus (X union Y)
# where X is the list of colours on edges incident with u
#       Y is the list of colours on edges incident with v
#       P is the list of permissible colours for edge uv
def first_permissible_or_none(G, u, v):
    X = colours_incident_with(G, u)
    Y = colours_incident_with(G, v)
    P = set(G[u][v]["permissible"])
    choices = P - X.union(Y)
    if(len(choices) > 0):
        choice = list(choices)[0]
    else:
        choice = None
    return(choice)

def greedy_list_edge_colouring(G):
    # assign the first permissible colour to every edge (or None if all permissible colours already used on incident edges)
    for u, v, colour in G.edges.data("colour"):
        G[u][v]["colour"] = first_permissible_or_none(G, u, v) # random.choice(colours)
    return(G)

def print_list_edge_colouring(G):
    # iterate through nodes and neighbours printing permissible lists and colours
    for n, nbrs in G.adj.items():
        for nbr, eattr in nbrs.items():
            perm = eattr['permissible']
            col = eattr['colour']
            print(f"({n}, {nbr}, {perm}, {col})")
        
