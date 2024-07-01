import copy
import random

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.nodoMax = None
        self.maxArchi = None
        self.grafo= nx.Graph()
        self.idMap={}
        self.solBest=[]
        self.maxConto=0

    def creaGrafo(self,rank):
        self.grafo.clear()
        nodi=DAO.getNodi()
        self.grafo.add_nodes_from(nodi)
        for a in nodi:
            self.idMap[a.id]=a
        archi=DAO.getArchi(rank)
        for a in archi:
            self.grafo.add_edge(self.idMap[a[0]],self.idMap[a[1]],peso=a[2])


    def getDetails(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def gradoMax(self):
        self.maxArchi=0

        for a in list(self.grafo.nodes):
            succ=self.grafo.neighbors(a)
            somma=0
            for i in succ:
                somma+=self.grafo[a][i]["peso"]

            if somma>self.maxArchi:
                self.maxArchi=somma
                self.nodoMax=a

        return self.nodoMax,self.maxArchi

    def getNodes(self):
        return list(self.grafo.nodes(data=False))

    def cammino(self,start):
        self.solBest=[]
        self.maxConto=0
        parziale=[start]
        self.ricorsione(parziale,start)
        res=[]
        for a in range(len(self.solBest)-1):
            res.append((self.solBest[a],self.solBest[a+1],self.grafo[self.solBest[a]][self.solBest[a+1]]["peso"]))

        return res,self.maxConto
    def ricorsione(self, parziale, start):
        print("*")
        succ=list(self.grafo.neighbors(start))
        ammissibili=self.getAmmissibili(parziale,succ,start)

        if self.isTerminale(ammissibili):
            if len(parziale)> self.maxConto:
                self.maxConto=len(parziale)
                self.solBest=copy.deepcopy(parziale)
        else:
            for a in ammissibili:
                parziale.append(a)
                self.ricorsione(parziale,a)
                parziale.pop()


        pass

    def getAmmissibili(self, parziale, succ,start):
        ammissibili=[]
        if len(parziale)<2:
            return succ
        else:
            for a in succ:
                if a not in parziale:
                    if self.grafo[start][a]["peso"]>=self.grafo[parziale[-2]][start]["peso"]:
                        ammissibili.append(a)
        return ammissibili

        pass

    def isTerminale(self, ammissibili):
        if len(ammissibili)==0:
            return True
        return False
        pass

