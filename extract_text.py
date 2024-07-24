import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import io
import os

# Configurar la ruta a tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\nicol\.conda\envs\chatbot_env\Library\bin\tesseract.exe'

# Configurar la variable de entorno TESSDATA_PREFIX directamente en el script
os.environ['TESSDATA_PREFIX'] = r'C:\Users\nicol\.conda\envs\chatbot_env\Library\share\tessdata'

def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    sections = []
    images = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text")

        page_images = []
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))

            # Use pytesseract to extract text from image
            image_text = pytesseract.image_to_string(image)
            text += f"\n\n[Imagen {img_index + 1}]\n\n{image_text}"  # Añadir marcador de imagen

            # Save the image if needed for other uses
            image_filename = f"image_{page_num+1}_{img_index+1}.png"
            image.save(image_filename)
            page_images.append(image_filename)

        sections.append(text)
        images.append(page_images)

    return sections, images

if __name__ == "__main__":
    pdf_path = "documento.pdf"
    pdf_sections, pdf_images = extract_text_from_pdf(pdf_path)
    for section in pdf_sections:
        print(section)  # Aquí puedes ver las secciones extraídas
