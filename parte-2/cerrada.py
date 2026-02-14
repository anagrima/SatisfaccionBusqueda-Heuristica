#contiene todos los nodos que ya han sido expandidos
class Cerrada:
    def __init__(self):
        #inicializamos un set vacío para que luego quea más facil y rápido buscar
        self.vertices_expandidos = set() #además con set controlamos duplicados

    #agrega a la lista de vertices expandidos 
    def agregarVertice(self, vertice:int):
        self.vertices_expandidos.add(vertice)
    
    #informa si el vertice se encuentra en la lista de vertices expandidos
    def contiene(self, vertice: int):
        return vertice in self.vertices_expandidos

    #hace un conteo del tamaño de la lista de vertices expandidos
    def contarVerticesExpandidos(self):
        return len(self.vertices_expandidos)
