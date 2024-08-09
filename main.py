
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, ValidationError
import pdfplumber
import os
import json
import pytesseract
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
app = FastAPI()

# Initialize Gemini 1.5 Model
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

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
    image = Image.open(file.file)
    text = pytesseract.image_to_string(image)
    return text

async def extract_invoice_data_gemini(text: str) -> InvoiceData:
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
        "    \"customer_name\": string,\n"
        "    \"customer_address\": string,\n"
        "    \"customer_email\": string,\n"
        "    \"products\": [{ \"name\": string, \"quantity\": int, \"price\": float }],\n"
        "    \"total_amount\": float\n"
        "}"
    )

    response = model.generate_content(prompt)
    raw_invoice_data = response.text.strip()

    # Sanitize the response text
    sanitized_data = raw_invoice_data.replace("'", "\"").strip("```json").strip("```").strip()

    try:
        invoice_data = json.loads(sanitized_data)
        return InvoiceData(**invoice_data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {e}")

@app.post("/extract_invoice")
async def extract_invoice(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF or image file.")

    try:
        if file.content_type == "application/pdf":
            pdf_text = await extract_text_from_pdf(file)
        else:
            pdf_text = await extract_text_from_image(file)

        invoice_data = await extract_invoice_data_gemini(pdf_text)
        return invoice_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
