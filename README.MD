# Morphology of 5-regular uncolorable graphs

## Uncolorable graphs on 16 vertices

All uncolorable 5-regular graphs on 16 vertices are listed in the file `results/uncol_16.g6`.

All of them have connectivity < 4. After splitting graph into two components by minimal cut one component is always uncolorable. Uncolorability of almost all of those component comes from number of vertices and edges in that component. That component is overfull.

## Each 5-regular graph with EC < 5 that can be split into two components of odd size is uncolorable

Each 5-regular graph with edge connectivity less than 5 that can be split by a minimum cut into two components with an odd number of vertices is uncolorable.

### Proof:

Let G be a 5 regular graph with N number of vertices and let C be size of minimal cut. Let G1 and G2 be components of G after removing cut.

(BUNV) Number of edges E in G1 is (|G1|*5 - C)/2

After adding this to overful formula we get:

$$
|E| > \Delta(G) * \lfloor |V|/2 \rfloor
$$

$$
= 5 (\frac{|G1|}{2} - \frac{C}{10}) > 5 \frac{|G1| - 1}{2}
$$


$$
= \frac{C}{10} > \frac{1}{2}
$$

This holds for any C<5. From the properties of overfull graphs, we know that such a graph is uncolorable; therefore, G is also uncolorable.

---

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

