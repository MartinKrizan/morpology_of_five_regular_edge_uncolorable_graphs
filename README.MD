# Morphology 5-colorability experiments

## Uncolorable graphs on 16 vertices

All uncolorable 5-regular graphs on 16 vertices are listed in the file `results/uncol_16.g6`.

All of them have connectivity < 4. After splitting graph into two components by minimal cut one component is always uncolorable. Uncolorability of almost all of those component comes from number of vertices and edges in that component. That component is overfull.


TODO: pozriet tych 8 co nie su overful

Graph: O~zPw[@?O@_E?J?J?BW?n

Uncol part: G~zPw[

Critical part: F~zPw



This we can use to generate uncolorable graphs on larger number of vertices.

## Generating uncolorable graphs

We can generate 5 regular uncolorable graphs by generating overful graph with max degree lte 5 on odd number of vertices and then adding vertices and edges to make it 5-regular.

Script generate_overful.py generates overful graphs with max degree lte 5 on odd number of vertices.

TODO: script to add vertices and edges to make these graphs 5-regular


## 4-edge-connected uncolorable 5 regular graphs

There is one known 4-edge-conected uncolorable 5-regular graph. https://houseofgraphs.org/graphs/50543

TODO: It can be used to generate others with EC4

## Multigraph to simple 5-regular
TODO

