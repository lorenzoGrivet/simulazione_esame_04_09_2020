import warnings

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self.selectedNode = None
        self.view = view
        # the model, which implements the logic of the program and holds the data
        self.model = model



    def handleCreaGrafo(self, e):
        self.view.txtGrafo.clean()
        rank=self.view.txtRank.value
        if rank=="":
            self.view.create_alert("Inserire rank")
        try:
            intRank=float(rank)
        except ValueError:
            self.view.create_alert("Rank non numerico")
            return
        self.model.creaGrafo(intRank)
        n,a= self.model.getDetails()
        self.view.txtGrafo.controls.append(ft.Text(f"Nodi: {n}. Archi: {a}"))
        self.view.update_page()
        self.fillDD()

        pass


    def handleGradoMassimo(self, e):
        res,peso=self.model.gradoMax()
        self.view.txtGrafo.controls.append(ft.Text(f"Film grado max: {res}"))
        self.view.txtGrafo.controls.append(ft.Text(f"Peso: {peso}"))
        self.view.update_page()

        pass

    def handleCalcolaCammino(self, e):
        if self.selectedNode is None:
            self.view.create_alert("Scegliere nodo")
        res,c =self.model.cammino(self.selectedNode)
        self.view.txtGrafo.controls.append(ft.Text(f"\nCammino da {self.selectedNode}"))
        self.view.txtGrafo.controls.append(ft.Text(f"Peso: {c}"))
        for a in res:
            self.view.txtGrafo.controls.append(ft.Text(f"{a[0]} -- {a[1]}, peso= {a[2]}"))
        self.view.update_page()
        pass



    def fillDD(self):
        nodi=self.model.getNodes()
        nodiDD=list(map(lambda x: ft.dropdown.Option(key=x,on_click=self.getSelectedNode),nodi))
        self.view.ddFilm.options=nodiDD
        self.view.update_page()
        pass

    def getSelectedNode(self,e):
        if e.control.key is None:
            pass
        else:
            self.selectedNode=e.control.key


           