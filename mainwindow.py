from ast import NodeVisitor
from tkinter import font
from token import NUMBER
from turtle import width
from PySide2 import QtWidgets
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from ui_mainwindow import Ui_MainWindow
import numpy as np
#from tabulate import tabulate
from colorama import init, Fore, Back, Style
import reglasObjetos
import networkx as nx  
import matplotlib.pyplot as plt  


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()


        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        header = self.ui.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        self.ui.pushButton.clicked.connect(self.Automata)
        

    @Slot()
    def Automata(self): 
        #Pila de strings
        pila2 = []
        pila2.append('$')
        pila2.append('0')
        entrada2 = []
        #print(pila2, entrada2)
        
        #Pila de enteros
        pila = []
        pila.append('2')
        pila.append('0')
        entrada = []
        
                    
        matrizLR = [['d2','','','1'], #0
                    ['','','r0(acept)',''], #1
                    ['','d3','r2',''], #2
                    ['d2','','','4'], #3
                    ['','','r1',''] #4
                    ]

        #Variables iniciales
        elementos=[]
        estado = 0
        indice = 0
        cadena = self.ui.textEdit.toPlainText().strip() + '$'
        while(indice<=(len(cadena)-1)  and estado==0):  
                #Se inicializan las siguientes variables
                lexema=''
                token='error'
                num=-1
                #Mientras el indice sea menor a la longitud de la cadena y NO se encuentre en el estado 20
                while(indice<=(len(cadena)-1) and estado!=20):
                    if estado==0:#Si está en el estado inicial
                        #Si en la posición cadena[indice] hay espacio en blanco
                        if(cadena[indice].isspace()):
                            estado=0 #El estado se establece como el inicial
                        #Si en la posición cadena[indice] hay una letra o un guión bajo
                        elif cadena[indice].isalpha() or cadena[indice]=='_':
                            estado=4 #La variable estado se establece con el número 4
                            lexema+=cadena[indice] #Al lexema se le agrega el contenido de cadena[indice]
                            token='identificador' #El token se define como un identificador
                            num=0 #La variable num se establece con el número 0
                            entrada.append(num)
                            #entrada2.append(lexema)
                        #Si en la posición cadena[indice] hay un $ (fin de cadena)
                        elif cadena[indice]=='$':
                            estado=20 #Se establece el estado como el final
                            lexema+=cadena[indice] #Al lexema se le agrega el contenido de cadena[indice]
                            token='$'  #El token se define como un signo de pesos o final de cadena
                            #num=23 #La variable num se establece con el número 23
                            num=2
                            entrada.append(num)
                            #entrada2.append(lexema)
                        elif cadena[indice].isdigit():
                            lexema+=cadena[indice]
                            token='entero'
                            estado=6 
                            num=1
                            #entrada.append(num)
                        elif cadena[indice]=='"':
                            lexema+=cadena[indice]
                            estado=11
                            indice+=1
                        elif cadena[indice]=='=':
                            lexema+=cadena[indice]
                            token='='
                            estado=5  
                            num=18  
                            #entrada.append(num)
                        elif cadena[indice]=='+' or cadena[indice]=='-':
                            lexema+=cadena[indice]
                            token='opSuma'
                            estado=20
                            #num=5 
                            num=1
                            entrada.append(num)
                            #entrada2.append(lexema)
                        elif cadena[indice]=='*' or cadena[indice]=='/':
                            lexema+=cadena[indice]
                            token='opMul'
                            estado=20 
                            num=6
                            entrada.append(num)
                        elif cadena[indice]=='<' or cadena[indice]=='<=' or cadena[indice]=='>' or cadena[indice]=='>=':
                            lexema+=cadena[indice]
                            token='opRelac'
                            estado=20 
                            num=7 
                            #entrada.append(num)
                        elif cadena[indice]=='||':
                            lexema+=cadena[indice]
                            token='opOr'
                            estado=20 
                            num=8
                            #entrada.append(num)  
                        elif cadena[indice]=='&&':
                            lexema+=cadena[indice]
                            token='opAnd'
                            estado=20 
                            num=9
                            #entrada.append(num)
                        elif cadena[indice]=='!':
                            lexema+=cadena[indice]
                            token='opNot'
                            estado=10 
                            num=10   
                            #entrada.append(num)
                        elif cadena[indice]==';':
                            lexema+=cadena[indice]
                            token=';'
                            estado=20 
                            num=12 
                            #entrada.append(num)
                        elif cadena[indice]==',':
                            lexema+=cadena[indice]
                            token=','
                            estado=20 
                            num=13 
                            #entrada.append(num)
                        elif cadena[indice]=='(':
                            lexema+=cadena[indice]
                            token='('
                            estado=20 
                            num=14
                            #entrada.append(num) 
                        elif cadena[indice]==')':
                            lexema+=cadena[indice]
                            token=')'
                            estado=20 
                            num=15
                            #entrada.append(num)
                        elif cadena[indice]=='{':
                            lexema+=cadena[indice]
                            token='{'
                            estado=20 
                            num=16
                            #entrada.append(num) 
                        elif cadena[indice]=='}':
                            lexema+=cadena[indice]
                            token='}'
                            estado=20 
                            num=17
                            #entrada.append(num)
                        #Si NO hay un espacio en blanco o alguno de los tokens válidos       
                        else:
                            estado=20 #Se establece el estado como el final
                            token='error' #El token se define como un error
                            lexema=cadena[indice] #Al lexema se le agrega el contenido de cadena[indice]
                            num=-1 #La variable num se establece con el número -1
                        indice+=1 #Se le suma 1 a la variable indice (se pasa a la siguiente posición)
                    elif estado==4:
                        #Si en la posición cadena[indice] hay un digito, una letra o un guión bajo
                        if cadena[indice].isdigit() or cadena[indice].isalpha() or cadena[indice]=='_':
                            estado=4 #Se establece el estado como el 4
                            lexema+=cadena[indice] #Al lexema se le agrega el contenido de cadena[indice]
                            token='identificador' #El token se define como un identificador
                            indice+=1 #Se le suma 1 a la variable indice (se pasa a la siguiente posición)
                            num=0 #La variable num se establece con el número 1
                            #entrada.append(num)
                            #entrada2.append(lexema)
                        #Si en la posición cadena[indice] NO hay un digito, una letra o un guión bajo
                        else:
                            estado=20 #Se establece el estado como el final
                    elif estado==5:
                        #Si en la posición cadena[indice] NO hay un "="
                        if cadena[indice]!='=':
                            estado=20 #Se establece el estado como el final
                        #Si en la posición cadena[indice] NO hay un "="
                        else:
                            estado=20 #Se establece el estado como el final
                            lexema+=cadena[indice] #Al lexema se le agrega el contenido de cadena[indice]
                            token='opIgualdad' #El token se define como un operador de igualdad
                            indice+=1 #Se le suma 1 a la variable indice (se pasa a la siguiente posición)
                            num=11 #La variable num se establece con el número 11
                            #entrada.append(num)
                    elif estado==6:
                        if cadena[indice].isdigit():
                            estado=7 
                            lexema+=cadena[indice] 
                            token='entero' 
                            indice+=1 
                            num=1 
                            #entrada.append(num)
                        if cadena[indice]=='.':
                            estado=7
                            lexema+=cadena[indice]
                            indice+=1
                        else:
                            estado=20  
                    elif estado==7:
                        if cadena[indice].isdigit():
                            estado=8
                            lexema+=cadena[indice]
                            token='real'
                            indice+=1
                            num=2
                            #entrada.append(num)
                        if cadena[indice]=='.':
                            estado=8
                            lexema+=cadena[indice]
                            indice+=1
                        else:
                            estado=20
                    elif estado==8:
                        if cadena[indice].isdigit():
                            estado=9
                            lexema+=cadena[indice]
                            token='real'
                            indice+=1
                            num=2
                            #entrada.append(num)
                        else:
                            estado=20
                    elif estado==9:
                        if cadena[indice].isdigit():
                            estado=20
                            lexema+=cadena[indice]
                            token='real'
                            indice+=1
                            num=2
                            #entrada.append(num)
                        else:
                            estado=20
                    elif estado==10:
                        if cadena[indice]!='=':
                            estado=20
                        else:
                            estado=20
                            lexema+=cadena[indice]
                            token='opIgualdad'
                            indice+=1
                            num=11
                            #entrada.append(num)
                    elif estado==11:
                        if cadena[indice]=='"':
                            estado=20
                            lexema+=cadena[indice]
                            token='cadena'
                            num=3
                            #entrada.append(num)
                        else:
                            while(indice<=(len(cadena)-1) and cadena[indice]!='"'): 
                                lexema+=cadena[indice]
                                token='cadena'
                                num=3
                                indice+=1
                                #entrada.append(num)
                estado = 0
                elementos.append({'token':token,'num':num,'lexema':lexema})
                #print(lexema)
                entrada2.append(lexema)

        init(autoreset=True) 
        r1 = 'r1 = E -> id + E'
        r2 = 'r2 = E -> id'
        print("{:^85}".format(Fore.YELLOW+'Tabla LR(1)'))
        print("{:^51} {:^12}".format(Fore.GREEN+r1,Fore.GREEN+r2))
        print ("{:^15} {:^15} {:^15} {:^15} {:^15}".format('','0','1','2','3','4'))
        print ("{:^16} {:^18} {:^23} {:^17} {:^22}".format('',Fore.CYAN+'id',Fore.CYAN+'+',Fore.CYAN+'$',Fore.CYAN+'E'))
        num=0
        for v in matrizLR:
            id, mas, pesos, E = v
            print ("{:^15} {:^15} {:^15} {:^15} {:^15}".format(num, id, mas, pesos, E))
            num+=1
        #Análisis LR con pila de enteros
        print('\n')      
        print("{:^100}".format(Fore.YELLOW+'Análisis LR(1) con Pila de Enteros')+ "{:^16}".format(Fore.YELLOW+'Análisis LR(1) con Pila de strings'))
        print('{:<40}{:<20}{:<5}'.format(Fore.CYAN+'Pila',Fore.CYAN+'Entrada',Fore.CYAN+'Salida')+'{:>28}{:>35}{:>32}'.format(Fore.CYAN+'Pila',Fore.CYAN+'Entrada',Fore.CYAN+'Salida'))
        #print('{:^45}{:^35}{:^13}'.format('Pila','Entrada','Salida'))
        
        #Análisis LR con pila de strings
        # print('\n')      
        # print("{:^130}".format(Fore.YELLOW+'Análisis LR(1) con Pila de strings'))
        # print('{:^50}{:^40}{:^18}'.format(Fore.CYAN+'Pila',Fore.CYAN+'Entrada',Fore.CYAN+'Salida'))
        
        def agregar_arista( G, u, v, di=True): # , w='' despues de v
            G.add_edge(u, v) # , weight=w
            
            #Si el grafo no es dirigido
            G.add_edge(v, u) # , weight=w
            
        #Declaración del grafo
        G = nx.DiGraph()
        
        dimension = len(entrada2)-1  
        #print('Dimension: '+str(dimension))
        if(dimension==1):
            objR2 = reglasObjetos.R2('E',entrada2[0])  # objR2 = reglasObjetos.R2(entrada2[0],'E') 
            nodoE = objR2.getPadre()
            nodoID = 'id'
            #pesoID = objR2.getID()
            
            agregar_arista(G, nodoE, nodoID) #, pesoID
            
            #Se dibuja el grafo con networkx y matplotlib mostrando las etiquetas de los nodos y usando el color yellow
            pos = nx.layout.planar_layout(G)
            nx.draw_networkx(G, pos, node_color='yellow', node_size=400, font_weight='bold')
            #labels = nx.get_edge_attributes(G, 'weight')
            #nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            plt.title('Grafo generado de la gramática')
            plt.show()
        else:             #r1 = E -> id + E          #r2 = E -> id   
            i=0
            datoR1=''
            datoR2 = ''   
            Padre=''
            datoR1Temp = ''
            
            #a+\b+\c+\d
            lengtInput = len(entrada2)-1
            while(i<lengtInput):
                if(i==1): #r1 = E -> id + E  
                    Padre = reglasObjetos.R1(entrada2[0],None,entrada2[1],None)
                    datoR1 = Padre
                    #print("1")
                    #print(entrada2[0]," ",entrada2[1])
                else:
                    if(i%2!=0 and i>1 and i!=lengtInput-1):#r1 = E -> id + E
                        datoR1Temp = reglasObjetos.R1(entrada2[i-1],datoR1,entrada2[i],None)#nodo actual                        
                        #print("Mitad")
                        datoR1.child = datoR1Temp
                        datoR1 = datoR1Temp
                    else:  
                        if(i==lengtInput-1):#r2 = E -> id 
                            #print("Fin") #
                            datoR2 = reglasObjetos.R2(datoR1,entrada2[i]) 
                            datoR1.child = datoR2  
                i+=1
            Padre.terminal=0
            Padre.nodo=0
            Padre.Print() 
            
        #print(entrada2)
        
        '''
        #Se dibuja el grafo con networkx y matplotlib mostrando las etiquetas de los nodos y usando el color yellow
        nx.draw(G, with_labels=True, node_color='yellow', node_size=400, font_weight='bold')  # networkx draw()
        plt.draw()  # pyplot draw()
        plt.show()
        '''
        
        
        while(True):
            
            #Pila de enteros
            x = int(entrada[0])
            y = int(pila[len(pila)-1])
            salida = matrizLR[y][x]
            

            #Pila de strings
            x2 = entrada2[0]
           
            #Análisis LR con pila de enteros
            print('{:<40}{:<20}{:<6}'.format(Fore.YELLOW+str(pila),Fore.GREEN+str(entrada),Fore.MAGENTA+salida)+'{:^55}{:<32}{:^9}'.format(Fore.YELLOW+str(pila2),Fore.GREEN+str(entrada2),Fore.MAGENTA+salida))

            #Análisis LR con pila de strings
            # print('{:^50}{:^40}{:^18}'.format(Fore.YELLOW+str(pila2),Fore.GREEN+str(entrada2),Fore.MAGENTA+salida2))
        
            if(salida == ''):
                print('ERROR!')
                QMessageBox.information(self,'Mensaje','Cadena rechazada!')
                break
            if(salida == 'r0(acept)'):
                QMessageBox.information(self,'Mensaje','Cadena aceptada!')
                break
            
            if(salida[0] == 'd'):
                #Pila de enteros
                entrada.pop(0)
                pila.append(x)
                pila.append(salida[1])
                
                #Pila de strings
                entrada2.pop(0)
                pila2.append(x2)
                pila2.append(salida[1])
                                
            elif(salida[0] == 'r'):
                if(salida[1] == '1'): 
                    #Pila de enteros
                    pila.pop()
                    pila.pop()
                    pila.pop()
                    pila.pop()
                    pila.pop()
                    pila.pop()
                    
                    pos = int(pila[len(pila)-1])
                    aux = int(matrizLR[pos][3])
                    
                    pila.append('3')
                    pila.append(aux)
                    
                    #Pila de strings
                    pila2.pop()
                    pila2.pop()
                    pila2.pop()
                    pila2.pop()
                    pila2.pop()
                    pila2.pop()
                    
                    pila2.append('3')
                    pila2.append(aux)
                
                    if(aux == ''):
                        print('ERROR!')
                        QMessageBox.information(self,'Mensaje','Cadena rechazada!')
                        break   
                else:
                    #Pila de enteros
                    pila.pop()
                    pila.pop()
                    
                    pos = int(pila[len(pila)-1])
                    aux = int(matrizLR[pos][3])
                    
                    pila.append('3')
                    pila.append(aux)
                    
                    #Pila de strings
                    pila2.pop()
                    pila2.pop()
                    
                    pila2.append('3')
                    pila2.append(aux)
                    
                    if(aux == ''):
                        print('ERROR!')
                        QMessageBox.information(self,'Mensaje','Cadena rechazada!')
                        break
                        
        self.ui.tableWidget.clearContents()

        row = 0
        self.ui.tableWidget.setRowCount(len(elementos))

        for elemento in elementos:
            if elemento['lexema']=="if":
                elemento['token']="if"
                elemento['num'] = 19
            elif elemento['lexema']=="else":
                elemento['token']="else"
                elemento['num'] = 22
            elif elemento['lexema']=="while":
                elemento['token']="while"
                elemento['num']=20
            elif elemento['lexema']=="return":
                elemento['token']="return"
                elemento['num']=21
            elif elemento['lexema']=="int":
                elemento['token']="tipo de dato"
                elemento['num']=4
            elif elemento['lexema']=="float":
                elemento['token']="tipo de dato"
                elemento['num']=4
            elif elemento['lexema']=="void":
                elemento['token']="tipo de dato"
                elemento['num']=4
            
            self.ui.tableWidget.setItem(row,0,QTableWidgetItem(elemento['token']))
            self.ui.tableWidget.setItem(row,1,QTableWidgetItem(str(elemento['num'])))
            self.ui.tableWidget.setItem(row,2,QTableWidgetItem(elemento['lexema']))
            row +=1  