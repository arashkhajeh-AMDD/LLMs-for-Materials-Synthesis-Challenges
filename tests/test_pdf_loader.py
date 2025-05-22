import unittest
from pyprojroot import here
from src.utils.pdf_loader import PDFLoader

class TestPDFLoader(unittest.TestCase):

    def test_load_pdfs(self):
        # Initialize PDFLoader
        data_dir = here("data/papers")
        pdf_loader = PDFLoader(data_dir)

        # Load all PDFs
        pdf_texts = pdf_loader.load_pdfs()

        # Assertions
        self.assertGreater(len(pdf_texts), 0, "No PDFs were loaded")
        for text in pdf_texts:
            self.assertIsInstance(text, str, "Loaded PDF content is not a string")
            self.assertNotEqual(text.strip(), "", "Loaded PDF content is empty")

    def test_load_a_pdf(self):
        # Initialize PDFLoader
        data_dir = here("data/papers")
        pdf_loader = PDFLoader(data_dir)

        # Load a single PDF
        file_name = 'paper_1.pdf'  # Replace with your PDF file name
        pdf_text = pdf_loader.load_a_pdf(file_name)

        # Assertions
        self.assertIsInstance(pdf_text, str, "Loaded PDF content is not a string")
        self.assertNotEqual(pdf_text.strip(), "", "Loaded PDF content is empty")

if __name__ == "__main__":
    unittest.main()
