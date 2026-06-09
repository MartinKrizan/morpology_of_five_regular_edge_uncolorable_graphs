# Lists of 5-regular multigraphs

- multigrahs were genearated using nauty-geng and nauty-multig similarly to script here https://github.com/ba-graph-research/ba-graph/blob/master/tools/generation/multigraphs/generateMultigraphs_d.sh 

- to reduce amount of graphs, lists contains only those with maximum edge multiplicity 2 - higher multiplicity implies that graph contains edge cut of size <= 4 

- multigraphs are in nauty simple text output format

- colorability was checked with this [script](../../python/morphology_graphs/cli/filter_uncol.py)

## Lists 

- [uncol_12_m2_all_small.txt](uncol_12_m2_all_small.txt) - List of all edge uncolorable multigraphs on 12 vertices
  - [high_conn_12_uncol_m.txt](high_conn_12_uncol_m.txt) - Those of them which have edge connectivity > 3, converted to simple graphs using [script](../../python/morphology_graphs/cli/filter_low_con.py) (graph6 representation)
- [uncol_10_m2_all_small.txt](uncol_10_m2_all_small.txt) - List of all edge uncolorable multigraphs on 10 vertices
- [uncol_8_m2_all_small.txt](uncol_8_m2_all_small.txt) - List of all edge uncolorable multigraphs on 8 vertices
