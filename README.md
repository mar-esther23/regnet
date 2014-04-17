regnet
======

Python library for analyzing dynamic boolean networks.

A dynamical network is a collection of connected elements whose values can change in time. 
In a regulatory network the nodes can represent genes, proteins, processes, etc. The state of the node can represent the presence or absence of the element (boolean), the concentration (discrete, continuous). The state of a node depends on its regulators, and can be represented with a function. A regulatory network is directed and can have selfloops.
