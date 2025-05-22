import os
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import json

def optimize_synthesis_info_schema(api_key: str,
                                   synthesis_text: str,
                                   current_schema: dict,
                                   azure: bool = True, 
                                   model_name: str = None,
                                   temp: float = 0,
                                   azure_api_version: str = None,
                                   azure_endpoint: str = None) -> dict:
    """
    Use an LLM to iteratively optimize the schema for extracting synthesis information.

    Parameters:
        api_key (str): OpenAI API key.
        synthesis_text (str): The text containing synthesis process information.
        current_schema (dict): The current schema to be optimized.
        azure (bool): Flag to indicate if Azure OpenAI service should be used.
        model_name (str, optional): The name of the Azure deployment or OpenAI model name. Defaults to None.
        temp (float, optional): The temperature for the model. Defaults to 0.
        azure_api_version (str, optional): The API version for Azure OpenAI service. Defaults to None.
        azure_endpoint (str, optional): The endpoint for Azure OpenAI service. Defaults to None.

    Returns:
        dict: Optimized schema for synthesis extraction.
    """
    if not azure:
        llm = ChatOpenAI(model_name=model_name or os.getenv("OPENAI_MODEL_NAME"),
                         temperature=temp, 
                         openai_api_key=api_key or os.getenv("OPENAI_API_KEY"))
    else:
        llm = AzureChatOpenAI(
            azure_deployment=model_name or os.getenv("AZURE_MODEL_DEPLOYMENT_NAME"),
            api_version=azure_api_version or os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=temp or 0,
            openai_api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        )

    optimization_prompt = f"""
    You are a materials research assistant tasked with optimizing the schema for extracting synthesis information from scientific papers.

    The current schema for synthesis is:
    {json.dumps(current_schema, indent=4)}

    Based on the provided synthesis text, determine if the input schema can capture critical information or suggest improvements to make the schema more comprehensive and generalizable for materials science research. 
    Ensure the schema can contain all relevant details for synthesis experts and is adaptable to various materials listed in the paper.
    Only focus on the materials information and synthesis part of the schema, and ignore other parts such as characterization, performance, etc, which are not relevant to synthesis and synthesized materials info.
    Schema should be generalizable to various materials and synthesis steps; DO NOT INCLUDE ANY VALUE OR DETAIL ABOUT THE SYNTHESIS PROCESS.
    ### Input:
    {synthesis_text}

    ### Output:
    Return only the optimized schema as a JSON object with the following structure:
    {{
      "optimized_schema": "<optimized schema JSON>",
      "improvements": "<description of improvements made during the optimization process numbered and formatted for easy reading>",
      "improvement_score": "<percentage of improvement based on the original schema (integer)>"
    }}

    """

    system_msg = SystemMessage(content="You are a materials research assistant specializing in schema optimization.")
    response = llm.invoke([
        system_msg,
        HumanMessage(content=optimization_prompt)
    ])

    # Handle empty or invalid responses
    if not response.content.strip():
        raise ValueError("LLM returned an empty response. Check the input prompt or LLM configuration.")

    # Separate the JSON part of the response
    try:
        json_start = response.content.index("{")
        json_end = response.content.rindex("}") + 1
        json_str = response.content[json_start:json_end]
    except ValueError:
        raise ValueError("Failed to extract JSON from LLM response. Check the response format.")
    
    try:
        extracted_schema = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {json_str}") from e
    return extracted_schema


def optimize_challenges_info_schema(api_key: str,
                                synthesis_text: str,
                                current_schema: dict,
                                azure: bool = True, 
                                model_name: str = None,
                                temp: float = 0,
                                azure_api_version: str = None,
                                azure_endpoint: str = None) -> dict:
    """
    Use an LLM to iteratively optimize the schema for challenges information.

    Parameters:
        api_key (str): OpenAI API key.
        synthesis_text (str): The text containing challenges in synthesis, characterization, testing, post-processing, and application.
        azure (bool): Flag to indicate if Azure OpenAI service should be used.
        model_name (str, optional): The name of the Azure deployment or OpenAI model name. Defaults to None.
        temp (float, optional): The temperature for the model. Defaults to 0.
        azure_api_version (str, optional): The API version for Azure OpenAI service. Defaults to None.
        azure_endpoint (str, optional): The endpoint for Azure OpenAI service. Defaults to None.

    Returns:
        dict: Optimized schema for challenges extraction.
    """
    if not azure:
        llm = ChatOpenAI(model_name=model_name or os.getenv("OPENAI_MODEL_NAME"),
                         temperature=temp, 
                         openai_api_key=api_key or os.getenv("OPENAI_API_KEY"))
    else:
        llm = AzureChatOpenAI(
            azure_deployment=model_name or os.getenv("AZURE_MODEL_DEPLOYMENT_NAME"),
            api_version=azure_api_version or os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=temp or 0,
            openai_api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        )

    optimization_prompt = f"""
    You are a materials research assistant tasked with optimizing the schema for extracting
    challenges and solutions researchers have encountered during synthesis, characterization, testing, post-processing, and application from scientific papers.
    The current schema for challenges is:
    
    {json.dumps(current_schema, indent=4)}

    Schema should be generalizable to various materials and should not include specific details about the synthesis process.

    Based on the provided synthesis text, determine if the input schema can capture critical information or suggest improvements to make the schema more comprehensive and generalizable for materials science research.
    Ensure the schema captures all relevant details for synthesis experts and is adaptable to various materials in the input text.

    ### Input:
    {synthesis_text}

    ### Output:
    Return only the optimized schema as a JSON object with the following structure:
    {{
      "optimized_schema": "<optimized schema JSON>",
      "improvements": "<description of improvements made during the optimization process numbered and formatted for easy reading>",
      "improvement_score": "<percentage of improvement based on the original schema (integer)>"
    }}

    """

    system_msg = SystemMessage(content="You are a materials research assistant specializing in schema optimization.")
    response = llm.invoke([
        system_msg,
        HumanMessage(content=optimization_prompt)
    ])


    # Handle empty or invalid responses
    if not response.content.strip():
        raise ValueError("LLM returned an empty response. Check the input prompt or LLM configuration.")

    # Separate the JSON part of the response
    try:
        json_start = response.content.index("{")
        json_end = response.content.rindex("}") + 1
        json_str = response.content[json_start:json_end]
    except ValueError:
        raise ValueError("Failed to extract JSON from LLM response. Check the response format.")
    
    try:
        extracted_schema = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {json_str}") from e
    return extracted_schema


# Syntheis info initial schema
# {{
#       "material": "<exact formula or name as presented in the paper>",
#       "synthesis_steps": [{{
#         {{
#           "step": 1,
#           "label": "<Short title of the step, e.g., 'Precursor Mixing'>",
#           "details": {{
#             "reagents": ["<chemical names>"],
#             "temperature": "<value or null>",
#             "duration": "<value or null>"
#           }}
#         }}
#       }}]
#     }}

# Challenges info initial schema
# {{
#         "material": "<exact formula or name as presented in the paper>",
#         "stage": "<eg. synthesis, characterization, testing, post-processing, application>",
#         "challenge": "<description of the specific problem the authors encountered in a concise way.>",
#         "impact": "<explanation of why this problem matters — what negative effect it has.>",
#         "solution": "<a summary of how the authors addressed or solved this challenge>",
#         "evidence": "<Quote where in the paper this information is discussed (e.g., page numbers, figures, tables, or sections).>"
#       }}  

# # Add the root of the project (where `src/` lives) to sys.path
# import sys
# from pyprojroot import here
# sys.path.append(str(here()))
# import dotenv
# import os
# # Load environment variables from .env file
# dotenv.load_dotenv()

# # Set the API keys
# azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
# print(f"AZURE_OPENAI_API_KEY: {azure_openai_api_key[:4]}...")
# if not azure_openai_api_key:
#     raise ValueError("AZURE_OPENAI_API_KEY environment variable not set.")
                           
# azure_deployment=os.getenv("AZURE_MODEL_DEPLOYMENT_NAME")
# azue_api_version=os.getenv("AZURE_OPENAI_API_VERSION")
# azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")

# from src.utils.pymupdf_loader import PyMuPDFLoader
# data_dir = here("data/papers/Na-Mn-O")
# pdf_loader = PyMuPDFLoader(data_dir)
# file_name = "000690060.pdf"
# pdf_text = pdf_loader.load_a_pdf(file_name)

# synthesis_text = '''{text}'''.format(text="\n".join(pdf_text))

# optimized_synthesis_schema= optimize_synthesis_info_schema(
#     api_key=azure_openai_api_key,
#     synthesis_text=synthesis_text,
#     azure=True,
#     model_name=azure_deployment,
#     temp=0,
#     azure_api_version=azue_api_version,
#     azure_endpoint=azure_endpoint
# )


# # Debugging: Print the optimized schema
# print("Optimized synthesis schema:", optimized_synthesis_schema)
# print("Type of optimized_schema:", type(optimized_synthesis_schema))

# # Ensure the synthesis schema is a dictionary
# if not isinstance(optimized_synthesis_schema, dict):
#     raise ValueError("Optimized synthesis schema is not a dictionary. Check the LLM response or parsing logic.")

# # Save the optimized schema to a JSON file
# output_dir = here("data/papers/Na-Mn-O")
# output_file = os.path.join(output_dir, "synthesis_schema.json")

# # Ensure the output directory exists
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# with open(output_file, "w", encoding="utf-8") as f:
#     json.dump(optimized_synthesis_schema, f, indent=4)

# print(f"Optimized schema saved to {output_file}")

# Extract challenges info from the pdf

# optimized_challenges_schema= optimize_challenges_info_schema(
#     api_key=azure_openai_api_key,
#     synthesis_text=synthesis_text,
#     azure=True,
#     model_name=azure_deployment,
#     temp=0,
#     azure_api_version=azue_api_version,
#     azure_endpoint=azure_endpoint
# )

# print("Optimized challenges schema:", optimized_challenges_schema)
# print("Type of optimized_schema:", type(optimized_challenges_schema))

# # Ensure the challenges schema is a dictionary
# if not isinstance(optimized_challenges_schema, dict):
#     raise ValueError("Optimized challenges schema is not a dictionary. Check the LLM response or parsing logic.")

# # Save the optimized schema to a JSON file
# output_dir = here("data/papers/Na-Mn-O")
# output_file = os.path.join(output_dir, "challenges_schema.json")

# # Ensure the output directory exists
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# with open(output_file, "w", encoding="utf-8") as f:
#     json.dump(optimized_challenges_schema, f, indent=4)

# print(f"Optimized schema saved to {output_file}")