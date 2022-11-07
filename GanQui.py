from pyparsing import col
import sys
import math
import folium
from folium import plugins


class Vertice:
    def __init__(self, i, h=0) -> None:
        self.id = i
        self.heuristica = h
        self.vecinos = []
        self.visitado = False
        self.padre = None
        self.costo = float('inf')
        self.costoF = float('inf')

    def agregaVecinos(self, v, p=0):
        if not v in self.vecinos:
            self.vecinos.append([v, p])


class Grafo:
    def __init__(self) -> None:
        self.vertices = {}

    def agregaVertice(self, v, h=0):

        if v not in self.vertices:
            self.vertices[v] = Vertice(v, h)

    def agregarArista(self, a, b, p):

        if a in self.vertices and b in self.vertices:
            self.vertices[a].agregaVecinos(b, p)

    def camino(self, a, b):
        # """Método que va guardando en la lista llamada 'camino' los nodos en el orden que sean visitados y actualizando dicha
        # lista con los vértices con el menor costo"""
        camino = []
        actual = b

        while actual != None:
            camino.insert(0, actual)
            actual = self.vertices[actual].padre
        sk = []
        for j in camino:
            k = str(j)
            s1 = k[k.index("6."):k.index(',')]
            s2 = k[k.index(",")+1:len(k)]
            ass = []
            ass.append(float(s1))
            ass.append(float(s2))

            sk.append(ass)
        return sk

    def hAcum(self, l):
        acum = 0
        for i in l:
            print(acum)
            k = str(i)
            k = k.replace("[", "")
            k = k.replace("]", "")
            k = k.replace(" ", "")
            acum = acum + float(self.vertices[k].heuristica)
        return acum

    def minimoH(self, l):
        # "Método que recibe la lista de los vertices no visitados, revisa si su longitud es mayor a cero(indica que
        # aún hay vértices sin visitar), y realiza comparaciones de los costos de cada vértice en ésta lista para encontrar
        # el de menor costo"
        if len(l) > 0:
            m = self.vertices[l[0]].costoF
            v = l[0]
            for e in l:
                if m > self.vertices[e].costoF:
                    m = self.vertices[e].costoF
                    v = e
            return v
        return v

    def imprimirGrafica(self):
        """Método que imprime el gráfo completo arista por arista con todas sus características(incluye heurística)"""
        for v in self.vertices:

            print("El costo del vértice "+str(self.vertices[v].id)+" con heuristica "+str(
                self.vertices[v].heuristica)+" es " + str(self.vertices[v].costo)+" llegando desde "+str(self.vertices[v].padre))

    def aEstrella(self, a, b):
        # """Método que sigue el algortimo de Bellman-Ford
        # 1. Inicialización
        # 	a) Se crea el conjunto_abierto, con el nodo inicial.
        # 	b) Predecesor nulo para todos los nodos. Costo: 0 para inicial 'infinito' para los demás
        # 	c) Costo heurístico: costo + heuristica para el inicial, 'infinito' para el resto
        # 2. Mientras conjunto abierto tenga elementos
        # 	a) actual <- nodo del conjunto_abierto con menor costo heurístico
        # 	b) si actual = destino, reconstruir camino
        # 	c) Sacar a actual del conjunto abierto y cambiar su estado a visitado
        # 	d) Para cada vecino de actual
        # 		I.	 Si vecino ya está visitado, ignorar y pasar a siguiente
        # 		II.	 Si vecino no esta en conjunto_abierto agregar
        # 		III. Si costo de actual + peso de arista con vecino < costo vecino
        # 			predecesor(vecino) <- actual
        # 			costo(vecino) <- costo(actual) + peso_arista(actual, vecino)
        # 			costo_heuristico(vecino) <- costo(vecino) + heuristica(vecino)
        # 3. Regresar error
        # """
        if a in self.vertices and b in self.vertices:
            # 1.c
            self.vertices[a].costo = 0
            self.vertices[a].costoF = self.vertices[a].heuristica

            # 1.a y 1.b
            for v in self.vertices:
                if v != a:
                    self.vertices[v].costo = float('inf')
                    self.vertices[v].costoF = float('inf')
                self.vertices[v].padre = None

            abierto = [a]

            # 2
            while len(abierto) > 0:
                # 2.a
                actual = self.minimoH(abierto)

                # 2.b
                if actual == b:
                    return [self.camino(a, b), self.vertices[b].costo, self.vertices[b].heuristica, self.vertices[b].padre]

                # 2.c
                abierto.remove(actual)
                self.vertices[actual].visitado = True

                # 2.d
                for v in self.vertices[actual].vecinos:
                    # 2.d.I
                    if self.vertices[v[0]].visitado == False:
                        # 2.d.II
                        if self.vertices[v[0]].id not in abierto:
                            abierto.append(v[0])
                        # 2.d.III

                        if float(self.vertices[actual].costo) + float(v[1]) < float(self.vertices[v[0]].costo):
                            self.vertices[v[0]].padre = actual
                            self.vertices[v[0]].costo = float(
                                self.vertices[actual].costo) + float(v[1])
                            self.vertices[v[0]].costoF = float(
                                self.vertices[v[0]].costo) + float(self.vertices[v[0]].heuristica)
            # 3
            return False
        else:
            return False


def csv_to_dict(nombre_archivo):
    separador = ";"
    with open(nombre_archivo, encoding="utf-8") as archivo:
        next(archivo)  # Omitir encabezado del archivo
        ciudad = []
        for linea in archivo:
            linea = linea.rstrip("\n")  # Quitar salto de línea
            columnas = linea.split(separador)

            nombre = columnas[0]
            og = columnas[1].replace(" ", "")
            origen = og[og.find(',')+1:og.find(')')] + \
                "," + og[1:og.find(',')]

            dt = columnas[2].replace(" ", "")
            destino = dt[dt.find(',')+1:dt.find(')')] + \
                "," + dt[1:dt.find(',')]
            tamaño = columnas[3]
            unadir = bool(columnas[4])
            acoso = columnas[5]
            geometria = columnas[6]

            ciudad.append({
                "nombre": nombre,
                "origen": origen,
                "destino": destino,
                "tamaño": tamaño,
                "unadir": unadir,
                "acoso": acoso,
                "geometria": geometria,
            })
        # print(ciudad[0])

        # a = ciudad[0].get("nombre")
        # print(a)
        return ciudad


def print_list(list):
    ciudads = csv_to_dict("medellin.csv")

    for ciudad in ciudads:
        nombre = ciudad["nombre"]
        origen = ciudad["origen"]
        destino = ciudad["destino"]
        tamaño = ciudad["tamaño"]
        unadir = ciudad["unadir"]
        acoso = ciudad["acoso"]
        geometria = ciudad["geometria"]

        print(f"Nombre:{nombre}, origen:{origen}, destino:{destino}, tamaño:{tamaño}, unadir:{unadir}, acoso: {acoso}, geometria:{geometria}")


def main():
    g = Grafo()

    ciudads = csv_to_dict("medellin.csv")
    a = "6.2099443,-75.568715"
    b = "6.2092431,-75.5690603"

    print(a)
    print(b)

    for i in range(0, len(ciudads)):
        g.agregaVertice(ciudads[i].get("origen"), ciudads[i].get("acoso"))
        if ciudads[i].get("oneway") == True:
            g.agregarArista(ciudads[i].get("origen"), ciudads[i].get(
                "destino"), ciudads[i].get("tamaño"))
        else:
            g.agregarArista(ciudads[i].get("origen"), ciudads[i].get(
                "destino"), ciudads[i].get("tamaño"))
            g.agregarArista(ciudads[i].get("destino"), ciudads[i].get(
                "origen"), ciudads[i].get("tamaño"))

    # for v in g.vertices:

    #     print(v, g.vertices[v].heuristica, g.vertices[v].vecinos)

    print(g.aEstrella(a, b))
    print(" ")
    print(g.hAcum(g.camino(a, b)))

    md_map = folium.Map(
        location=[6.204122, -75.5836638], zoom_start=16, control_scale=True)
    folium.Marker(location=[6.204122, -75.5836638],
                  tooltip="Inicio").add_to(md_map)

    # g.imprimirGrafica()


main()
