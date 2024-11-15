import os

def leer_archivo():
    try:
        with open('Glossary - Sheet2.tsv', 'r') as archivo:
            return archivo.readlines()
    except FileNotFoundError:
        print("Error: El archivo no fue encontrado.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

def procesar_datos(archivo):
    try:
        resultado = []
        for linea in archivo[1:]:  # Skip the first line
            resultado.append([campo.strip() for campo in linea.split('\t')])
        resultado.sort(key=lambda x: x[0].lower(), reverse=True)
        return resultado
    except Exception as e:
        print(f"Error al procesar los datos: {e}")

def crear_termino(termino):
    try:
        print(termino)
        html = f"""
        <div class="termino">
            <dt>{termino[0]}</dt>
            <dd>
        """
        if any(termino[8:13]):
            html += '        <div class="categorias-container">\n'
            for i in range(8, 13):
                if termino[i]:
                    html += f'                    <span class="categoria"><a href="{termino[i].replace(" ","%20")}.html">{termino[i]}</a></span>\n'
            html += '                </div>\n'
        
        html += f'                <p>{termino[1]}</p>\n'
        html += f'                <p>{termino[2]}</p>\n'

        if any(termino[5:8]):
            html += '                <div class="imagenes-container">\n'
            for i in range(5, 8):
                if termino[i]:
                    html += f'                    <img src="{termino[i]}" alt="{termino[i]}">\n'
            html += '                </div>\n'
        
        if any(termino[3:5]):
            html += '                <hr><p>Referencias:</p>\n'
            html += '                <ul class="referencias">\n'
            for i in range(3, 5):
                if termino[i]:
                    html += f'                    <li><a target="_blank" href="{termino[i]}">{termino[i]}</a></li>\n'
            html += '                </ul>\n'
        
        html += '            </dd>\n        </div>\n'
        return html
    except IndexError as e:
        print(f"Error: El término no tiene el formato esperado. {e}")
    except Exception as e:
        print(f"Error al crear el término: {e}")

def generar_pagina_web(resultado):
    try:
        with open('../docs/index.html', 'r') as archivo:
            contenido = archivo.readlines()
        
        # Insert glossary terms with headers for new letters
        inicio_glosario = contenido.index('    <!-- INICIO DE GLOSARIO -->\n')
        fin_glosario = contenido.index('    <!-- FIN DE GLOSARIO -->\n')
        contenido[inicio_glosario+1:fin_glosario] = []
        
        letra_anterior = ""
        for termino in resultado:
            letra_actual = termino[0][0].upper()
            if letra_actual != letra_anterior:
                contenido.insert(inicio_glosario+1, f'        <h2 id="{letra_actual}">{letra_actual}</h2>\n')
                letra_anterior = letra_actual
            contenido.insert(inicio_glosario+2, crear_termino(termino))
        
        # Extract categories
        categorias = set()
        for termino in resultado:
            categorias.update(termino[8:13])
        categorias.discard('')

        # Generate category list HTML
        lista_categorias_html = '    <div class="lista-categorias">\n'
        for categoria in sorted(categorias):
            lista_categorias_html += f'        <span class="categoria"><a href="{categoria.replace(" ","%20")}.html">{categoria}</a></span>\n'
        lista_categorias_html += '    </div>\n'

        # Insert category list
        inicio_cats = contenido.index('    <!-- INICIO CATS -->\n')
        fin_cats = contenido.index('    <!-- FIN CATS -->\n')
        contenido[inicio_cats+1:fin_cats] = [lista_categorias_html]

        with open('../docs/index.html', 'w') as archivo:
            archivo.writelines(contenido)

        # Create category pages
        for categoria in categorias:
            with open(f'../docs/{categoria}.html', 'w') as archivo:
                archivo.write('<html><head><link rel="stylesheet" href="estilos/general.css"></head><body><h1>Glossary - Ben Smith</h1>\n')
                archivo.write(f'<h1>{categoria}</h1>\n')
                archivo.write('<a href="./index.html">back</a>\n<dl>\n')
                # Filter and sort terms for the category
                terms_in_category = [termino for termino in resultado if categoria in termino[8:13]]
                terms_in_category.sort(key=lambda x: x[0].lower())
                
                letra_anterior = ""
                for termino in terms_in_category:
                    letra_actual = termino[0][0].upper()
                    if letra_actual != letra_anterior:
                        archivo.write(f'<h2 id="{letra_actual}">{letra_actual}</h2>\n')
                        letra_anterior = letra_actual
                    archivo.write(crear_termino(termino))
                
                archivo.write('</dl></body></html>\n')

    except FileNotFoundError:
        print("Error: El archivo de salida no fue encontrado.")
    except Exception as e:
        print(f"Error al generar la página web: {e}")

def main():
    try:
        archivo = leer_archivo()
        if archivo:
            resultado = procesar_datos(archivo)
            if resultado:
                generar_pagina_web(resultado)
    except Exception as e:
        print(f"Error en la función principal: {e}")

main()
