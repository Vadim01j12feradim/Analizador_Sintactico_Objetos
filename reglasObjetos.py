import networkx as nx
import matplotlib.pyplot as plt

#Declaración del grafo
G = nx.DiGraph()

def agregar_arista( G, u, v, di=True): # , w='' despues de v
        G.add_edge(u, v) # , weight=w
            
        #Si el grafo no es dirigido
        G.add_edge(v, u) # , weight=w
'''
var1='0'
var2='1'
var3=var1
var4='2'
agregar_arista(G,var1,var2)
agregar_arista(G,var3,var4)


#Se dibuja el grafo con networkx y matplotlib mostrando las etiquetas de los nodos y usando el color yellow
pos = nx.layout.planar_layout(G)
nx.draw_networkx(G, pos, node_color='yellow', node_size=400, font_weight='bold')     
plt.title('Grafo generado de la gramática')
plt.show()
'''

class R1():  
    def __init__(self, id, E, operador,child): #r1 = E -> id + E
        self.identificador = id
        self.terminal = E
        self.operador = operador
        self.child = child
        self.nodo=0
        
    def returnChild(self):
        return self.child
    
    def getID(self):
        return self.identificador
    
    def getTerminal(self):
        return self.terminal
    
    def Print(self):
        # print("E")
        # print("id: ",self.identificador)
        # print("Operador: ",self.operador,"\n\n")
        
        self.child.nodo=self.nodo+1
        
        agregar_arista(G, 'E'+str(self.nodo), 'E'+str(self.child.nodo))
        agregar_arista(G, 'E'+str(self.nodo), self.identificador)
        agregar_arista(G, 'E'+str(self.nodo), str(self.nodo)+self.operador)
        
        self.child.Print() 
        
class R2():
    def __init__(self, Padre, id): #r2 = E -> id 
        self.padre = Padre
        self.id = id
        self.nodo=1
    
    def getPadre(self):
        return self.padre 
    
    def getID(self):
        return self.id
    
    def Print(self):
        # print("E")
        # print("id: ",self.id) 
        
    
        agregar_arista(G, 'E'+str(self.nodo), self.id)
        #agregar_arista(G, self.)
        
        #Se dibuja el grafo con networkx y matplotlib mostrando las etiquetas de los nodos y usando el color yellow
        pos = nx.layout.planar_layout(G)
        nx.draw_networkx(G, pos, node_color='yellow', node_size=400, font_weight='bold')     
        plt.title('Grafo generado de la gramática')
        plt.show()
    
    

'''
#Probando clases
pruebaR1 = R1('Hola','Mundo')
print('R1: '+ pruebaR1.getID() + pruebaR1.getTerminal())
pruebaR2 = R2('Hola')
print('R2: '+ pruebaR2.getID())
'''
