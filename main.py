
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pdfplumber
import pytesseract
from PIL import Image
import openai
import os
import io
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

# Pydantic models for validation
class Product(BaseModel):
    name: str
    quantity: int
    price: float

class InvoiceData(BaseModel):
    customer_name: str
    customer_address: str = None
    customer_email: str = None
    products: list[Product]
    total_amount: float

async def extract_text_from_pdf(file: UploadFile) -> str:
    with pdfplumber.open(file.file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

async def extract_text_from_image(file: UploadFile) -> str:
    image = Image.open(io.BytesIO(await file.read()))
    text = pytesseract.image_to_string(image)
    return text

async def extract_invoice_data(text: str) -> InvoiceData:
    prompt = (
        "Extract the following information from this invoice text:\n"
        "1. Customer Name\n"
        "2. Customer Address\n"
        "3. Customer Email\n"
        "4. List of Products with name, quantity, and price\n"
        "5. Total Amount\n\n"
        "Invoice Text:\n"
        f"{text}\n\n"
        "Respond with JSON format adhering to the following schema:\n"
        "{\n"
        "    'customer_name': string,\n"
        "    'customer_address': string,\n"
        "    'customer_email': string,\n"
        "    'products': [{ 'name': string, 'quantity': int, 'price': float }],\n"
        "    'total_amount': float\n"
        "}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    invoice_data = response['choices'][0]['message']['content']
    return InvoiceData.parse_raw(invoice_data)

@app.post("/extract_invoice")
async def extract_invoice(file: UploadFile = File(...)):
    if file.content_type == "application/pdf":
        pdf_text = await extract_text_from_pdf(file)
        invoice_data = await extract_invoice_data(pdf_text)
        return invoice_data

    elif file.content_type in ["image/png", "image/jpeg"]:
        image_text = await extract_text_from_image(file)
        invoice_data = await extract_invoice_data(image_text)
        return invoice_data

    else:
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF or an image file.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
