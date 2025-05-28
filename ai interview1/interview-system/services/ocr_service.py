import pytesseract
import PyPDF2
import io
import os
from PIL import Image
import logging
from pdf2image import convert_from_path
import tempfile

class OCRService:
    def __init__(self):
        """
        Initialize OCR Service with configuration settings.
        """
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # For Windows: Uncomment and set the correct path to tesseract.exe
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def extract_text_from_pdf(self, pdf_file):
        """
        Extract text from a PDF file using both PDF text extraction and OCR.
        
        Args:
            pdf_file: File object of the uploaded PDF
            
        Returns:
            str: Extracted text from the PDF
        """
        try:
            # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
                pdf_file.save(temp_pdf.name)
                temp_pdf_path = temp_pdf.name

            extracted_text = []

            # Try PyPDF2 first for text extraction
            with open(temp_pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    # Try to extract text directly
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()

                    # If no text is extracted, try OCR
                    if not text.strip():
                        # Convert PDF to images
                        images = convert_from_path(temp_pdf_path, first_page=page_num+1, last_page=page_num+1)
                        
                        for image in images:
                            # Perform OCR on the image
                            text = pytesseract.image_to_string(image, lang='eng')
                            if text.strip():
                                break

                    extracted_text.append(text)

            # Clean up temporary file
            os.unlink(temp_pdf_path)

            # Combine all extracted text
            final_text = '\n'.join(extracted_text)
            
            # Basic text cleaning
            final_text = self._clean_text(final_text)
            
            self.logger.info(f"Successfully extracted text from PDF: {len(final_text)} characters")
            return final_text

        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {str(e)}")
            raise OCRException(f"Failed to extract text from PDF: {str(e)}")

    def extract_text_from_image(self, image_file):
        """
        Extract text from an image file using OCR.
        """
        try:
            image = Image.open(image_file)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            text = pytesseract.image_to_string(image, lang='eng')
            text = self._clean_text(text)
            
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text from image: {str(e)}")
            raise OCRException(f"Failed to extract text from image: {str(e)}")

    def _clean_text(self, text):
        """
        Clean the extracted text.
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        cleaned = ' '.join(text.split())
        
        # Remove non-printable characters
        cleaned = ''.join(char for char in cleaned if char.isprintable())
        
        return cleaned

    def validate_file(self, file):
        """
        Validate the uploaded file.
        """
        if not file:
            raise OCRException("No file provided")

        filename = file.filename.lower()
        allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
        file_ext = os.path.splitext(filename)[1]
        
        if file_ext not in allowed_extensions:
            raise OCRException(f"Unsupported file format. Allowed formats: {', '.join(allowed_extensions)}")

        # Check file size (max 10MB)
        if file.content_length > 10 * 1024 * 1024:
            raise OCRException("File size too large. Maximum size is 10MB")

        return True

class OCRException(Exception):
    """Custom exception for OCR-related errors"""
    pass