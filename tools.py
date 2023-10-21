# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:39:29 2020

@author: Zacharias Hultman
"""

import math
import numpy as np
import pandas as pd
from pandas import ExcelWriter
import networkx as nx
   

from collections import deque
from heapq import heappush, heappop
from itertools import count
import networkx as nx
from networkx.utils import generate_unique_node


def find_cheapest_edge(edge_data):
    # finds the cheapest edge
    # in: 'networkx.classes.coreviews.AtlasView'
    #out: string
    cheapest_stock = math.inf
    for k in edge_data:
        if edge_data[k]['weight'] <= cheapest_stock:
            ultimate_stock = edge_data[k]['key']
    return ultimate_stock

def gen_data_to_excell(stocks, excell_data,max_dev, file_loc):
    writer = ExcelWriter(file_loc,engine='xlsxwriter')
    for stock in excell_data.index:
        amount=len(list(filter(lambda i: i['name'] == excell_data.iloc[stock, 0] , stocks)))
        df1 = pd.DataFrame({excell_data.iloc[stock, 0]})
        df2 = pd.DataFrame({amount})
        df1.to_excel(writer, 'Result', startcol=0,startrow=stock,header=None, index=False)
        df2.to_excel(writer, 'Result', startcol=1,startrow=stock,header=None, index=False)
    df3 = pd.DataFrame({max_dev})
    df3.to_excel(writer, 'Result', startcol=4,startrow=stock+1,header=['Yearly devidend'], index=False)
    writer.save()
    
    
def del_first_occurence(stock_list,index):
    stock_del=[]
    flagsator=False
    for i in stock_list:
        if i['index']==index and flagsator==False:
            flagsator=True
            continue
        stock_del.append(i)
    return stock_del   

def cheapest_combo(max_dev_hist,stock_rates):
    cheapest_magic_path_cost=math.inf
    for combo in max_dev_hist:
        combo_cost=0
        for k in combo:
            combo_cost=combo_cost+stock_rates.iloc[k.get('index')].to_numpy()
        if combo_cost<=cheapest_magic_path_cost:
            cheapest_magic_path_cost=combo_cost
            cheapest_magic_path=combo
    return cheapest_magic_path,cheapest_magic_path_cost

    
def _weight_function(G, weight):
    """Returns a function that returns the weight of an edge.

    The returned function is specifically suitable for input to
    functions :func:`_dijkstra` and :func:`_bellman_ford_relaxation`.

    Parameters
    ----------
    G : NetworkX graph.

    weight : string or function
        If it is callable, `weight` itself is returned. If it is a string,
        it is assumed to be the name of the edge attribute that represents
        the weight of an edge. In that case, a function is returned that
        gets the edge weight according to the specified edge attribute.

    Returns
    -------
    function
        This function returns a callable that accepts exactly three inputs:
        a node, an node adjacent to the first one, and the edge attribute
        dictionary for the eedge joining those nodes. That function returns
        a number representing the weight of an edge.

    If `G` is a multigraph, and `weight` is not callable, the
    minimum edge weight over all parallel edges is returned. If any edge
    does not have an attribute with key `weight`, it is assumed to
    have weight one.

    """
    if callable(weight):
        return weight
    # If the weight keyword argument is not callable, we assume it is a
    # string representing the edge attribute containing the weight of
    # the edge.
    if G.is_multigraph():
        return lambda u, v, d: min(attr.get(weight, 1) for attr in d.values())
    return lambda u, v, data: data.get(weight, 1)

def single_source_dijkstra(G, source, target=None, cutoff=None,
                           weight='weight',special=False,magic_number=0):
    """Find shortest weighted paths and lengths from a source node.

    Compute the shortest path length between source and all other
    reachable nodes for a weighted graph.

    Uses Dijkstra's algorithm to compute shortest paths and lengths
    between a source and all other reachable nodes in a weighted graph.

    Parameters
    ----------
    G : NetworkX graph

    source : node label
       Starting node for path

    target : node label, optional
       Ending node for path

    cutoff : integer or float, optional
       Depth to stop the search. Only return paths with length <= cutoff.

    weight : string or function
       If this is a string, then edge weights will be accessed via the
       edge attribute with this key (that is, the weight of the edge
       joining `u` to `v` will be ``G.edges[u, v][weight]``). If no
       such edge attribute exists, the weight of the edge is assumed to
       be one.

       If this is a function, the weight of an edge is the value
       returned by the function. The function must accept exactly three
       positional arguments: the two endpoints of an edge and the
       dictionary of edge attributes for that edge. The function must
       return a number.

    Returns
    -------
    distance, path : pair of dictionaries, or numeric and list.
       If target is None, paths and lengths to all nodes are computed.
       The return value is a tuple of two dictionaries keyed by target nodes.
       The first dictionary stores distance to each target node.
       The second stores the path to each target node.
       If target is not None, returns a tuple (distance, path), where
       distance is the distance from source to target and path is a list
       representing the path from source to target.

    Raises
    ------
    NodeNotFound
        If `source` is not in `G`.
    Notes
    -----
    Edge weight attributes must be numerical.
    Distances are calculated as sums of weighted edges traversed.

    The weight function can be used to hide edges by returning None.
    So ``weight = lambda u, v, d: 1 if d['color']=="red" else None``
    will find the shortest red path.

    Based on the Python cookbook recipe (119466) at
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/119466

    This algorithm is not guaranteed to work if edge weights
    are negative or are floating point numbers
    (overflows and roundoff errors can cause problems).


    """
    return multi_source_dijkstra(G, {source}, cutoff=cutoff, target=target,
                                 weight=weight,special=special,magic_number=magic_number)
    
def multi_source_dijkstra(G, sources, target=None, cutoff=None,
                          weight='weight',special=False,magic_number=0):
    """Find shortest weighted paths and lengths from a given set of
    source nodes.

    Uses Dijkstra's algorithm to compute the shortest paths and lengths
    between one of the source nodes and the given `target`, or all other
    reachable nodes if not specified, for a weighted graph.

    Parameters
    ----------
    G : NetworkX graph

    sources : non-empty set of nodes
        Starting nodes for paths. If this is just a set containing a
        single node, then all paths computed by this function will start
        from that node. If there are two or more nodes in the set, the
        computed paths may begin from any one of the start nodes.

    target : node label, optional
       Ending node for path

    cutoff : integer or float, optional
       Depth to stop the search. Only return paths with length <= cutoff.

    weight : string or function
       If this is a string, then edge weights will be accessed via the
       edge attribute with this key (that is, the weight of the edge
       joining `u` to `v` will be ``G.edges[u, v][weight]``). If no
       such edge attribute exists, the weight of the edge is assumed to
       be one.

       If this is a function, the weight of an edge is the value
       returned by the function. The function must accept exactly three
       positional arguments: the two endpoints of an edge and the
       dictionary of edge attributes for that edge. The function must
       return a number.

    Returns
    -------
    distance, path : pair of dictionaries, or numeric and list
       If target is None, returns a tuple of two dictionaries keyed by node.
       The first dictionary stores distance from one of the source nodes.
       The second stores the path from one of the sources to that node.
       If target is not None, returns a tuple of (distance, path) where
       distance is the distance from source to target and path is a list
       representing the path from source to target.

    Notes
    -----
    Edge weight attributes must be numerical.
    Distances are calculated as sums of weighted edges traversed.

    The weight function can be used to hide edges by returning None.
    So ``weight = lambda u, v, d: 1 if d['color']=="red" else None``
    will find the shortest red path.

    Based on the Python cookbook recipe (119466) at
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/119466

    This algorithm is not guaranteed to work if edge weights
    are negative or are floating point numbers
    (overflows and roundoff errors can cause problems).

    Raises
    ------
    ValueError
        If `sources` is empty.
    NodeNotFound
        If any of `sources` is not in `G`.

    See Also
    --------
    multi_source_dijkstra_path()
    multi_source_dijkstra_path_length()

    """
    if not sources:
        raise ValueError('sources must not be empty')
    if target in sources:
        return (0, [target])
    weight = _weight_function(G, weight)
    paths = {source: [source] for source in sources}  # dictionary of paths
   
    dist = _dijkstra_multisource(G, sources, weight, paths=paths,
                                 cutoff=cutoff, target=target,special=special,magic_number=magic_number)
    if target is None:
        return (dist, paths)
    try:
        return (dist[target], paths[target])
    except KeyError:
#        raise ("No path to {}.".format(target))
        print('except')
        
        
def _dijkstra_multisource(G, sources, weight, pred=None, paths=None,
                          cutoff=None, target=None,special=False,magic_number=0):
    """Uses Dijkstra's algorithm to find shortest weighted paths

    Parameters
    ----------
    G : NetworkX graph

    sources : non-empty iterable of nodes
        Starting nodes for paths. If this is just an iterable containing
        a single node, then all paths computed by this function will
        start from that node. If there are two or more nodes in this
        iterable, the computed paths may begin from any one of the start
        nodes.

    weight: function
        Function with (u, v, data) input that returns that edges weight

    pred: dict of lists, optional(default=None)
        dict to store a list of predecessors keyed by that node
        If None, predecessors are not stored.

    paths: dict, optional (default=None)
        dict to store the path list from source to each node, keyed by node.
        If None, paths are not stored.

    target : node label, optional
        Ending node for path. Search is halted when target is found.

    cutoff : integer or float, optional
        Depth to stop the search. Only return paths with length <= cutoff.

    Returns
    -------
    distance : dictionary
        A mapping from node to shortest distance to that node from one
        of the source nodes.

    Raises
    ------
    NodeNotFound
        If any of `sources` is not in `G`.

    Notes
    -----
    The optional predecessor and path dictionaries can be accessed by
    the caller through the original pred and paths objects passed
    as arguments. No need to explicitly return pred or paths.

    """
    G_succ = G._succ if G.is_directed() else G._adj
    
    
    
    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    seen = {}
    # fringe is heapq with 3-tuples (distance,c,node)
    # use the count c to avoid comparing nodes (may not be able to)
    c = count()
    fringe = []
    
    for source in sources:
        if source not in G:
            raise nx.NodeNotFound("Source {} not in G".format(source))
        seen[source] = 0
        push(fringe, (0, next(c), source))
        prev_v=0
        cost_hist=[]
        
    while fringe:
        (d, _, v) = pop(fringe)
#
#        print('d',d)
#        print('v',v)
#        print('prev_v',prev_v)
        if v in dist:
            continue  # already searched this node.
        dist[v] = d           
        if v == target:
            break
        
        for u, e in G_succ[v].items():
#            print('u',u)
#            gåt nog att ändra e (egdes) till OK_e (okey edges)
#            frågan är väl hur man ska kunna nollställa dessa okey edges. och var ska man lägga till att en edge har användts?
#            e är en dict
#            funkar inte än
#            print('e',e)
            e_backup=e
            counter=0
            flag=False
            while True:
                try:    
                    cost = weight(v, u, e)
                except:
#                    counter=counter+1
#                    e=e_back_up
#                    magic_number=magic_number+1
#                    print(magic_number)
                    flag=True 
                    break
                if cost_hist.count(cost)>=magic_number:
#                    for key in e.items():
#                        print('key',key[1].get('weight'))
                    print('cost',cost)
#                    print('u',u)
#                    print('e before',e)
                    e=[i for i in e.items() if not (i[1].get('weight')==cost)]
                    print('e',e)
#                    print('e_tmp',e_tmp) 
                    print('remove')
                else:
                     cost_hist.append(cost)   
                     print('append')
                     break

                
#            if counter>0:
#                magic_number=magic_number-counter
            if flag==True:
                flag=False
                continue 
                
            if cost is None:
                continue
            vu_dist = dist[v] + cost
            if cutoff is not None:
                if vu_dist > cutoff:
                    continue
            if u in dist:
                if vu_dist < dist[u]:
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')
            elif (u not in seen or vu_dist < seen[u]):
                seen[u] = vu_dist
                push(fringe, (vu_dist, next(c), u))
                if paths is not None:
                    paths[u] = paths[v] + [u]
                if pred is not None:
                    pred[u] = [v]
            elif vu_dist == seen[u]:
                if pred is not None:
                    pred[u].append(v)
        prev_v=v

    # The optional predecessor and path dictionaries can be accessed
    # by the caller via the pred and paths objects passed as arguments.
#    print('dist',dist)
    return dist