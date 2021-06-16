# Algorithms and data structures

## Data structures

* Array
* Linked list
* Stack
* Queue (single or double-sided, FIFO or LIFO; using linked list)
* Priority queue (using heap tree)
* Hash map / hash table
* Hash set
* Associative array / dictionary (usually done with Hash map, otherwise with binary search tree)
* Hash map collision ???
* Hash set (built on top of hash map)
* Graph (nodes/vertices + edges)
    * Undirected graph
    * Directed graph
    * Positive weighted
    * Negative weighted
    * Cycle
    * How to represent graph (object + pointers; matrix; adjacency list; hash table)
    * Complete binary graph (k, 2k + 1, 2k + 2)
* Max / min binary heap tree
* Memory heap
* Heap queue algorithm ???
* Tree (graph with the root node, each node has subtree)
    * Binary Search Tree
    * Trie ???
    * AVL tree
    * Red-black tree
* Bag (unordered: add, size, iterate; using list or defaultdict)
* Forward index: document -> list of words
* Inverted index: word -> list of documents

### Applications of data structures


* Parentheses balancing -> stack
* Recursion -> stack
* Depth-first -> recursion
* Breadth-first -> double-side queue

## Sort algorithms

* Heap sort (unstable)
* Quicksort (unstable)
* Merge sort (stable)
* Bubble sort (stable) ???
* Bucket sort ???
* Radix sort ???
* Insertion sort (stable) ~~~
* Timsort (Python) ???

### Applications of sort algorithms

* Nearly sorted (K sorted) array A: O(n * log k)
    * min binary heap for A\[:k] element
    * for i in 0...len(A)-k:
        * insert A\[k + i] into heap
        * pop min from heap into A\[i]
* Almost sorted array -> use quick sort with pivot = last or first element
* Insertion sort for small arrays (<= 10 elements)
* We already know the range of target values -> radix sort

## Type of algorithms

* Bottom-up algorithms ???
* Top-down algorithms ???


* Brute force ???
* Divide-and-conquer ???
* Recursion
* Possible fix for recursion:
    * Loops
    * Memoization
* Greedy ???
* NP-complete problem ???
* Dynamic programming/memoization ???

## Search, Traversal and pathfinder

* Binary search (in an array)
* Binary search tree (in tree)
* Minimum spanning tree ???
* Red-black tree ???
* AVL tree ???
* Depth-first
* Breadth-first

* Find connection / distance between graphs
    * Breadth-first from both directions
    * Dijkstra
    * A* ???
    * For negative graphs ???
    * For cycle graphs ???
* Graph search ???
* Graph cycle detection ???
* Graph connectivity detection ???
* Graph topology sort ???

## Complexity

### Runtime complexity + space complexity

## Bit operations and implementations


## Distributed

* Distributed hash table system ???
* For loop problems ???
* Index ???
* reverse link-list ???

## Python

* What is GIL? What is it for? Why cannot get rid of it? ???
* What are co-routines in Python ???
* What is the event loop in Python? What a possible executors? Multi-cores? ???
    * See `loop.run_in_executor` + `concurrent.futures.ProcessPoolExecutor`
* How is dict implemented in Python ???
* Python hash function ???
* Python hash collision situation ???
* What sorting does `[].sort` use? (Timsort)
* How is order preserved in dict in Python ???
* Is order preserved for set in Python ???
* How is set implemented in Python ???
* How is list implemented in Python ???
* How is tuple implemented in Python ???
* What exactly is stored in execution stack ???
* What is the depth of stack in Python (stack overflow) ???
* Stackless Python ???
* Stack-less model of execution. Actors?  ???
* Python tail recursion optimization ???

## PostgreSQL

* B-tree index ???
* Hash index ???
* GiST index ???
* SP-GiST index ???
* GIN index ???
* BRIN index ???

## Google Style Guides for Python

https://google.github.io/styleguide/pyguide.html
