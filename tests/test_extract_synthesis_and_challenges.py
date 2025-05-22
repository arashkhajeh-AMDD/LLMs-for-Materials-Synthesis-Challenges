import unittest
from pyprojroot import here
from src.utils.extract_synthesis_and_challenges import extract_synthesis, extract_challenges
from src.utils.pdf_loader import PDFLoader
import dotenv
import os

class TestExtractSynthesisAndChallenges(unittest.TestCase):

    def test_extract_synthesis_and_challenges(self):
        # Load environment variables
        dotenv.load_dotenv()

        # Set the API keys
        azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.assertIsNotNone(azure_openai_api_key, "AZURE_OPENAI_API_KEY is not set")

        openai_api_key = os.getenv("OPENAI_API_KEY")
        self.assertIsNotNone(openai_api_key, "OPENAI_API_KEY is not set")

        azure_deployment = os.getenv("AZURE_MODEL_DEPLOYMENT_NAME")
        azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

        # Initialize PDFLoader
        data_dir = here("data/papers")
        pdf_loader = PDFLoader(data_dir)
        pdf_texts = pdf_loader.load_pdfs()

        # Ensure PDFs are loaded
        self.assertGreater(len(pdf_texts), 0, "No PDFs were loaded")
        self.assertIsInstance(pdf_texts[0], str, "Loaded PDF content is not a string")

        # Extract synthesis and challenges information
        synthesis_text = pdf_texts[0]

        synthesis_info = extract_synthesis(
            synthesis_text=synthesis_text,
            api_key=azure_openai_api_key,
            azure=True,
            model_name=azure_deployment,
            temp=0
        )

        challenges_info = extract_challenges(
            synthesis_text=synthesis_text,
            api_key=azure_openai_api_key,
            azure=True,
            model_name=azure_deployment,
            temp=0
        )

        # Ensure the outputs are not empty
        self.assertIsNotNone(synthesis_info, "Synthesis info is None")
        self.assertNotEqual(synthesis_info, "", "Synthesis info is empty")

        self.assertIsNotNone(challenges_info, "Challenges info is None")
        self.assertNotEqual(challenges_info, "", "Challenges info is empty")

if __name__ == "__main__":
    unittest.main()
