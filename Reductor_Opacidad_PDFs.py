import os
import tempfile
import customtkinter as ctk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def reduce_opacity(input_pdf_path, output_pdf_path, opacity):
    # Crear un archivo temporal para la capa de opacidad
    packet = tempfile.NamedTemporaryFile(delete=False)
    packet_name = packet.name
    packet.close()

    # Crear una capa transparente con ReportLab
    c = canvas.Canvas(packet_name, pagesize=A4)
    c.setFillAlpha(opacity)
    c.setFillColorRGB(1, 1, 1)  # Blanco
    c.rect(0, 0, A4[0], A4[1], fill=1)
    c.save()

    # Leer el PDF de entrada
    with open(input_pdf_path, "rb") as input_file:
        reader = PdfReader(input_file)
        writer = PdfWriter()

        # Leer la capa de opacidad
        with open(packet_name, "rb") as overlay_file:
            overlay_pdf = PdfReader(overlay_file)
            overlay_page = overlay_pdf.pages[0]

            # Aplicar la capa de opacidad a cada página
            for page_number in range(len(reader.pages)):
                page = reader.pages[page_number]
                page.merge_page(overlay_page)
                writer.add_page(page)

        # Escribir el PDF de salida
        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)

    # Eliminar el archivo temporal
    os.remove(packet_name)

def select_input_pdf():
    input_pdf = filedialog.askopenfilename(
        title="Selecciona el PDF de entrada",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if input_pdf:
        input_pdf_label.configure(text=f"PDF original: {os.path.basename(input_pdf)}")
        input_pdf_path.set(input_pdf)

def select_output_pdf():
    output_pdf = filedialog.asksaveasfilename(
        title="Guardar PDF con opacidad reducida",
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if output_pdf:
        output_pdf_label.configure(text=f"PDF modificado: {os.path.basename(output_pdf)}")
        output_pdf_path.set(output_pdf)

def process_pdf():
    input_pdf = input_pdf_path.get()
    output_pdf = output_pdf_path.get()
    opacity = opacity_slider.get() / 100  # Convertir a valor entre 0 y 1
    if input_pdf and output_pdf:
        reduce_opacity(input_pdf, output_pdf, opacity)
        result_label.configure(text=f"PDF guardado exitosamente en: {output_pdf}")
    else:
        result_label.configure(text="Por favor, seleccioná los archivos de entrada y salida.")

# Configuración de la ventana principal
ctk.set_appearance_mode("System")  # "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # Cambia el tema de colores

root = ctk.CTk()
root.title("Reductor de Opacidad de PDF")
root.geometry("1000x400")

# Variables de ruta de archivo
input_pdf_path = ctk.StringVar()
output_pdf_path = ctk.StringVar()

# Widgets
input_pdf_button = ctk.CTkButton(root, text="Seleccioná el PDF que quieras editar", command=select_input_pdf)
input_pdf_button.pack(pady=5)

input_pdf_label = ctk.CTkLabel(root, text="PDF original: Ninguno")
input_pdf_label.pack(pady=5)

output_pdf_button = ctk.CTkButton(root, text="Seleccioná Nombre del nuevo PDF", command=select_output_pdf)
output_pdf_button.pack(pady=5)

output_pdf_label = ctk.CTkLabel(root, text="PDF modificado: Ninguno")
output_pdf_label.pack(pady=5)

opacity_slider = ctk.CTkSlider(root, from_=0, to=100, number_of_steps=101)
opacity_slider.set(100)  # Valor inicial al 100%
opacity_slider.pack(pady=10)

opacity_label = ctk.CTkLabel(root, text="Dismunuir la opacidad: 100%")
opacity_label.pack(pady=5)

def update_opacity_label(value):
    opacity_label.configure(text=f"Dismunuir la opacidad: {int(value)}%")

opacity_slider.configure(command=update_opacity_label)

process_button = ctk.CTkButton(root, text="Procesar PDF", command=process_pdf)
process_button.pack(pady=20)

result_label = ctk.CTkLabel(root, text="Herramienta creada por Leonardo Sola.")
result_label.pack(pady=5)

root.mainloop()
