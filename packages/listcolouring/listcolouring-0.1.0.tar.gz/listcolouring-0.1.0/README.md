# list-colouring
List colouring in Python with NetworkX.

```
import networkx as nx
import matplotlib.pyplot as plt

import listcolouring
from listcolouring import list_init, greedy_list_edge_colouring, print_list_edge_colouring

G = nx.petersen_graph()

G = list_init(G, range(0, 10), 3, 0)
G = greedy_list_edge_colouring(G)
    
options = {'with_labels': True, 'node_color': "white"}
colors = nx.get_edge_attributes(G,'colour').values()
nx.draw_shell(G, nlist = [range(5, 10), range(5)], edge_color = colors, **options)

plt.savefig("img/petersen-shell.png", format = "PNG"
```