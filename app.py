from flask import Flask, request, jsonify, send_from_directory, render_template
from qa_model import answer_question
from extract_text import extract_text_from_pdf
import os

app = Flask(__name__)

# Ruta al archivo PDF
pdf_path = "documento.pdf"

# Función para cargar y procesar el PDF
def load_pdf():
    global sections, images
    sections, images = extract_text_from_pdf(pdf_path)

# Cargar el contenido del PDF al iniciar la aplicación
load_pdf()

keywords = [
    "ingreso", "sistema", "documento", "herramienta", "solicitudes", "capítulo", 
    "introducción", "trámite", "requisitos", "pasos", "gestión", "ventas", "cliente", 
    "servicio", "proceso", "metodología", "solicitud", "aprobación", "análisis", "evaluación",
    "contraseña", "datos", "vinculación", "actividad económica", "centro de ayuda", "consulta", 
    "cliente listo", "cliente debe actualizar", "cliente necesita más información"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def answer():
    data = request.get_json()
    question = data.get('question')
    
    # Detectar si la pregunta es específica del documento
    if any(keyword in question.lower() for keyword in keywords):
        answer, related_images = answer_question(question, sections, images)
    else:
        answer = "Lo siento, solo puedo responder preguntas relacionadas con el documento."
        related_images = []

    response = {
        'answer': answer,
        'images': related_images
    }
    return jsonify(response)

@app.route('/reload', methods=['POST'])
def reload():
    load_pdf()
    return jsonify({"status": "PDF recargado y procesado"})

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(debug=True)
