# PDF Invoice Extractor

This project is a FastAPI application designed to extract invoice details from PDF files using OpenAI's language model. The application processes PDF files, extracts text, and then uses an LLM to parse the invoice information into a structured format.

## Features

- **Upload PDF Invoices**: Upload a PDF file containing invoice data.
- **Extract Invoice Details**: Extract customer details, products, and total amount from the invoice using GPT-4 (or other available models).
- **API Endpoint**: A POST endpoint to handle PDF uploads and data extraction.

## Prerequisites

- Python 3.8+
- OpenAI API key
- PDF files for testing

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/atul-007/extractor.git
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   - Create a `.env` file in the root directory of the project.
   - Add your OpenAI API key to the `.env` file:

     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

5. **Install Additional Dependencies**

   - Make sure to install `python-dotenv` for loading environment variables:

     ```bash
     pip install python-dotenv
     ```

## Usage

1. **Run the FastAPI Application**

   ```bash
   uvicorn main:app --reload
   ```

   The application will start and be available at `http://127.0.0.1:8000`.

2. **Send a Request**

   - **Using Postman**:
     - Method: POST
     - URL: `http://127.0.0.1:8000/extract_invoice`
     - Body: Form-data
       - Key: `file`
       - Type: File
       - Value: Select your PDF file

   - **Using cURL**:

     ```bash
     curl -X POST "http://127.0.0.1:8000/extract_invoice" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path_to_your_pdf_file.pdf"
     ```

   - **Using HTML Form**:

     Create a simple HTML form to upload a PDF and test the endpoint.



---

