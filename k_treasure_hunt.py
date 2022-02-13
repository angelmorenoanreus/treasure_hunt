import networkx as nx
import random

class Player:
    def __init__(self,start,G):
        self.start=start
        self.G=G.copy()

    def read_interactor_feedback(self,interactor_input):
        splited_input=interactor_input.split(' ')
        current_degree=int(splited_input[1])
        adjacent_deg_flag=[]
        for i in range(2,len(splited_input),2):
            deg=int(splited_input[i])
            flag=int(splited_input[i+1])
            adjacent_deg_flag.append((deg,flag))
        return current_degree,adjacent_deg_flag

    def make_decision(self,current_degree,adjacent_deg_flag):
        sorted_list=sorted(adjacent_deg_flag,key=lambda x:x[0]) #Sorts by degree
        sorted_list.sort(key=lambda x:x[1]) #Sorts flag==0 first
        selected_deg_flag=sorted_list[0]
        selected_index=adjacent_deg_flag.index(selected_deg_flag)
        return selected_index + 1 #+1 because indexes must beggin with 1

        
class Interactor:
    def __init__(self,start,G):
        self.current_node=start
        self.G=G.copy()
    
    def give_feedback(self,moves_count,base_move_count):
        if all(map(lambda x: x==1,nx.get_node_attributes(self.G,'flag'))): #if all nodes explored
            resu= 'AC'
        elif moves_count>2*base_move_count:
            resu= 'F'
        else:
            current_degree=self.G.degree[self.current_node]
            neighbor_nodes=list(self.G.neighbors(self.current_node))
            random.shuffle(neighbor_nodes) #sorts negihbor_nodes randomly 
            self.neighbor_nodes=neighbor_nodes
            degrees_dict={elem[0]:elem[1] for elem in list(self.G.degree(neighbor_nodes))}
            flags_dict=nx.get_node_attributes(self.G,'flag')
            deg_flag_list=[(degrees_dict[node],flags_dict[node]) for node in neighbor_nodes]
            
            resu=f'R {current_degree}'
            for elem in deg_flag_list:
                resu+=f' {elem[0]} {elem[1]}'
            
        print(resu)
        return resu

    def update(self,decision):
        index=decision-1
        nx.set_node_attributes(self.G,{self.current_node:1},name='flag')
        destiny_node=self.neighbor_nodes[index]
        self.current_node=destiny_node

def main():
    number_of_tests=int(input())

    for _ in range(number_of_tests):
        n,m,start,base_move_count=tuple(map(int, input().split(' ')))
        
        

        G=create_graph(m)

        player=Player(start,G)
        interactor=Interactor(start,G)

        moves_count=0
        while True:
            #interactor prints degrees and flags of the adjacent vertices as for example: R 2 2 0 2 0
            interactor_feedback=interactor.give_feedback(moves_count,base_move_count)
            if interactor_feedback[0]=='R':
                current_degree,adjacent_deg_flag=player.read_interactor_feedback(interactor_feedback)
                decision=player.make_decision(current_degree,adjacent_deg_flag)
                print(decision)
                interactor.update(decision)

            else:
                break
            moves_count+=1






def create_graph(m):
    G=nx.Graph()
    for _ in range(m):
        u,v=tuple(map(int, input().split(' ')))
        G.add_edge(u,v)
    nodes_list=list(G.nodes)
    d_attrs={node:0 for node in nodes_list}
    nx.set_node_attributes(G,d_attrs,name='flag')
    return G






if __name__ == '__main__':
    main()