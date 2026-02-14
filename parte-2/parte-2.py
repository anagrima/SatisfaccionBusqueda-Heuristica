import sys, time
from pathlib import Path
from grafo import Grafo
from algoritmo import Algoritmo

USO = "Uso correcto: python parte-2.py <vertice-1> <vertice-2> <nombre-del-mapa> <salida>"


#las siguientes funciones servrian para escribir en el fichero de salida con el formato deseado

#devuelve el coste de ir de un vertice a otro
def costeArco(grafo: Grafo, vertice_1: int, vertice_2: int):
    for vertice, coste in grafo.vecinosVertice(vertice_1):
        if vertice == vertice_2:
            return coste
    raise ValueError(f"No existe arco {vertice_1}->{vertice_2}")

def escribirSolucion(ruta_salida: Path, camino: list[int], grafo: Grafo):
    # escibimos por ejemplo: 1 - (1498) - 308 - (8718) - 309, vertices y el coste de ir de un vertice a otro
    vertices = [str(camino[0])] #obtenemos los vertices del camino obtenido en la resolucion del problema
    for vertice in range(len(camino) - 1): #por cada vertice buscamos el coste de ir de v1 a v2
        vertice_1 = camino[vertice]
        vertice_2 = camino[vertice + 1]
        coste_v1_v2 = costeArco(grafo, vertice_1, vertice_2)
        vertices.append(f"- ({coste_v1_v2}) - {vertice_2}")
    ruta_salida.write_text(" ".join(vertices) + "\n", encoding="utf-8")

#resolvemos las rutas .gr y .co
def resolverRutas(nombre_mapa: str):
    ruta_base = Path(nombre_mapa)

    # Si pasan "algo.gr" o "algo.co", quita esa extensión final
    if str(ruta_base).endswith(".gr"):
        ruta_base = Path(str(ruta_base)[:-3])
    elif str(ruta_base).endswith(".co"):
        ruta_base = Path(str(ruta_base)[:-3])

    # USA-road-d.USA/USA-road-d.USA.gr
    if ruta_base.exists() and ruta_base.is_dir():
        gr = ruta_base / (ruta_base.name + ".gr")
        co = ruta_base / (ruta_base.name + ".co")
        return gr, co

    # Por ejemplo pasan el nombre base (USA-road-d.USA)
    # y los ficheros están en el mismo directorio actual
    gr = Path(str(ruta_base) + ".gr")
    co = Path(str(ruta_base) + ".co")
    return gr, co


def main():

    #verifica el nº de argumentos    
    if len(sys.argv) != 5:
        print(USO, file=sys.stderr)
        sys.exit(1)

    #verifica que existe ruta .gr y .co para el nombre del mapa especificado
    ruta_gr, ruta_co = resolverRutas(sys.argv[3])


    #verificar que existe el fichero .gr
    if not ruta_gr.exists(): # si no existe = error
        print(f"Error: no existe el fichero: {ruta_gr}", file=sys.stderr)
        sys.exit(2)

    if not ruta_co.exists(): # si no existe = error
        print(f"Error: no existe el fichero: {ruta_co}", file=sys.stderr)
        sys.exit(2)

    #convertimos los índices a int y establecemos un rango 
    try:
        vertice_1 = int(sys.argv[1])
        vertice_2 = int(sys.argv[2])
    except ValueError:
        print("Error: vértice-1 y vértice-2 deben ser números enteros", file=sys.stderr)
        sys.exit(1)

    #guarda la ruta de salida como path
    salida = Path(sys.argv[4])

    #inicializamos el grafo. la clase Grafo lee los archivos gr y co, guarda los vectores y sus vecinos y las coordenadas de cada vectos
    grafo = Grafo(ruta_gr, ruta_co)

    # validar que existen como claves 
    if vertice_1 not in grafo.vecinos or vertice_2 not in grafo.vecinos:
        print("Error: alguno de los vértices no existe en el mapa", file=sys.stderr)
        sys.exit(3)

    #inicializamos el algoritmo
    algoritmo = Algoritmo(grafo)
    t_inicial = time.perf_counter() #medimos tiempo inicial
    camino, coste, expansiones = algoritmo.aEstrella_h2(vertice_1, vertice_2) #resolvemos el problema llamando a la heuristica que se usará
    t_final = time.perf_counter() #medimos tiempo final

    tiempo = t_final - t_inicial #calculamos el tiempo de ejecucion

    # imrpime por pantalla:
    print(f"# vertices: {grafo.num_vertices}") #nº de vertices procesados
    print(f"# arcos : {grafo.num_arcos}") #nº de arcos procesados

    #si camino esta vacio entonces no se ha encontrado solucion
    if camino is None:
        print("No se ha encontrado solución")
        salida.write_text("No se ha encontrado camino", encoding="utf-8")
        sys.exit(0)

    #si hay solucion, imprime la solucion óptima encontrada
    print(f"Solución óptima encontrada con coste {coste}\n")

    # nodes/sec
    if tiempo > 0:
        nodes_sec = expansiones / tiempo
    else:
        nodes_sec = float("inf")

    #tiempo de ejecucion calculado anteriormente
    print(f"Tiempo de ejecución: {tiempo:.4f} segundos")
    #nº de nodos expandidos (nodos en la lista cerrada)
    print(f"# expansiones : {expansiones} ({nodes_sec:.2f} nodes/sec)")

    #escribe en el fichero de salida con el formato pedido
    escribirSolucion(salida, camino, grafo)

if __name__ == "__main__":
    main()
   