import time
from datetime import timedelta, datetime
import json
from os import path

##################################################
# the graph is a hash table of edges, each edge  #
# in the hash table has a count, and it will be  #
# deleted when the count becomes zero            #
##################################################
class Hashtag_graph:
        # the edge is an unordered tuple
        class Edge():
                def __init__(self, a, b):
                        self.a = a
                        self.b = b
                def __eq__(self, other):
                        if self.a == other.a and self.b == other.b:
                                return True
                        elif self.a == other.b and self.a == other.b:
                                return True
                        else:
                                return False
                def __ne__(self, other):
                        return not self.__eq__(other)
                def __hash__(self):
                        return hash(self.a) ^ hash(self.b)
                        
        def __init__(self):
                self.dict_edge = {}
                self.dict_node = {}
                self.num_nodes = 0
                self.total_degree = 0 # 2 * num_edges
        
        # insert a node into the dictionary if not existed
        # increment the count of the node if already existed
        def increase_node(self, node):
                if node in self.dict_node:
                        self.dict_node[node] += 1
                else:
                        self.dict_node[node] = 1
                        self.num_nodes +=1
                        
        # insert an edge into the dictionary if not existed
        # increment the count of the edge if already existed
        def increase_edge(self, a, b):                        
                new_edge = self.Edge(a, b)
                if new_edge in self.dict_edge:
                        self.dict_edge[new_edge] += 1
                else:
                        self.dict_edge[new_edge] = 1
                        self.total_degree += 2

        # decrement the count of the node in the dictionary
        # remove the node from the dictionary if count becomes 0        
        def decrease_node(self, node):
                self.dict_node[node] -= 1
                # remove the node if count becomes zero
                if self.dict_node[node] == 0:
                        self.dict_node.pop(node, None);
                        self.num_nodes -= 1
                        
        # decrement the count of the edge in the dictionary
        # remove the edge from the dictionary if count becomes 0
        def decrease_edge(self, a, b):
                delete_edge = self.Edge(a,b)
                self.dict_edge[delete_edge] -= 1
                # remove the edge if count becomes zero
                if self.dict_edge[delete_edge] == 0:
                        self.dict_edge.pop(delete_edge, None);
                        self.total_degree -= 2
                        
        # return the avg degree of the graph
        # if the graph is empty, return 0
        def avg_degree(self):
                if self.num_nodes > 0:
                        return float(self.total_degree)/self.num_nodes
                else:
                        return 0


#########################################################
###################### Solution! ########################
#########################################################                
def Solution():
        script_dir = path.dirname(__file__)
        input_path = path.join(script_dir, "../tweet_input/tweets.txt")
        output_path = path.join(script_dir, "../tweet_output/output.txt")

        # the date twitter was founded, no tweet can be older than it
        time_newest = datetime.strptime("2006-03-21 00:00:00", "%Y-%m-%d %H:%M:%S")
        
        # the list of tweets (of hashtags and time offset w.r.t. time_newest)
        # it should be sorted with respect to the time offset
        # it is basically an ordered queue
        # an example of the tuple can be [["tag1", "tag2", "tag3"], 37)]
        window = []
        window_size = 0
        
        # the hashtag graph object
        hashtag_graph = Hashtag_graph()
        
        #########################################################
        # compare_time takes a new datetime object as argument  #
        # it replaces time_newest by this new time if it is     #
        # newer, and returns the difference between old and new #
        #########################################################
        def compare_time(time_new):
                nonlocal time_newest
                sec_diff = (time_newest - time_new).total_seconds()
                if sec_diff < 0:
                        time_newest = time_new
                return sec_diff
                
        #########################################################
        # given a list of hashtags, insert into the graph these #
        # nodes and the edges they form                         #
        #########################################################
        def insert_to_graph(hashtags_list):
                nonlocal hashtag_graph
                for node in hashtags_list:
                        hashtag_graph.increase_node(node)
                        
                n = len(hashtags_list)
                for i in range(0, n):
                        for j in range(i+1, n):
                                hashtag_graph.increase_edge(hashtags_list[i],hashtags_list[j])

        #########################################################
        # given a list of hashtags, remove from the graph these #
        # nodes and the edges they form                                #
        #########################################################
        def remove_from_graph(hashtags_list):
                nonlocal hashtag_graph
                for node in hashtags_list:
                        hashtag_graph.decrease_node(node)
                        
                n = len(hashtags_list)
                for i in range(0, n):
                        for j in range(i+1, n):
                                hashtag_graph.decrease_edge(hashtags_list[i],hashtags_list[j])


        with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
                for line in infile:
                        # decode the tweet from json format
                        tweet = json.loads(line)
                        
                        # extract the tweet timestamp and convert it into datetime object
                        if 'created_at' in tweet:
                                time_tweet = tweet['created_at']
                                time_new = datetime.strptime(time_tweet,'%a %b %d %H:%M:%S +0000 %Y')
                        else:
                                continue; # no field for 'created_at', discard

                        # extract the hashtags from json into an array of unique hashtages\
                        hashtags_tweet = tweet['entities']['hashtags']
                        hashtags_list = []
                        for t in hashtags_tweet:
                                hashtag = t['text']
                                if hashtags_list.count(hashtag) == 0:
                                        hashtags_list.append(hashtag)
                                
                        # update the time_newest and the timing window
                        time_diff = compare_time(time_new)
                        if time_diff <= 0:  # if the time_new is newer
                                # update the time offsets in the window
                                for t in window:
                                        t[1] -= time_diff  
                                # insert the new hashtag-offset "tuple"
                                window.append([hashtags_list, 0]) 
                                window_size += 1
                        elif time_diff < 60:  # out-of-order but still within 60 seconds
                                # only insert the new hashtag-offset tuple
                                # search for insertion position from the end of the window
                                i = window_size - 1
                                while i >= 0:
                                        if window[i][1] < time_diff:
                                                i -= 1
                                        else:
                                                i += 1
                                                break
                                window.insert(i, [hashtags_list, time_diff])
                                window_size += 1
                        else:  # out-of-order and outside of 60 seconds range
                                continue  # ignore this tweet and look at the next one
                                
                        # update the hashtag graph with this new hashtags list
                        insert_to_graph(hashtags_list)
                        
                        # search from the front, pop all old tweets from the window
                        # and update the hashtag graph accordingly
                        while window[0][1] >= 60:
                                remove_from_graph(window[0][0])
                                window.pop(0)
                                window_size -= 1

                        # evaluate the average degree and write it to the output file
                        outfile.write('%.2f' % hashtag_graph.avg_degree() + '\n')



###############################
# call of the solution method #
###############################
Solution()

