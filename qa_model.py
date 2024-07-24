from transformers import pipeline

# Cargar el modelo de preguntas y respuestas en español
qa_pipeline = pipeline("question-answering", model="mrm8488/bert-base-spanish-wwm-cased-finetuned-spa-squad2-es")

def answer_question(question, sections, images):
    best_answer = None
    best_score = 0
    best_images = []

    for i, section in enumerate(sections):
        result = qa_pipeline(question=question, context=section)
        if result['score'] > best_score:
            best_answer = result['answer']
            best_score = result['score']
            best_images = images[i]

    return best_answer, best_images

if __name__ == "__main__":
    from extract_text import extract_text_from_pdf
    
    pdf_path = "documento.pdf"
    sections, images = extract_text_from_pdf(pdf_path)
    
    question = "¿Cómo ingreso al sistema?"
    answer, related_images = answer_question(question, sections, images)
    print(f"Respuesta: {answer}")
    print(f"Imágenes relacionadas: {related_images}")
