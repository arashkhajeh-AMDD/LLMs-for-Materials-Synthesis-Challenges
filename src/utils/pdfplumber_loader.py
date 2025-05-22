import os
import pdfplumber
import re
import unicodedata

def clean_text(text):
    # Normalize Unicode (e.g., ligatures, accented characters)
    text = unicodedata.normalize("NFKC", text)

    # Merge hyphenated line breaks (e.g., "electro-\nchemical" → "electrochemical")
    text = re.sub(r"-\s+", "", text)

    # Remove newlines and normalize whitespace
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    # Final cleanup
    text = re.sub(r"\s+", " ", text).strip()

    return text

class PDFPlumberLoader:
    def __init__(self, directory: str):
        self.directory = directory

    def load_pdfs(self):
        pdf_texts = []
        for filename in os.listdir(self.directory):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.directory, filename)
                with pdfplumber.open(file_path) as pdf:
                    text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
                    text = clean_text(text)
                    pdf_texts.append(text)
        return pdf_texts

    def load_a_pdf(self, file_name: str):
        file_path = os.path.join(self.directory, file_name)
        with pdfplumber.open(file_path) as pdf:
            text = " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
            text = clean_text(text)
        return text

    def find_in_doc(self, text: str, search_terms: list[str]) -> bool:
        """
        Search for terms in the text and return True if any are found.
        """
        return any(
            search_term.lower() in text.lower()
            for search_term in search_terms
        )

    def truncate_text(self, text:str, keywords: list[str]) -> str:
        """
        Truncate the text to the first occurrence of any keyword.
        """
        # find the last indecies of each keywords occurrence
        indeces = []
        for keyword in keywords:
            index = text.lower().rfind(keyword.lower())
            if index != -1:
                indeces.append(index + len(keyword))
        # if indeces is not empty, return the text up to the first occurrence of any keyword
        # otherwise, return the original text
        if indeces:
            return text[:min(indeces)]
        return text
    

# # # Example usage:
# from pyprojroot import here

# if __name__ == "__main__":
#     data_dir = here("data/papers/Li-Mn-O")
#     file_name = "1-s2.0-002236976690045X-main.pdf"  # Replace with your PDF file name
#     pdf_loader = PDFPlumberLoader(data_dir)
#     pdf_texts = pdf_loader.load_a_pdf(file_name)
#     print(f"Text from PDF:\n{pdf_texts[:200]}\n")

#     print("Finding terms in the document:")
#     search_terms = ["References", "Acknowledgements", "Acknowledgment"]
#     found = pdf_loader.find_in_doc(pdf_texts, search_terms)
#     print(f"Found terms: {found}")