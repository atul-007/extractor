

# Invoice Data Extraction API

This FastAPI project allows you to extract invoice data from PDF and image files (JPEG/PNG) using the Gemini 1.5 model by Google and Tesseract OCR for text recognition from images.

## Table of Contents
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Example Usage](#example-usage)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Installation

### Prerequisites
- Python 3.8 or higher
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and added to your system's PATH

### Step 1: Clone the Repository
```bash
git clone https://github.com/atul-007/extractor/tree/gemini
```

### Step 2: Install Python Dependencies
Create a virtual environment and install the required Python packages:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### Step 3: Install Tesseract OCR
- **Linux (Debian/Ubuntu)**:
  ```bash
  sudo apt-get install tesseract-ocr
  ```
- **macOS** (using Homebrew):
  ```bash
  brew install tesseract
  ```
- **Windows**:
  - Download and install Tesseract from the [official repository](https://github.com/tesseract-ocr/tesseract).

### Step 4: Verify Tesseract Installation
Ensure Tesseract is correctly installed by running:
```bash
tesseract --version
```

## Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variable:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

You can obtain the `GEMINI_API_KEY` by signing up for Google Generative AI services.

## Running the Application

To start the FastAPI server, run:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

This will start the application on `http://0.0.0.0:8000`.

## API Endpoints

### `POST /extract_invoice`
This endpoint allows you to upload a PDF or image file (JPEG/PNG) and extracts the invoice data.

- **Request**:
  - `file`: The PDF or image file (JPEG/PNG) containing the invoice.

- **Response**:
  Returns the extracted invoice data in JSON format.
  
  ```json
  {
      "customer_name": "John Doe",
      "customer_address": "123 Main St, City, Country",
      "customer_email": "john.doe@example.com",
      "products": [
          {
              "name": "Product 1",
              "quantity": 2,
              "price": 99.99
          }
      ],
      "total_amount": 199.98
  }
  ```

## Example Usage

You can use `curl` or any API client like Postman to test the API:

```bash
curl -X POST "http://localhost:8000/extract_invoice" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/invoice.pdf"
```

## Troubleshooting

### Tesseract Not Installed or Not Found
If you encounter the error:

```json
{
    "detail": "Error processing file: tesseract is not installed or it's not in your PATH. See README file for more information."
}
```

Ensure that Tesseract is installed and accessible via the command line. Add the Tesseract installation path to your system's PATH environment variable if necessary.

### Invalid API Key
If the API returns an error related to the Gemini API, make sure your `GEMINI_API_KEY` is correct and that you have sufficient permissions.



---
