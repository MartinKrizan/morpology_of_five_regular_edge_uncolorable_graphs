# Report za letný semester

Git repozitár: https://github.com/MartinKrizan/morpology_of_five_regular_edge_uncolorable_graphs 

- vygenerované zoznami 5-regularnych nezafarbitelných 
    multigrafov s max 2 paralelnymi hranami po 12 vrcholov https://github.com/MartinKrizan/morpology_of_five_regular_edge_uncolorable_graphs/tree/main/data/multigraphs
- konštrukcia na transformaciu 5-regularneho multigrafu na jednoduchý graf https://github.com/MartinKrizan/morpology_of_five_regular_edge_uncolorable_graphs/blob/main/docs/research-notes.md
- identifikacia príčin nezafarbitelnosti grafov po 16 vrcholov
    - https://github.com/MartinKrizan/morpology_of_five_regular_edge_uncolorable_graphs/blob/main/docs/research-notes.md
    - https://github.com/MartinKrizan/morpology_of_five_regular_edge_uncolorable_graphs/blob/main/docs/research-notes.md#odd-component-cut-observation
- script na generovanie veľkých nezafarbitelných grafov 
  - https://github.com/MartinKrizan/morpology_of_five_regular_edge_uncolorable_graphs/blob/main/docs/research-notes.md#odd-component-cut-observation
  - https://github.com/MartinKrizan/morpology_of_five_regular_edge_uncolorable_graphs/blob/main/python/morphology_graphs/cli/generate_overfull.py
- program na vyhodnotenie zafarbitelnosti pomocou CP-SAT
  - CP-SAT model: https://github.com/MartinKrizan/morpology_of_five_regular_edge_uncolorable_graphs/blob/main/python/morphology_graphs/core/is_colorable.py
  - script: https://github.com/MartinKrizan/morpology_of_five_regular_edge_uncolorable_graphs/blob/main/python/morphology_graphs/cli/filter_uncol.py
- benchmark algoritmov na vyhodnotenie zafarbitelnosti
  - https://github.com/MartinKrizan/morpology_of_five_regular_edge_uncolorable_graphs/blob/main/python/benchmark/README.md
- testy pomocných funkcii na spracovanie grafov
- automatizovanie buildovania projektu 
  - https://github.com/MartinKrizan/morpology_of_five_regular_edge_uncolorable_graphs/blob/main/Dockerfile
  - https://github.com/MartinKrizan/morpology_of_five_regular_edge_uncolorable_graphs/blob/main/README.md#setup

