
def csv_to_dict(nombre_archivo):
    separador = ";"
    with open(nombre_archivo, encoding="utf-8") as archivo:
        next(archivo)  # Omitir encabezado del archivo
        ciudad = []
        for linea in archivo:
            linea = linea.rstrip("\n")  # Quitar salto de línea
            columnas = linea.split(separador)

            nombre = columnas[0]
            origen = columnas[1]
            destino = columnas[2]
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
        return ciudad


def main():
    ciudads = csv_to_dict("medellin.csv")
    for ciudad in ciudads:
        nombre = ciudad["nombre"]
        origen = ciudad["origen"]
        destino = ciudad["destino"]
        tamaño = ciudad["tamaño"]
        unadir = ciudad["unadir"]
        acoso = ciudad["acoso"]
        geometria = ciudad["geometria"]

        # print(
        #     f"Nombre:{nombre}, origen:{origen}, destino:{destino}, tamaño:{tamaño}, unadir:{unadir}, acoso: {acoso}, geometria:{geometria}")


main()
