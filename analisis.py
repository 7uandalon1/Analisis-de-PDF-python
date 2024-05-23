import re
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
from tkinter.ttk import Label
from datetime import datetime
import pandas as pd
import PyPDF2
from PIL import Image, ImageTk
import time
import threading


root = tk.Tk()
root.geometry("1080x1920")
root.state("zoomed")
# Cambia el color de fondo a blanco
root.config(bg="#C7DAE2")
# Obtiene la altura de la pantalla
screen_height = root.winfo_screenheight()

header = tk.Frame(root)

# Establece la altura de la cabecera al 100px
header.config(height=100)

# Establece el fondo de la cabecera al blanco
header.config(bg="#C7DAE2")


def eliminar_palabras(cadena, palabras):
    expresión_regular = r"\b({})\b".format("| ".join(palabras))
    cadena_modificada = re.sub(expresión_regular, "", cadena)
    return cadena_modificada


def threading_init(event):
    # Call work function
    t1 = threading.Thread(target=abrir_archivo(event))
    t1.start()


global barra_progreso
barra_progreso = Progressbar(root, orient="horizontal", length=200)
labels_list = []


def barra():
    barra_progreso.pack()
    barra_progreso.start()
    return barra_progreso


def parar_barra():
    barra_progreso.stop()
    barra_progreso.pack_forget()


def clear_labels():
    for label in labels_list:
        label.pack_forget()
    labels_list.clear()
    parar_barra()


header.config(width=root.winfo_screenwidth())
clear_button = tk.Button(root, text="Limpiar Labels", command=clear_labels)
clear_button.pack(pady=10)
# Crea un widget Button para cerrar el programa
close_button = tk.Button(header, text="Cerrar", command=root.destroy)

# Coloca el botón de cierre en la esquina superior derecha de la cabecera
close_button.pack(side="top", anchor="ne", padx=10, pady=10)

# Coloca la cabecera en la parte superior de la ventana
header.pack(side="top", fill="both", expand="yes")
imagen_original = Image.open("logo.png")

# Establecer el tamaño deseado
nuevo_tamano = (1000, 300)
imagen_redimensionada = imagen_original.resize(nuevo_tamano)

# Convertir la imagen redimensionada a un formato compatible con Tkinter
imagen_tk = ImageTk.PhotoImage(imagen_redimensionada)

# Crear una etiqueta con la imagen
label = tk.Label(header, image=imagen_tk)
Label.config(self=label, background="#C7DAE2")
label.pack()
# Crea un widget Label para el título de la cabecera

root.title("Abrir archivo")

expresion_regular_fecha_nacimiento = re.compile(
    r"""
    \b\d{1,2}[-/]\w+[-/]\d{2,4}\b |    # DD/MMM/YY o DD/MMM/YYYY o D/MMM/YY o D/MMM/YYYY
    \b\d{1,2}\s(?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)\s\d{2,4}\b |  # DD Mes YY o DD Mes YYYY
    \b(?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)\s\d{1,2},?\s\d{2,4}\b |  # Mes DD, YYYY o Mes DD YYYY
    \b\d{1,2}\s(?:ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)\b               # DD Mes
    """,
    re.IGNORECASE | re.VERBOSE,
)
palabras_a_eliminar = [
    "SEXO",
    "IDENTIFICACIÓN",
    "IDENTIFICACION",
    "FECHA",
    "DE",
    "NACIMIENTO",
]
# Empieza a reproducir el video de carga


def calcular_tiempo_transcurrido(fecha_nacimiento, fecha_folio):
    # Convertir meses de palabras a números
    meses = {
        "enero": "01",
        "febrero": "02",
        "marzo": "03",
        "abril": "04",
        "mayo": "05",
        "junio": "06",
        "julio": "07",
        "agosto": "08",
        "septiembre": "09",
        "octubre": "10",
        "noviembre": "11",
        "diciembre": "12",
    }

    fecha_nac = re.sub(
        r"(\w+)", lambda x: meses.get(x.group(1).lower(), x.group(1)), fecha_nacimiento
    )
    fecha_fol = re.sub(
        r"(\w+)", lambda x: meses.get(x.group(1).lower(), x.group(1)), fecha_folio
    )

    fecha_nac = datetime.strptime(fecha_nac, "%d/%m/%Y")
    fecha_fol = datetime.strptime(fecha_fol, "%d/%m/%Y")
    delta = fecha_fol - fecha_nac
    años = delta.days // 365
    meses = (delta.days % 365) // 30
    dias = (delta.days % 365) % 30
    return f"{años} años / {meses} meses / {dias} días"


def abrir_archivo(event):
    t4 = threading.Thread(target=barra)
    # Mostrar el diálogo para abrir un archivo.
    filename = filedialog.askopenfilename()
    t4.start()
    if not filename:
        parar_barra()
    print(filename)
    t = threading.Thread(target=procesar_pdf, args=(filename,))
    t.start()


def procesar_pdf(filename):
    data = {
        "Nombre": [],  # completado
        "Identificación": [],  # completado
        "Fecha de Nacimiento": [],  # completado
        "Fecha de folio": [],  # completado
        "Tiempo transcurrido entre fecha de nacimiento y fecha de folio": [],  # completado
        "USS": [],  # completado
        "Urgencias": [],  # completado
        "Sexo": [],  # completado
        "Especialidad del médico": [],  # completado
        "Fecha de notificación": [],  # completado
        "Nombre del médico": [],  # completado
        "Hemoglobina": [],  # completado
        "Peso": [],  # completado
        "Talla": [],  # completado
        "Perimetro del brazo": [],
        "Prueba de apetito": [],
        "FTLC": [],
        "F75": [],
        "Pediasure": [],
        "Infatrini": [],
        "Leche de Vaca": [],
        "Amoxicilina": [],  # completado
        "Albendazol": [],  # completado
        "Antiparasitario": [],
        "Ácido Fólico": [],
        "Cita": [],
        "Carnet de vacunación": [],
        "ICBF": [],  # completado
    }
    # Lee el archivo PDF
    with open(filename, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_paginas = len(pdf_reader.pages)
        # for numero_pagina in range(num_paginas):
        pagina = pdf_reader.pages[0]
        text = pagina.extract_text()
        lines = text.split("\n")
        for line in lines:
            if "Nombre Paciente: " in line:
                # Inicializa la lista antes de usarla
                paciente = []

                # Agrega el nombre del paciente al conjunto
                paciente_fase1 = line.split("Nombre Paciente: ")[1].strip()
                paciente_fase2 = " ".join(re.findall(r"\b[A-Z]+\b", paciente_fase1))
                resultado = eliminar_palabras(paciente_fase2, palabras_a_eliminar)
                paciente.append(resultado)
                data["Nombre"].append(resultado)

                set(paciente.copy())
            if "NOMBRE PACIENTE: " in line:
                paciente = []

                # Agrega el nombre del paciente al conjunto
                paciente_fase1 = line.split("NOMBRE PACIENTE: ")[1].strip()
                paciente_fase2 = " ".join(re.findall(r"\b[A-Z]+\b", paciente_fase1))
                resultado = eliminar_palabras(paciente_fase2, palabras_a_eliminar)
                paciente.append(resultado)
                data["Nombre"].append(resultado)
                # Procesa las líneas del PDF
        for line in lines:
            identificacion = []
            if "identificacion" in line.lower():
                identificacion_fase1 = line.lower().split("identificacion: ")[1].strip()
                identificacion_fase2 = " ".join(
                    re.findall(r"\b\d{5,}\b", identificacion_fase1)
                )
                identificacion.append(identificacion_fase2)
                resultado = identificacion
                data["Identificación"].append(identificacion_fase2)
                set(identificacion.copy())
            if "identificación" in line.lower():
                identificacion_fase1 = line.lower().split("identificación: ")[1].strip()
                identificacion_fase2 = " ".join(
                    re.findall(r"\b\d{5,}\b", identificacion_fase1)
                )
                data["Identificación"].append(identificacion_fase2)

                set(identificacion.copy())
            for line in lines:
                if "nacimiento" in line.lower():
                    if not data.get("Fecha de Nacimiento"):
                        resultado = []
                        fecha_n_fase1 = re.search(r"nacimiento:\s*(\S+)", line.lower())
                        fecha_n_fase1 = fecha_n_fase1.group(1)
                        fecha_n_fase2 = "".join(
                            expresion_regular_fecha_nacimiento.findall(fecha_n_fase1)
                        )
                        resultado.append(fecha_n_fase2)
                        set(resultado.copy())
                        data["Fecha de Nacimiento"].append(fecha_n_fase2)

                if re.search(r"fecha (de)?folio", line.lower()):
                    if not data.get("Fecha de folio"):
                        resultado = []
                        folio_n_fase1 = re.search(r"folio:\s*(\S+)", line.lower())
                        folio_n_fase1 = folio_n_fase1.group(1)
                        folio_n_fase2 = "".join(
                            expresion_regular_fecha_nacimiento.findall(folio_n_fase1)
                        )
                        resultado.append(folio_n_fase2)
                        set(resultado.copy())
                        data["Fecha de folio"].append(folio_n_fase2)
                if re.search(r"fecha de ingreso", line.lower()):
                    if not data.get("Fecha de folio"):
                        resultado = []
                        folio_n_fase1 = re.search(
                            r"fecha de ingreso:\s*(\S+)", line.lower()
                        )
                        folio_n_fase1 = folio_n_fase1.group(1)
                        folio_n_fase2 = "".join(
                            expresion_regular_fecha_nacimiento.findall(folio_n_fase1)
                        )
                        resultado.append(folio_n_fase2)
                        set(resultado.copy())
                        data["Fecha de folio"].append(folio_n_fase2)
                    if data["Fecha de Nacimiento"]:
                        if not data.get(
                            "Tiempo transcurrido entre fecha de nacimiento y fecha de folio"
                        ):
                            tiempo_transcurrido = calcular_tiempo_transcurrido(
                                data["Fecha de Nacimiento"][-1],
                                data["Fecha de folio"][-1],
                            )
                            data[
                                "Tiempo transcurrido entre fecha de nacimiento y fecha de folio"
                            ].append(tiempo_transcurrido)
                expresion = r"urgencias"
                patron = re.compile(expresion, re.IGNORECASE)
                if not data.get("Urgencias"):
                    if re.search(patron, line):
                        data["Urgencias"].append("SI")
                    else:
                        data["Urgencias"].append("NO")
                if not data.get("Sexo"):
                    sex_expresion = r"sexo:"
                    sex_patron = re.compile(sex_expresion, re.IGNORECASE)
                    if re.search(sex_patron, line):
                        expresion_regular = r"sexo:\s*(\w+)"
                        coincidencias = re.findall(
                            expresion_regular, line, re.IGNORECASE
                        )
                        if coincidencias:
                            data["Sexo"].append(coincidencias[0])
                            break

        for pagina_com in range(num_paginas):
            texto_pagina = pdf_reader.pages[pagina_com]
            text = texto_pagina.extract_text()
            lines = text.split("\n")
            uss_pattern = re.compile(r"\bUSS\b(?:\s+\w+){1,5}\b", re.IGNORECASE)
            if not data.get("USS"):
                match = uss_pattern.search(text)
                if match:
                    uss_found = match.group()
                    data["USS"].append(uss_found)
                    break

        for pagina_com in range(num_paginas):
            texto_pagina = pdf_reader.pages[pagina_com]
            text = texto_pagina.extract_text()
            lines = text.split("\n")

            if not data.get("Especialidad del médico"):
                esp_expresion = r"especialidad\s*(.+)"
                esp_patron = re.compile(esp_expresion, re.IGNORECASE)

                filtro_1 = re.search(esp_patron, text)
                if filtro_1:
                    # Obtiene el texto después de "especialidad"
                    texto_filtrado = (
                        filtro_1.group(1).strip() if filtro_1.group(1) else ""
                    )
                    if texto_filtrado:
                        # pagina_especialista = pagina_com
                        data["Especialidad del médico"].append(texto_filtrado)
                        break
        for pagina_com in range(num_paginas):
            texto_pagina = pdf_reader.pages[pagina_com]
            text = texto_pagina.extract_text()
            lines = text.split("\n")

            if not data.get("FTLC"):
                fltc_expresion = r"FTLC"
                fltc_patron = re.compile(fltc_expresion, re.IGNORECASE)

                filtro_fltc = re.search(fltc_patron, text)
                if filtro_fltc:
                    # Obtiene el texto después de "especialidad"
                    texto_fltc = (
                        filtro_fltc.group(1).strip() if filtro_fltc.group(1) else ""
                    )
                    if texto_fltc:
                        # pagina_especialista = pagina_com
                        print("encontrado")
                        break

            # print(pagina_especialista)
            # texto_pagina = pdf_reader.pages
            # text = texto_pagina.extract_text()
            # lines = text.split("\n")

            if not data.get("Nombre del médico"):
                esp_expresion = r"Profesional\s*(.+)"
                esp_patron = re.compile(esp_expresion, re.IGNORECASE)

                filtro_1 = re.search(esp_patron, text)
                if filtro_1:
                    # Obtiene el texto después de "especialidad"
                    texto_filtrado = (
                        filtro_1.group(1).strip() if filtro_1.group(1) else ""
                    )
                    if texto_filtrado:
                        data["Nombre del médico"].append(texto_filtrado)
                        break
        for pagina_com in range(num_paginas):
            texto_pagina = pdf_reader.pages[pagina_com]
            text = texto_pagina.extract_text()
            lines = text.split("\n")

            if not data.get("ICBF"):
                esp_expresion = r"reporte a icbf"
                esp_patron = re.compile(esp_expresion, re.IGNORECASE)

                filtro_icbf_1 = esp_patron.search(text)
                if filtro_icbf_1:
                    data["ICBF"].append("SI")
                else:
                    data["ICBF"].append("NO")
            if not data.get("Albendazol"):
                alb_expresion = r"albendazol"
                alb_patron = re.compile(alb_expresion, re.IGNORECASE)
                filtro_alb_1 = alb_patron.search(text)
                if filtro_alb_1:
                    data["Albendazol"].append("SI")
                else:
                    data["Albendazol"].append("NO")
            if not data.get("Amoxicilina"):
                amo_expresion = r"amoxicilina"
                amo_patron = re.compile(amo_expresion, re.IGNORECASE)
                filtro_amo_1 = amo_patron.search(text)
                if filtro_amo_1:
                    data["Amoxicilina"].append("SI")
                else:
                    data["Amoxicilina"].append("NO")
            # Verificar si "Hemoglobina" está presente en los datos
            if not data.get("Hemoglobina"):
                # Definir la expresión regular con re.IGNORECASE para ignorar mayúsculas y minúsculas
                patron = re.compile(
                    r"\b(hb|hemoglobina)\b(?![^(]*\))\s*([0-9]+(?:\.[0-9]+)?)?",
                    re.IGNORECASE,
                )

                # Buscar la primera coincidencia en el texto
                filtro_hb_1 = patron.search(text)

                if filtro_hb_1:
                    # Obtener el texto después de "hb" o "hemoglobina"
                    texto_filtrado = filtro_hb_1.group(0).strip()

                    # Obtener la información numérica inmediatamente después
                    info_numerica = filtro_hb_1.group(2)

                    if info_numerica:
                        data["Hemoglobina"].append(info_numerica)
                        break
            if not data.get("Peso"):
                patron_peso = re.compile(
                    r"\b(\d+(\.\d+)?)\s*(kg|kilogramos|lb|libras|g|gramos)\b",
                    re.IGNORECASE,
                )

                coincidencias_peso = patron_peso.findall(text)

                for peso, _, unidad in coincidencias_peso:
                    peso_resultado = f"{peso.replace('.', ',')} {unidad}"
                    data["Peso"].append(peso_resultado)
        keywords_to_search = [
            "FTLC",
            "F75",
            "Pediasure",
            "Infatrini",
            "Leche de Vaca",
            "Ácido Fólico",
            "Cita",
            "Carnet de vacunación",
            "Prueba de apetito",
        ]

        for pagina_com in range(num_paginas):
            texto_pagina = pdf_reader.pages[pagina_com]
            text = texto_pagina.extract_text()
            lines = text.split("\n")

            for keyword in keywords_to_search:
                keyword_expression = re.escape(keyword)
                keyword_pattern = re.compile(
                    rf"\b{keyword_expression}\b[.,]?", re.IGNORECASE
                )

                for i, line in enumerate(lines, start=1):
                    keyword_match = re.search(keyword_pattern, line)
                    if keyword_match:
                        if not data.get(keyword):
                            data[keyword] = ["SI"]
                            result_label = tk.Label(root, text="")
                            result_label.config(
                                text=f"Palabra clave '{keyword}' encontrada en el siguiente frase '{line}' dentro de la página {pagina_com + 1}"
                            )
                            labels_list.append(result_label)
                            result_label.pack()
        for keyword in keywords_to_search:
            if not data.get(keyword):
                result_label = tk.Label(root, text="")
                result_label.config(text=f"Palabra clave '{keyword}' no encontrada")
                labels_list.append(result_label)
                result_label.pack()

    for pagina_com in range(num_paginas):
        texto_pagina = pdf_reader.pages[pagina_com].extract_text()

        # Busca la palabra "Talla"
        filtro_talla = re.search(r"Talla", texto_pagina)
        if filtro_talla:
            talla_pos = filtro_talla.start()

            # Busca el primer número después de "Talla"
            numero_match = re.search(r"\d+(?:\.|,)\d+?", texto_pagina[talla_pos:])
            if numero_match:
                numero_extraido = numero_match.group(0)
                data["Talla"].append(numero_extraido)
                print(data.get("Talla"))
                break
    if not data.get("Talla"):
        data["Talla"].append("No encontrado")
        result_label = tk.Label(root, text="")
        result_label.config(text="Palabra clave 'Talla' no encontrada")
        labels_list.append(result_label)
        result_label.pack()

    for pagina_com in range(num_paginas):
        texto_pagina = pdf_reader.pages[pagina_com].extract_text()
        peri_expresion = r"perimetro del brazo"
        peri_patron = re.compile(peri_expresion, re.IGNORECASE)
        filtro_talla = re.search(peri_patron, texto_pagina)
        if filtro_talla:
            print(filtro_talla)
            talla_pos = filtro_talla.start()

            # Busca el primer número después de "Talla"
            numero_match = re.search(r"\d+(?:\.|,)\d+?", texto_pagina[talla_pos:])
            if numero_match:
                numero_extraido = numero_match.group(0)
                # data["Perimetro del brazo"].append(numero_extraido)
                print(numero_extraido)

    if not data.get("Perimetro del brazo"):
        data["Perimetro del brazo"].append("No encontrado")
        result_label = tk.Label(root, text="")
        result_label.config(text="Palabra clave 'Perimetro del brazo' no encontrada")
        labels_list.append(result_label)
        result_label.pack()
    if data.get("Albendazol") == ["SI"] or data.get("Amoxicilina") == ["SI"]:
        data["Antiparasitario"].append("SI")
    else:
        data["Antiparasitario"].append("NO")

    for key, value in data.items():
        if not value:
            data[key] = ["No encontrado"]
    print(data)
    dataframe = pd.DataFrame(data)

    result_label.pack()

    # Escribe el resultado en la ventana

    # Solicita el nombre del archivo
    nombre_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx")

    # Escribe el DataFrame en el archivo Excel
    parar_barra()
    try:
        dataframe.to_excel(nombre_archivo)
    except PermissionError as e:
        fuente_personalizada = "Arial", 14, "bold"
        result_label = tk.Label(root, text="", font=fuente_personalizada)
        result_label.config(text="Cerrar excel para actualizar archivo")
        labels_list.append(result_label)
        result_label.pack()


boton_abrir = tk.Button(root, text="Abrir archivo")
boton_abrir.bind("<Button-1>", threading_init)
boton_abrir.pack()

root.mainloop()


def is_empty(array):
    return len(array) == 0
