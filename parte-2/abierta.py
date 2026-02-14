#esta clase contiene los nodos pendientes de ser expandidos
#func_evaluacion (f): funcion de evaluacion, f (n) = g(n) + h(n) (funcion de ordenacion de nodos para sacarMejor) 

class Abierta:
    def __init__(self):
        self.vertices_pendientes = []

    #agrega a la lista de vertices pendientes una tupla con: funcion de evaluacion del vertice correspondiente y vertice 
    def agregarVertice(self, vertice: int, func_evaluacion: float):
        self.vertices_pendientes.append((vertice, func_evaluacion))

    # ordena la lista de forma ascendente según el valor de la funcion de evaluacion
    # y devuelve el vertice con mejor funcion de evaluacion (el primero)
    def sacarMejor(self):
        mejor_indice = 0 #comenzamos por el primer vertice de la lista, indice = 0
        for indice in range(1, len(self.vertices_pendientes)): #recorremos la lista de uno en uno 
            #elegimos el indice con menor funcion de evaluacion.
            if self.vertices_pendientes[indice][1] < self.vertices_pendientes[mejor_indice][1]:
                mejor_indice = indice
                #guardamos el indice con menor funcion de evaluacion
            #al final del bucle, mejor_indice será el indice del vértice con la funcin de evaluacion más pequeña

        #sacamos el vertice cuyo indice coincide con la mejor funcion de evaluacion
        vertice, func_evaluacion = self.vertices_pendientes.pop(mejor_indice)
        return vertice
    
    #devuelve True si la lista esta vacia o False si no 
    def estaVacia(self):
        return len(self.vertices_pendientes) == 0
