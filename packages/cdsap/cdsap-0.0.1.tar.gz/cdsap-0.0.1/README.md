# CDSAP 

**Common and Customized Data Structures in Python** 

This is only a helper library primarily designed for other related libraries and tools such as `sgep` and `mkmap`. 
If you intend to use this on your custom projects, you may do so at your own discretion. 

## Main Features

1. **Linked Lists**
    1. **Circular Singly Linked List (CSLL)** - Node Class Based
    2. **Circular Doubly Linked List (CDLL)** - Node Class Based

2. **Heaps** 
    1. **Keyed Binary Heap (KBH)** 
    2. **Keyed Min-Max Heap (KMMH)** 

3. **Queues**
    1. **Deque** - Doubled-Ended Queue using `CDLL`
    2. **Doubled-Ended Priority Queue** - `KMMH` Heap-Based 

4. **Balanced Binary Search Trees**
    1. **Threaded Order-statistic AVLT Tree** 
    2. **Threaded Order-statistic RBT Tree**  

5. **Graphs** 
    1. **Graph** - Directed and Undirected
    2. **Topological Sorting** 
    3. **Pathfinding** - (Dijkstra, A*, Bellman-Ford, Floyd-Warshall)

6. **Miscellaneous** 
    1. **Combinations and Permutations (with and without Repetitions)**
    2. **Segment Tree**


## Installation 
```
    pip install cdsap
```


## Archives Folder 
For other, unlisted and non-release implementations, please look at the `archives/`
folder. 

Such folder contains the initial/draft version of the algorithms before the major 
rewrite of this helper library. Such files are kept for future reference. 

Some algorithms that can be merged practically with algorithms have been
omitted such as *singly-linked list* and *doubly-linked list*. 

* **Stacks** 
    * Stacks are not included in the main release. 
    * They are straightforward to implement using Python lists without the unnecessary overhead.
* **Linked-Lists** 
    * Only the *circular singly-linked list* and *circular doubly-linked list* have been chosen
* **Queues** 
    * Both the *doubled-ended queue (deque)* and *priority queue* are part of the release.
* **Hash-Tables** 
    * The hash-tables here are slow and are not included in the main release.
    * The standard Python `dict()` might be preferred. 
    * In dealing with `floating point` as keys, the *balanced binary search trees* might be preferred
* **Heaps** 
    * Only the *Keyed-Binary Heap* and *Keyed Min-max Heap*
    * The *Keyed Fibonacci-Heap* and *Keyed K-ary Heap* are not included in the main release.
* **Balanced Binary Search Trees** 
    * Both the *Red-black Tree* and *AVLT tree* data structures are part of the release.
* **Graphs** 
    * The graph data structure and very common algorithms under this module/folder are included in the release.
    * Algorithms that are included pathfinding, mst, and topological sorting.
* **Misc** 
    * Segment-Trees and Combinatons & Permutations implementations are part of the release.

The omitted implementations that here are safekept but not included in the main release. 
They are also not included in future testing and updates. 

## Usage

[Documentation Coming Soon]