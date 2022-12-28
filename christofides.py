# Prim's Algorithm in Python
import copy
import networkx as nx
import matplotlib.pyplot as plt

#Algorithme de prim pour déterminer ACM 
INF = 9999999
# le nombre de sommet
V = 5
# la matrice d'adjacence

G = [[0, 9, 75, 2, 6,79],
     [9, 0, 95, 19, 42,5],
     [75,95, 0, 51, 66,31],
     [2, 19, 51, 0, 31,12],
     [6, 42, 66, 31, 0,37],
     [79, 5, 31, 12, 37,0]]

# créer un tableau pour suivre le sommet sélectionné
# sélectionné deviendra vrai sinon faux
selected = [0, 0, 0, 0, 0]
# set number of edge to 0
no_edge = 0
# le nombre d'arêtes dans l'arbre couvrant minimum sera
# toujours inférieur à(V - 1), où V est le nombre de sommets dans
# graphique
# choisissez le 0ème sommet et rendez-le vrai
selected[0] = True
# imprimer pour le bord et le poids
print("Edge : Weight\n")
#liste des prédécesseur, sucesseurs et poids
liste_x=[]
liste_y=[]
liste_poid=[]

while (no_edge < V - 1):
    # Pour chaque sommet de l'ensemble S, trouver tous les sommets adjacents
     #, calculez la distance à partir du sommet sélectionné à l'étape 1.
     # si le sommet est déjà dans l'ensemble S, supprimez-le sinon
     # choisissez un autre sommet le plus proche du sommet sélectionné à l'étape 1.
    minimum = INF
    x = 0
    y = 0
    
    for i in range(V):
        if selected[i]:
            for j in range(V):
                if ((not selected[j]) and G[i][j]):  
                    # pas sélectionné et il y a une arrête
                    if minimum > G[i][j]:
                        minimum = G[i][j]
                        x = i
                        y = j
    print(str(x) + "-" + str(y) + ":" + str(G[x][y]))
    liste_x.append(x)
    liste_y.append(y)
    liste_poid.append(G[x][y])
    
    selected[y] = True
    no_edge += 1
#les arrête de mon ACM
les_couple_acm=[]
i1=0
while i1 <len(liste_x):
    i2=0
    while i2 <len(liste_y):
        if i1==i2:
            a= (liste_x[i1],liste_y[i2])
            les_couple_acm.append(copy.deepcopy(a)) 
           
        i2=i2+1
    i1=i1+1
print(f"\nx= {liste_x} \ny= {liste_y} \npoids= {liste_poid}\nles couple:{les_couple_acm}")



#génération de la matrice d'adjacence de ACM
def nouveau_arbre(sommet:int, x:list, y:list, poid:list):
    # je construit l'ACM
    arbre= []
    for i in range(sommet):
        arbre.append([])
        for j in range(sommet):
            arbre[i].append(0)
    for i in range(len(x)):
        for j in range (len(y)):
            if i==j:
                arbre[x[i]][y[j]]= poid[j]
                arbre[y[j]][x[i]]= poid[j]
    return arbre

Mat_adj_abre= nouveau_arbre(5,liste_x,liste_y,liste_poid)
print(f"ACM: {Mat_adj_abre}")

#la fonction pour déssiner le graphe
def dessin(G):
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) ]
   
    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def cree(l_x:list,l_y:list,l_p):
    i=0
    
    G= nx.Graph()
    while i <len(l_x):
        
        j=0
        while j <len(l_y):
            if i==j:
                a=copy.deepcopy(l_x[i])
                b=copy.deepcopy(l_y[j]) 
                c=copy.deepcopy(l_p[j])
            
                G.add_edge( a,b , weight= c )
            j=j+1
        i=i+1
    return G

#je vais créer l'ACM pour le déssiner
Graphe_final=cree(liste_x,liste_y,liste_poid)
dessin(Graphe_final)

#je détermine la liste des dégré

def determine_des_deg(abre:list[list]):
    #j'énumère la liste des dégré
    n=0
    liste_deg=[]
    for i in range(len(abre)):
        for j in range(len(abre)):
            if abre[i][j]:
                n=n+1
        liste_deg.append(n)
        n=0
    
    print(f"liste des dégré : {liste_deg}\n")
    return liste_deg
liste_des_deg=determine_des_deg(Mat_adj_abre)

#je recupère les sommets de dégrés impaire
def deg_impaire(deg:list):
    liste_des_degr=[]
    #déterminons les deg impairs
    for i in range(len(deg)):
        if ( deg[i] % 2) == 0:
            deg[i]=0
    for k in range(len(deg)):
        if deg[k]!=0:
            liste_des_degr.append(k)
    print(f"les sommets de dégré impairs sont{liste_des_degr}\n")
    return liste_des_degr
liste_deg_impairs=deg_impaire(liste_des_deg)


#on va déterminer le couplage minimum
#on va d'abord déterminer les combinaisons possibles
from itertools import combinations
def n_length_combo(arr, n):
    #retoune une combinaison sans duplication
    return list(combinations(arr, n))
n= 2 #cardinal du couple   
combinaisons1=n_length_combo([x for x in liste_deg_impairs], n)


#jai formé les couples
#on va determiner les couplages
#voici la liste de u-plet de couplage possible
nb= len(liste_deg_impairs)/2  #le nombre de sommets impaire d'un graphe est toujours paire
combinaisons2=n_length_combo([x for x in combinaisons1], n)

#on va eleminer les couplage non disjoints
def est_disjoint(a:tuple,b:tuple):
    i=0
    j=0
    while i< len(a):
        while j< len(b):
            if a[i]==b[j]:
                return False
            j=j+1
        i=i+1
        j=0
    return True

def couplages(va:list[tuple[tuple]], initial:list):
    n= len(initial)/2 #le nombre de sommets impaire d'un graphe est paire
    selection=[]
    for elemt in va:
        nombre=0
        for i in range(len(elemt)):
            for j in range(len(elemt)):
                if i!=j:
                    a=elemt[i]
                    b=elemt[j]  
                    c=est_disjoint(a,b)
                    if c==True:
                        nombre=nombre+1
                        if nombre==n:
                            selection.append(elemt)
    return selection
#j'ai éliminé les disjoints
couplage= couplages(combinaisons2,liste_deg_impairs)
#j'ai maliste de couplage possible
#je vais choisir le minimum
def liste_couplage(liste_couplage:list[tuple[tuple]], graphe_initial:list[list], listes_couples_initial: list[tuple]):
    indice_minimum =0
    poids_min=9999999
    i=0
    while i<len(liste_couplage):
        long= copy.deepcopy( len(liste_couplage))
        a= liste_couplage[i]
        for elemt in listes_couples_initial:
            j= 0
            while j <len(a):
                b= (a[j][1],a[j][0] )
                # print(b)
                if elemt==a[j] or elemt==b :
                    liste_couplage.pop(i)
                    break
                j=j+1
        if long > len(liste_couplage):
            i=i
        else:
            i=i+1
    print(f"les couplages possibles:{liste_couplage}")
    return liste_couplage

liste_couple_finale=liste_couplage(couplage,G, les_couple_acm)
#j'ai trouvé une liste de couplage sans doublons et sans arrête déja utilisé
def minimum_couplage(liste:list[tuple], origine: list[list]):
    for element in liste:
        poids_min=99999
        poids=0
        i=0
        n=0
        while i < len(element):
            b= element[i]
            if origine[b[0]][b[1]]==0:
                 break   
            else:
                n=n+1
                poids= origine[b[0]][b[1]] +poids
                i=i+1    
        if poids< poids_min and n== len(element):
            poids_min= poids
    print(f"\nle couplage minimum est \n{element}\nson poids:{poids} \n ")
    return element
le_couplage= minimum_couplage(liste_couple_finale,G)
#j'ai enfin le couplage minimum
#je vais ajouter aux listes sucessurs et prédécéssseurs
for i in le_couplage:
    a= copy.deepcopy(i[0])
    b= copy.deepcopy(i[1])
    liste_x.append(copy.deepcopy(a))
    liste_y.append(copy.deepcopy(b))
    liste_poid.append(G[a][b])
    Mat_adj_abre[a][b]=G[a][b]
#ajouter le couplage au graphe et déssiner le nouvaue de graphe

Graphe_final= cree(liste_x,liste_y,liste_poid)
dessin(Graphe_final)
print(f"matrice d'adjacence du nouveau abre{Mat_adj_abre}")

#nous allons utiliser maintenat l'agorithme de fleury pour déterminer le cycle eulerien



from collections import defaultdict

#Cette classe représente un graphe non orienté utilisant la représentation de liste d'adjacence
class Graph:

    def __init__(self,vertices):
        self.V= vertices #Nombre de sommets
        self.graph = defaultdict(list) # dictionnaire par défaut pour stocker le graphique
        self.Time = 0

    # fonction pour ajouter une arête au graphique
    def addEdge(self,u,v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    # Cette fonction supprime l'arête u-v du graphique
    def rmvEdge(self, u, v):
        for index, key in enumerate(self.graph[u]):
            if key == v:
                self.graph[u].pop(index)
        for index, key in enumerate(self.graph[v]):
            if key == u:
                self.graph[v].pop(index)

   # Une fonction basée sur DFS pour compter les sommets accessibles à partir de v
    def DFSCount(self, v, visited):
        count = 1
        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                count = count + self.DFSCount(i, visited)		
        return count

    # La fonction pour vérifier si l'arête u-v peut être considérée comme l'arête suivante dans
     # Visite d'Euler
    def isValidNextEdge(self, u, v):
        # L'arête u-v est valide dans l'un des deux cas suivants :

         # 1) Si v est le seul sommet adjacent de u
        if len(self.graph[u]) == 1:
            return True
        else:
            '''
            2) S'il y a plusieurs adjacents, alors u-v n'est pas un pont
                 Suivez les étapes suivantes pour vérifier si u-v est un pont

            2.a) nombre de sommets accessibles depuis u'''
            visited =[False]*(self.V)
            count1 = self.DFSCount(u, visited)

            '''2.b) Retirez l'arête (u, v) et après avoir enlevé l'arête, comptez
                 sommets accessibles depuis u'''
            self.rmvEdge(u, v)
            visited =[False]*(self.V)
            count2 = self.DFSCount(u, visited)

            #2.c) Ajouter l'arrête au graphique
            self.addEdge(u,v)

            # 2.d) Si count1 est supérieur, alors l'arête (u, v) est un pont
            return False if count1 > count2 else True


   # Imprimer le tour d'Euler à partir du sommet u
    def printEulerUtil(self, u, liste:list):
       #Recur pour tous les sommets adjacents à ce sommet
        for v in self.graph[u]:
           #Si l'arête u-v n'est pas supprimée et qu'il s'agit d'une arête suivante valide
            if self.isValidNextEdge(u, v):
                liste.append(u)
                print("%d-%d " %(u,v)),
                self.rmvEdge(u, v)
                self.printEulerUtil(v, liste)
    '''La fonction principale qui imprime Eulerian Trail. Il trouve d'abord un impair
degré de sommet (s'il y en a un) puis appelle printEulerUtil()
pour imprimer le chemin '''
    def printEulerTour(self):
       #Trouver un sommet avec un degré impair
        u = 0
        for i in range(self.V):
            if len(self.graph[i]) %2 != 0 :
                u = i
                break
        # Imprimer le tour à partir d'un sommet impair
        print ("\n")
        sommets_euler=[]
        self.printEulerUtil(u,sommets_euler)
        print(f"le cycle euleurien est :{sommets_euler}")
        return sommets_euler
nb1=0
Graphe_final= Graph (len(liste_x))
while nb1< len(liste_x):
    nb2=0
    while nb2<len(liste_y):
        if nb2==nb1:
            Graphe_final.addEdge(liste_x[nb1],liste_y[nb2])

        nb2=nb2+1
    nb1=nb1+1
liste_sommet= Graphe_final.printEulerTour()
i=0
while i < len(liste_sommet)-1:
    j=i+1
    while j< len(liste_sommet)-1:
        if liste_sommet[i]== liste_sommet[j]:
            liste_sommet.pop(j)
            j=j
        else:
            j=j+1
    i=i+1
print( f"le plus court chemin est {liste_sommet}")



        


