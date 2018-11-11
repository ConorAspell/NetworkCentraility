import networkx as nx
class Main:
    def readCSV(self): #Text Processing to make the network and calculate weights
        global G
        G = nx.DiGraph() #An empty NetworkX directed graph
        file = open("results.csv", "r")
        for line in file:
            words = line.split(",")
            words[1] = int(words[1])
            words[3] = int(words[3])
            if words[0] not in G:
                G.add_node(words[0])
            if words[2] not in G:
                G.add_node(words[2])
            if words[1] > words[3]:
                score = abs(words[1]-words[3])
                
                if G.has_edge(words[0], words[2]):
                    G.edge[words[0]][words[2]]['weight'] += score;
                else:
                    G.add_edge(words[0], words[2])
                    G.edge[words[0]][words[2]]['weight'] = score;
            if words[3] >= words[1]:
                score = abs(words[3]-words[1])
                if G.has_edge(words[2], words[0]):
                    G.edge[words[2]][words[0]]['weight'] += score;
                else:
                    G.add_edge(words[2], words[0])
                    G.edge[words[2]][words[0]]['weight'] = score;
                    
        groups = {}
        i =0
        #We will code here
        
        nx.set_node_attributes(G, 'centrality', nx.in_degree_centrality(G)) #this sets the "centrality" value, we will need
                                                                            #to calculate centrality above this and set it here  
        for item in G.nodes(): #Just sets an identifier for each team
            groups[item] = i 
            i+=1  
        nx.set_node_attributes(G, 'groups', groups)     
        
    def makeJSON(self, G): #Makes a JSON for visualisation purposes which can be viewed here: http://bl.ocks.org/conoraspell/ac2f6cda7bae02fd7a7fd271476f867b
        i =0
        j =0 
        
        size1 = len(G.nodes())
        data = nx.get_node_attributes(G, 'groups')
        data2 = nx.get_node_attributes(G, 'centrality')
        size = len(G.edges())
        json =""
        json += "{\n\"nodes\":[\n"
        for item in G:
            j+=1
            
                
            if(j<size1):
                json+= "{\n \"name\": \"" + item + "\",\n\"group\":"+ str(data[item])+ ",\n\"centrality\":"+ str(0.5)+"\n},"
            else:
                json+= "{\n \"name\": \"" + item + "\",\n\"group\":"+str(data[item])+",\n\"centrality\":"+ str(0.5)+"\n}"
        json+="],\"links\": [\n"
        for u, v, weight in G.edges(data='weight'):
            
            i += 1
            if(i<size):
                json += "{\"source\": " + str(data[u]) + ", \"target\": " + str(data[v]) + ", \"value\": " + str(weight) + ", \"type\": \"arrow\""+"},\n"
            else:
                json += "{\"source\": " + str(data[u]) + ", \"target\": " + str(data[v]) + ", \"value\": " + str(weight) + ", \"type\": \"arrow\""+"}\n"
            
        json += "]\n}"
        print(json)
main = Main()
main.readCSV()
main.makeJSON(G)
