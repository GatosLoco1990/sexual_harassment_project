from pyparsing import col


class Vertice:
    def __init__(self, i, h="n/a") -> None:
        self.id = i
        self.visitado = False
        self.nivel = -1
        self.padre = None
        self.vecinos = []
        self.dist = float('inf')
        self.distF = float('inf')
        self.risk = h

    def agregaVecinos(self, v):
        if not v in self.vecinos:
            self.vecinos.append(v)


class Grafo:
    def __init__(self) -> None:
        self.vertices = {}

    def agregaVertice(self, v):

        if v not in self.vertices:
            self.vertices[v] = Vertice(v)

    def agregarArista(self, a, b):

        if a in self.vertices and b in self.vertices:
            self.vertices[a].agregaVecinos(b)
            self.vertices[b].agregaVecinos(a)

    def aEstrella(self, a, b):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].costo = 0
            self.vertices[a].costoF = self.vertices[a].costo + \
                self.vertices[a].heuristica

        for v in self.vertices:
            if v != a:
                self.vertices[v].costo = float('inf')
                self.vertices[v].costoF = float('inf')
            self.vertices[v].padre = None

        abierto = [a]

        while (len(abierto) > 0):
            actual = self.minimoH(abierto)

            if actual == b:
                return [self.camino(a, b), self.vertices[b].costo]

            abierto.remove(actual)
            self.vertices[actual].visitado = True

            for v in self.vertices[actual].vecinos:
                if self.vertices[v[0]].visitado == False:
                    if self.vertices[v[0]].id not in abierto:
                        abierto.append(v[0])

                    if self.vertices[actual].costo + v[1] < self.vertices[v[0]].costo:
                        self.vertices[v[0]].padre = actual
                        self.vertices[v[0]
                                      ].costo = self.vertices[v[0]].costo + v[1]
                        self.vertices[v[0]].costoF = self.vertices[v[0]
                                                                   ].costo + self.vertices[v[0]].heuristica


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
            origen = "(" + og[og.find(',')+1:og.find(')')] + \
                "," + og[1:og.find(',')] + ")"

            dt = columnas[2].replace(" ", "")
            destino = "(" + dt[dt.find(',')+1:dt.find(')')] + \
                "," + dt[1:dt.find(',')] + ")"
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

        #a = ciudad[0].get("nombre")
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
    a = ciudads[0].get("origen")
    b = ciudads[0].get("destino")
    g.agregaVertice(ciudads[0].get("origen"))
    g.agregarArista(ciudads[0].get("origen"), ciudads[0].get("destino"))
    print(a)
    print(b)

    for i in range(0, len(ciudads)):
        g.agregaVertice(ciudads[i].get("origen"))
        g.agregarArista(ciudads[i].get("origen"), ciudads[i].get("destino"))

    # g.dfs()


main()
