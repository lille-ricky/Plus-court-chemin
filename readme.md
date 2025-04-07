# Plus Court Chemin , a report by Enrik Pashaj



## Structure

### Key Files
- **dijkstra_minheap.py**: Dijkstra's algorithm implementation using a binary heap
- **dijkstra_fibo.py**: Dijkstra's algorithm implementation using a Fibonacci heap
- **bellman-ford.py**: Bellman-Ford algorithm Implementation
- **DataLoader.py**:  Loads and transforms GTFS data for Dijkstra algorithm tests
- **DataLoaderBellman-Ford.py**: Utility for loading data for Bellman-Ford algorithm tests

### Datasets
- The project uses GTFS data from Lille's public transportation network (Ilévia)
- Primary data source: `stop_times.txt` - bus stop times


## Generating the grpahs
Head to the ressources folder
###  Dijkstra's Algorithm graph
run the ```Dataloader.py``` script to generate the graphs.

###  Bellman-Ford Algorithm graph
run the ```DataloaderBellman-Ford.py``` script to generate the graphs.


## Visualizations and Analysis

The project includes performance analyses visualized through:
- Comparison charts of execution times
- Graphical representation of algorithm efficiency based on graph density
- Theoretical vs. empirical performance comparisons

## Conclusion and Future Work

The project demonstrates that while theoretical complexity analysis provides valuable insights, practical implementation details (such as memory access patterns and constant factors) significantly impact real-world performance. For most practical applications with moderate-sized graphs, Dijkstra's algorithm with a Binary Heap implementation offers the best balance of simplicity and performance.

Areas for future exploration include:
- Parallelization of shortest path algorithms
- Application to dynamic graphs where edge weights change over time
- Integration with real-time transportation systems

## References
The project relies on fundamental algorithms literature including:
- Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs"
- Bellman, R. (1958). "On a routing problem"
- Fredman, M. L., & Tarjan, R. E. (1987). "Fibonacci heaps and their uses in improved network optimization algorithms"
- Cormen, T. H., et al. (2022). "Introduction to Algorithms" (4th ed.)

For more information head for the ```Rapport_PCC_Pashaj_Enrik.pdf``` file in main branch. 


## Github Repository containing my work 
[https://github.com/lille-ricky/Plus-court-chemin]


Licence 2 Informatique 
Faculte des Sciences - Jean Perrin 
![universite_artois](Université_d'Artois_(logo).svg.png)