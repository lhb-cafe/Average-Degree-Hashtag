This is the coding challenge for Insight Data Engineering Fellows Program
https://github.com/InsightDataScience/coding-challenge


The objective of this project is to compute the the average degree of 
the graph formed by hashtags that are mentioned together in tweets.


My code consists of two main definitions:
1. The class of Hashtag_graph
2. The main method for solving the problem, Solution()





*********************************************************
************ The Hashtag_graph **************************
*********************************************************

I first defined a class for edges, which is basically an
unordered tuple of strings. Since it is not mutable, I also 
defined the __eq__ and __hash__ method for the Edge class, 
so that I can use a hash table, or a dictionary, to store 
the edges.


The graph class consists of two parts: 
a. A dictionary for nodes, where the key is the name of the node, 
   i.e., the hashtags, and the value is the number of instances 
   this hashtags has been inserted into the graph.
b. A dictionary for edges, where the key is the Edge class I 
   defined previously, i.e., the hashtags which appears in the 
   same tweets together. And the value is the number of instances 
   this pair of hashtages has been inserted into the graph.


The graph class consists of the following methods:
a. __init__() creates an empty graph
b. increase_node(node) inserts a new node into the graph, if the 
   node already exists, it will increases its value in the dictionary
c. increase_edge(na, nb) inserts an edge consisting of na and nb as
   nodes into the graph. If this edge already exists, it will increase 
   its value in the dictionary.
d. decrease_node(node) removes one instance of a node from the graph, 
   if the count of this node becomes zero, it will also remove this 
   node from the dictionary as a key.
e. decrease_edge(na, nb) removes one instance of the edge consisting 
   of na and nb. If the count of this edge becomes zero, it will also 
   remove this edge from the dictionary as a key.
f. avg_degree() evaluates and returns the avg degree of nodes.
   Even though each node or edge can have multiple instances in the 
   graph, they are only counted once if they exist at all.







*********************************************************
******************* Solution() **************************
*********************************************************

Procedure for solving the problem:


Use the imported JSON library, decode the tweets.txt file line 
by line. For each line, only extract the 'created_at' and 'hashtags' 
fields.


For time comparison:
Use the imported datetime object, translate the timestamps from 
twitter API into datetime objects, so we can compare them into 
difference of seconds.


For hashtag processing:
The array of decoded 'hashtags' consists of the hashtags and the 
indices. We only need the hashtags and we want each of them to be 
unique in a single tweet. So we put them into a list of unique 
hashtags.


The 60 second window:
The process keeps a window, which is basically is a 'queue' of 
each tweet (consisting of hashtags and time offsets from with 
respect to the newest tweet). But it is also ordered by the offset, 
so each time we enqueue a newer tweet and update the offsets by 
time difference between the new tweet and the previous new tweet, 
we only need to check the front of the queue to see if there is 
any tweet falls outside of the 60 second range.
For the tweets falling outside of the range, we remove the hashtags 
and the hashtag edges contributed by them to the graph, and then pop 
them out of the window.


Writing to the output.txt file
For each line from tweets.txt we process, following the above procedure, 
we evaluate the avg degree of the graph and write it to the output.txt 
file line by line, with 2 decimal point position as required by the format.






*********************************************************
******************* Efficiency **************************
*********************************************************

I chose to use Python because it is a very popular language chosen by 
data scientists. It also has many well developed packages, for example, 
the json package or the datetime package. More importantly, Python 
is known for its excellent portability between different platforms since 
it generates bytecodes first.


This program involves inserting, searching, and deleting nodes and 
edges to and from the graph all the time. So it is very important that 
we use an efficient data structure for these operations. The best choice 
is through using a hash table, or in Python, a dictionary.


The benefit for using a sorted list to implement the window is that we 
can save a lot of time checking all tweets in the window for time range. 
We only need to check the front of the 'queue' for each newer tweet 
we enqueue. Making the checking time complexity from O(n) to O(1), where 
n is the number of tweets in the window.
One slight drawback for using sorted list for the window is enqueueing a 
new tweet can be slightly more complicated if the new tweet comes out of 
order, i.e., it should be placed before the end of the queue. But this 
situation is extremely rare. And even if it happens, it won't be too much 
older than the newest tweet, so its proper position is easy to find.

