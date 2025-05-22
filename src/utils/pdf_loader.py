import os
from langchain_community.document_loaders import PyPDFLoader
import re
import unicodedata

import re
import unicodedata


import re
import unicodedata

# def clean_text(text):
#     import unicodedata
#     import re

#     # Normalize Unicode (e.g., ligatures, accented characters)
#     text = unicodedata.normalize("NFKC", text)

#     # Merge hyphenated line breaks (e.g., "electro-\nchemical" → "electrochemical")
#     text = re.sub(r"-\s+", "", text)

#     # Remove newlines and normalize whitespace
#     text = text.replace("\n", " ")
#     text = re.sub(r"\s+", " ", text)

#     # Fix common ligatures that NFKC might miss
#     ligature_fixes = {
#         "ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl",
#         "ﬅ": "ft", "ﬆ": "st"
#     }
#     for bad, good in ligature_fixes.items():
#         text = text.replace(bad, good)

#     # Fix common stuck-together scientific terms and layout issues
#     stuck_fixes = {
#         "theflakes": "the flakes",
#         "overflakes": "over flakes",
#         "offlakes": "of flakes",
#         "thefinal": "the final",
#         "byoperando": "by operando",
#         "andin situ": "and in situ",
#         "in situelectrochemical": "in situ electrochemical",
#         "Na xMO2": "NaxMO2",
#         "Na xMnO2": "NaxMnO2",
#         "theflake": "the flake",
#         "theflakes": "the flakes",
#         "the spheresover": "the spheres over",
#         "Cycling StabilityNicolas": "Cycling Stability. Nicolas",
#     }
#     for bad, good in stuck_fixes.items():
#         text = text.replace(bad, good)

#     # Fix spacing in scientific expressions
#     text = re.sub(r"MO\s*6", "MO6 ", text)
#     text = re.sub(r"m\s*2", "m²", text)  # You can change this to m^2 if preferred
#     text = re.sub(r"g-1", "g⁻¹", text)

#     # Clean up common publisher headers and footers
#     text = re.sub(r"Received:.*?Published:.*?Article pubs\.acs\.org/cm", "", text)
#     text = re.sub(r"© \d{4} American Chemical Society.*?(\s|$)", " ", text)
#     text = re.sub(r"10\.1021/acs\.chemmater\..*?(\s|$)", " ", text)
#     text = re.sub(r"Downloaded via.*?legitimately share published articles\.", "", text)

#     # Fix corrupted minus signs and voltage/capacity ranges
#     text = text.replace("−", "-").replace("–", "-")
#     text = re.sub(r"(\d)\s*-\s*(\d)", r"\1–\2", text)  # Use en dash for number ranges

#     # Remove stray commas/periods between numbers and units
#     text = re.sub(r"\s+([,\.])\s+", r"\1 ", text)

#     # Final cleanup
#     text = re.sub(r"\s+", " ", text).strip()

#     return text
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


class PDFLoader:
    """
    A class to load and extract text from PDF files in the specified directory using PyPDFLoader.
    
    Attributes:
        directory (str): The path to the directory containing PDF files.
    
    Methods:
        load_pdfs() -> List[str]:
            Loads all PDF files from the directory and extracts their text.
    """

    def __init__(self, directory: str):
        self.directory = directory

    def load_pdfs(self):
        """
        Loads all PDF files from the specified directory and extracts their text.

        Returns:
            List[str]: A list of extracted texts from each PDF file.
        """
        pdf_texts = []
        for filename in os.listdir(self.directory):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.directory, filename)
                loader = PyPDFLoader(file_path)
                documents = loader.load_and_split()
                text = "\n".join([doc.page_content for doc in documents])
                text = clean_text(text)  # Clean the extracted text
                pdf_texts.append(text)
        return pdf_texts
    
    def load_a_pdf(self, file_name: str):
        """
        Loads a single PDF file and extracts its text.

        Returns:
            An extracted texts from each PDF file.
        """
        pdf_texts = ''
        file_path = os.path.join(self.directory, file_name)
        loader = PyPDFLoader(file_path)
        documents = loader.load_and_split()
        text = "\n".join([doc.page_content for doc in documents])
        text = clean_text(text)
        pdf_texts += text
        return pdf_texts
    
    

# # # Example usage:
# from pyprojroot import here

# if __name__ == "__main__":
#     data_dir = here("data/papers")
#     pdf_loader = PDFLoader(data_dir)
#     pdf_texts = pdf_loader.load_pdfs()
#     for i, text in enumerate(pdf_texts):
#         print(f"Text from PDF {i+1}:\n{text}\n")

# # Example usage:
# from pyprojroot import here

# if __name__ == "__main__":
#     data_dir = here("data/papers")
#     pdf_loader = PDFLoader(data_dir)
#     file_name = 'paper_1.pdf'  # Replace with your PDF file name
#     pdf_texts = pdf_loader.load_a_pdf(file_name)
#     print(f"Text from PDF:\n{pdf_texts}\n")