from pyparsing import col


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
    ciudads = csv_to_dict("medellin.csv")
    a = ciudads[0].get("origen")
    b = ciudads[0].get("destino")
    print(a)
    print(b)


main()
