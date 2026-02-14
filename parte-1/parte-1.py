import sys
from pathlib import Path
from constraint import *

USO = "Uso correcto: python parte-1.py <entrada.in> <salida.out>"

# Funciones creadas para el cumplimiento de las restricciones
#Restricción 1 y 2: conteo de X en cada fila y columna, nº de X tiene que coincidir con nº O. Por lo que:
#la mitad de los valores de la lista deben ser X (lo que significa que la otra mitad son O)
def contador_X_O(*valores):
    conteo_x = 0
    for valor in valores:
        if valor == "X": conteo_x += 1
    return conteo_x * 2 == len(valores)   # equivale a X == O

#Restricción 3 y 4: no deben haber tres simbolos iguales consecutivos en fila/columna
def consecutivos(*valores):
    for posicion in range(len(valores) - 2):
        if valores[posicion] == valores[posicion + 1] ==  valores[posicion + 2]:
            return False
    return True


#creamos una funcion para mostrar el tablero en el formato deseado
def mostrarTablero(n, tablero):
    print("+---"*n + "+")
    for num_fila in range(n):
        print("|", end='')
        for num_columna in range(n):
            valor = tablero[f"X_{num_fila}_{num_columna}"]
            print(f" {valor} |", end='')
        print()
    print("+---"*n + "+")

# funcion para escribir las soluciones en archivo de salida.out
def escribirTablero(salida, n, tablero):
    salida.write("+---"*n + "+\n")
    for num_fila in range(n):
        salida.write("|")
        for num_columna in range(n):
            valor = tablero[f"X_{num_fila}_{num_columna}"]
            salida.write(f" {valor} |")
        salida.write("\n")
    salida.write("+---"*n + "+\n")


#funcion principal
def main():
    #verifica el nº de argumentos
    if len(sys.argv) != 3:
        print(USO, file=sys.stderr)
        sys.exit(1)
    
    #rutas de los ficheros de entrada y salida
    ruta_in = Path(sys.argv[1])
    ruta_out = Path(sys.argv[2])

    #verificar que existe el fichero .in
    if not ruta_in.exists(): # si no existe = error
        print(f"Error: no existe el fichero de entrada: {ruta_in}", file=sys.stderr)
        sys.exit(2)

    #leer .in
    lineas = []
    # abrimos fichero y leemos cada linea
    with ruta_in.open("r", encoding="utf-8") as fichero:
        for linea in fichero: # cada linea del fichero
            valor = linea.strip() # eliminar espacios en blanco al inicio y final
            #cada linea no vacia la guardamos
            if valor:
                lineas.append(valor)
    #verificamos nº de filas y el nº de columnas
    n = len(lineas)

    #primero si el tablero esta vacío (n = 0)
    if n == 0:
        print("Error: el tablero está vacío", file=sys.stderr)
        sys.exit(3)

    #para la resolución del problema n tiene que ser par (un cuadrado)
    if (n % 2) != 0:
        print("Error: n debe ser un valor par", file=sys.stderr)
        sys.exit(3)
    
    #comprobar que n filas = n columnas (es nxn)
    for num_fila, fila in enumerate(lineas, start=1):
        if len(fila) != n:
            print(f"Error: la fila {num_fila} tiene longitud {len(fila)} pero se esperaba {n}", file=sys.stderr)
            sys.exit(3)
    
    #variable para guardar el tablero inicial
    tablero_inicial = {}

    #comprobar que las filas contienen símbolos válidos
    validos = {'.', 'X', 'O'}
    for num_fila, fila in enumerate(lineas):
        for num_columna, simbolo in enumerate(fila):
            if simbolo not in validos:
                print(f"Error: símbolo inválido '{simbolo}' en fila {num_fila}, col {num_columna}", file=sys.stderr)
                sys.exit(3)
            #cambiamos "." por " " para luego mostrar por pantalla en el tablero inicial como se especifica 
            if simbolo == ".":
                    simbolo = " "
            #guardamos el tablero inicial
            tablero_inicial[f"X_{num_fila}_{num_columna}"] = simbolo
        
    
    #una vez se verifica que los valores del .in son correctos, creamos el problema
    problem = Problem()

    #definimos variables, nº variables = nxn y su dominio depende del valor almacenado en cada linea
    for num_fila, fila in enumerate(lineas): 
        for num_columna, simbolo in enumerate(fila): 
            #si ya tiene valor X, únicamente va a poder tomar valor X
            if simbolo == "X":
                dominio = ["X"]
            #si ya tiene valor O, únicamente va a poder tomar valor O
            elif simbolo == "O":
                dominio = ["O"]
            #si no tiene X/O, puede tomar valor X ó O
            else:
                dominio = ["X", "O"]
            #añadimos la variable con su dominio correspondiente
            problem.addVariable(f"X_{num_fila}_{num_columna}", dominio)
    """
    habiendo definido el dominio para las variables ya cumplimos con la 
    restricción en donde no puede quedar ninguna posicion vacia
    puesto que los valores que pueden tomar son X ó O segun estos mismos
    """
    #una vez definimos los dominios aplicamos las restricciones
    #Restricciones para las filas: 
    for num_fila in range(n): 
        #construimos la lista de variables de la fila 
        valores_fila = [f"X_{num_fila}_{num_columna}" for num_columna in range(n)]
        #Restricción 1: mismo número de X y O por fila
        problem.addConstraint(contador_X_O, valores_fila)
        #Restricción 3: No pueden haber tres simbolos iguales consecutivos
        problem.addConstraint(consecutivos, valores_fila)
    
    #Restricciones para las columnas:
    for num_columna in range(n):
        #construimos la lista de variables de la columna
        valores_columna = [f"X_{num_fila}_{num_columna}" for num_fila in range(n)]
        #Restricción 2. mismo número de X y O por columna
        problem.addConstraint(contador_X_O, valores_columna)
        #Restricción 4: No pueden haber tres simbolos iguales consecutivos
        problem.addConstraint(consecutivos, valores_columna)

    """
    por ultimo, soluciones
    por pantalla imprime: 1. Tablero vacío, 2. nº de soluciones encontradas y 3. Una solucion encontrada
    Luego, en el fichero de salida .out se guardan las soluciones encontradas
    """

    #1. mostramos el tablero inicial del .in
    mostrarTablero(n, tablero_inicial)

    #2. nº de soluciones encontradas
    soluciones = problem.getSolutions()
    print ("{0} soluciones encontradas".format (len (soluciones)))
    
    #si hay soluciones entonces: 
    if soluciones:
        #3. imprimimos una de las soluciones encontradas
        mostrarTablero(n, soluciones[0])
    else:
        print("\nNo hay soluciones.")

    #4. guardamos en el archivo de salida .out las soluciones encontradas
    #si no hay soluciones, solo quedará el tablero inicial
    with ruta_out.open("w", encoding="utf-8") as salida:
        escribirTablero(salida, n, tablero_inicial)
        for sol in soluciones:
            escribirTablero(salida, n, sol)

if __name__ == "__main__":
    main()
