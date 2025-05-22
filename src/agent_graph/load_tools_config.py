
import os
import yaml
from dotenv import load_dotenv
from pyprojroot import here

load_dotenv()


class LoadToolsConfig:

    def __init__(self) -> None:
        with open(here("configs/tools_config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)

        # Set environment variables
        os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
        os.environ['TAVILY_API_KEY'] = os.getenv("TAVILY_API_KEY")

        # Primary agent
        self.primary_agent_llm = app_config["primary_agent"]["llm"]
        self.primary_agent_llm_temperature = app_config["primary_agent"]["llm_temperature"]

        # Internet Search config
        self.tavily_search_max_results = int(
            app_config["tavily_search_api"]["tavily_search_max_results"])

        # Table definitions RAG configs
        self.table_definitions_rag_llm = app_config["table_definitions_rag"]["llm"]
        self.table_definitions_rag_llm_temperature = float(
            app_config["table_definitions_rag"]["llm_temperature"])
        self.table_definitions_rag_embedding_model = app_config["table_definitions_rag"]["embedding_model"]
        self.table_definitions_rag_vectordb_directory = str(here(
            app_config["table_definitions_rag"]["vectordb"]))  # needs to be strin for summation in chromadb backend: self._settings.require("persist_directory") + "/chroma.sqlite3"
        self.table_definitions_rag_unstructured_docs_directory = str(here(
            app_config["table_definitions_rag"]["unstructured_docs"]))
        self.table_definitions_rag_k = app_config["table_definitions_rag"]["k"]
        self.table_definitions_rag_chunk_size = app_config["table_definitions_rag"]["chunk_size"]
        self.table_definitions_rag_chunk_overlap = app_config["table_definitions_rag"]["chunk_overlap"]
        self.table_definitions_rag_collection_name = app_config["table_definitions_rag"]["collection_name"]

        # Comments RAG configs
        self.comments_rag_llm = app_config["comments_rag"]["llm"]
        self.comments_rag_llm_temperature = float(
            app_config["comments_rag"]["llm_temperature"])
        self.comments_rag_embedding_model = app_config["comments_rag"]["embedding_model"]
        self.comments_rag_vectordb_directory = str(here(
            app_config["comments_rag"]["vectordb"]))  # needs to be strin for summation in chromadb backend: self._settings.require("persist_directory") + "/chroma.sqlite3"
        self.comments_rag_unstructured_docs_directory = str(here(
            app_config["comments_rag"]["unstructured_docs"]))
        self.comments_rag_k = app_config["comments_rag"]["k"]
        self.comments_rag_chunk_size = app_config["comments_rag"]["chunk_size"]
        self.comments_rag_chunk_overlap = app_config["comments_rag"]["chunk_overlap"]
        self.comments_rag_collection_name = app_config["comments_rag"]["collection_name"]

        # ICDD SQL Agent configs
        self.icdd_sqldb_directory = str(here(
            app_config["icdd_sqlagent_configs"]["icdd_sqldb_dir"]))
        self.icdd_sqlagent_llm = app_config["icdd_sqlagent_configs"]["llm"]
        self.icdd_sqlagent_llm_temperature = float(
            app_config["icdd_sqlagent_configs"]["llm_temperature"])


        # Graph configs
        self.thread_id = str(
            app_config["graph_configs"]["thread_id"])
