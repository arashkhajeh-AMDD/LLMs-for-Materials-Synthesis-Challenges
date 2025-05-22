import os
import json
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Import the prompts
from prompts.challenge_categorization import CHALLENGE_COMBINED_PROMPT
from prompts.challenge_categorization import CHALLENGE_CATEGORY_IDENTIFICATION_PROMPT
from prompts.challenge_categorization import CHALLENGE_CATEGORIZATION_PROMPT
from prompts.solution_categorization import SOLUTION_COMBINED_PROMPT
from prompts.solution_categorization import SOLUTION_CATEGORY_IDENTIFICATION_PROMPT
from prompts.solution_categorization import SOLUTION_CATEGORIZATION_PROMPT

def evaluate_and_save_categorized_items(text_items, categorized_items, output_file_path):
    # Check missing items
    missing_items = []
    for item in text_items:
        found = False
        for category, items in categorized_items.items():
            if item in items:
                found = True
                break
        if not found:
            missing_items.append(item)
    print("Num. of missing items:", len(missing_items))
    print("Missing items:", missing_items)

    # Check for duplicates
    duplicates = {}
    for category, items in categorized_items.items():
        seen = set()
        for item in items:
            if item in seen:
                if category not in duplicates:
                    duplicates[category] = []
                duplicates[category].append(item)
            else:
                seen.add(item)
    print("Duplicates:", duplicates)

    # Write the categorized items to a JSON file if there are no missing or duplicated IDs
    if not missing_items and not duplicates:
        # raise an error if the file already exists
        if os.path.exists(output_file_path):
            raise FileExistsError(f"Output file {output_file_path} already exists. Please choose a different name or remove the existing file.")
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        # Write the categorized items to a JSON file
        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(categorized_items, f, indent=4)
    else:
        print("Not saving categorized items due to missing or duplicated IDs.")

def group_and_categorize_challenges(
                       challenge_texts: list,
                       challenge_stage: str = "synthesis",
                       prompt: str = CHALLENGE_COMBINED_PROMPT,
                       api_key: str = None,  
                       azure: bool = True, 
                       model_name: str = None, 
                       temp: float = 0, 
                       azure_api_version: str = None, 
                       azure_endpoint: str = None) -> json:
    """
    Categorize(cluster) extracted challenges into different categories(clusters).

    Parameters:
        challenges_text (list): List of challenges to categorize.
        api_key (str): OpenAI API key.
        azure (bool): Flag to indicate if Azure OpenAI service should be used.
        model_name (str, optional): The name of the Azure deployment or openai model name. Defaults to None.
        temp (float, optional): The temperature for the model. Defaults to 0.   
        azure_api_version (str, optional): The API version for Azure OpenAI service. Defaults to None.
        azure_endpoint (str, optional): The endpoint for Azure OpenAI service. Defaults to None.
        azure_api_version (str): The API version for Azure OpenAI service. Defaults to None.
        
    Returns:
        json: JSON object containing the the categorized challenges.
    """
    if not azure:
        llm = ChatOpenAI(model_name=model_name or os.getenv("OPENAI_MODEL_NAME"),  # Replace with your OpenAI model name
                         temperature=temp, 
                         openai_api_key=api_key or os.getenv("OPENAI_API_KEY"))
    else:
        llm = AzureChatOpenAI(
            azure_deployment=model_name or os.getenv("AZURE_MODEL_DEPLOYMENT_NAME"),  # Replace with your Azure deployment name
            api_version=azure_api_version or os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=temp or 0,
            openai_api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")  # Explicitly pass the endpoint
        )

    challenges_prompt = prompt.format(
        challenge_texts=challenge_texts,
        challenge_stage=challenge_stage
    )

    system_msg = SystemMessage(content="You are a helpful and precise materials scientist. ")
    response = llm.invoke([
    system_msg,
    HumanMessage(content=challenges_prompt)
    ])

    # Separate the JSON part of the response
    try:
        json_start = response.content.index("{")
        json_end = response.content.rindex("}") + 1
        json_str = response.content[json_start:json_end]
    except ValueError:
        raise ValueError("Failed to extract JSON from LLM response. Check the response format.")

    try:
        extracted_output = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {json_str}") from e

    return extracted_output

def identify_challenge_categories(
                       challenge_texts: list,
                       challenge_stage: str = "synthesis",
                       prompt: str = CHALLENGE_CATEGORY_IDENTIFICATION_PROMPT,
                       api_key: str = None,  
                       azure: bool = True, 
                       model_name: str = None, 
                       temp: float = 0, 
                       azure_api_version: str = None, 
                       azure_endpoint: str = None) -> json:
    """
    Make categories from list of challenges.

    Parameters:
        challenges_text (list): List of challenges to categorize.
        api_key (str): OpenAI API key.
        azure (bool): Flag to indicate if Azure OpenAI service should be used.
        model_name (str, optional): The name of the Azure deployment or openai model name. Defaults to None.
        temp (float, optional): The temperature for the model. Defaults to 0.   
        azure_api_version (str, optional): The API version for Azure OpenAI service. Defaults to None.
        azure_endpoint (str, optional): The endpoint for Azure OpenAI service. Defaults to None.
        azure_api_version (str): The API version for Azure OpenAI service. Defaults to None.
        
    Returns:
        json: JSON object containing the the categorized challenges.
    """
    if not azure:
        llm = ChatOpenAI(model_name=model_name or os.getenv("OPENAI_MODEL_NAME"),  # Replace with your OpenAI model name
                         temperature=temp, 
                         openai_api_key=api_key or os.getenv("OPENAI_API_KEY"))
    else:
        llm = AzureChatOpenAI(
            azure_deployment=model_name or os.getenv("AZURE_MODEL_DEPLOYMENT_NAME"),  # Replace with your Azure deployment name
            api_version=azure_api_version or os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=temp or 0,
            openai_api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")  # Explicitly pass the endpoint
        )

    challenges_prompt = prompt.format(
        challenge_texts=challenge_texts,
        challenge_stage=challenge_stage
    )
    # challenges_prompt = CHALLENGE_CATEGORIZATION_PROMPT.format(
    system_msg = SystemMessage(content="You are a helpful and precise materials scientist. ")
    response = llm.invoke([
    system_msg,
    HumanMessage(content=challenges_prompt)
    ])

    # Separate the JSON part of the response
    try:
        json_start = response.content.index("{")
        json_end = response.content.rindex("}") + 1
        json_str = response.content[json_start:json_end]
    except ValueError:
        raise ValueError("Failed to extract JSON from LLM response. Check the response format.")

    try:
        extracted_output = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {json_str}") from e

    return extracted_output

def categorize_challenges(
                       challenge_texts: list,
                       challenge_stage: str = "synthesis",
                       prompt: str = CHALLENGE_CATEGORIZATION_PROMPT,
                       challenge_categories: list = None,
                       api_key: str = None,  
                       azure: bool = True, 
                       model_name: str = None, 
                       temp: float = 0, 
                       azure_api_version: str = None, 
                       azure_endpoint: str = None) -> json:
    """
    Categorize extracted challenges into different categories.

    Parameters:
        challenges_text (list): List of challenges to categorize.
        challenge_stage (str): The stage of the challenges (e.g., "synthesis", "characterization").
        challenge_categories (list): List of categories to use for categorization.
        api_key (str): OpenAI API key.
        azure (bool): Flag to indicate if Azure OpenAI service should be used.
        model_name (str, optional): The name of the Azure deployment or openai model name. Defaults to None.
        temp (float, optional): The temperature for the model. Defaults to 0.   
        azure_api_version (str, optional): The API version for Azure OpenAI service. Defaults to None.
        azure_endpoint (str, optional): The endpoint for Azure OpenAI service. Defaults to None.
        azure_api_version (str): The API version for Azure OpenAI service. Defaults to None.
        
    Returns:
        json: JSON object containing the the categorized challenges.
    """
    if not azure:
        llm = ChatOpenAI(model_name=model_name or os.getenv("OPENAI_MODEL_NAME"),  # Replace with your OpenAI model name
                         temperature=temp, 
                         openai_api_key=api_key or os.getenv("OPENAI_API_KEY"))
    else:
        llm = AzureChatOpenAI(
            azure_deployment=model_name or os.getenv("AZURE_MODEL_DEPLOYMENT_NAME"),  # Replace with your Azure deployment name
            api_version=azure_api_version or os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=temp or 0,
            openai_api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")  # Explicitly pass the endpoint
        )

    challenges_prompt = prompt.format(
        challenge_texts=challenge_texts,
        challenge_stage=challenge_stage,
        challenge_categories=challenge_categories
    )
    system_msg = SystemMessage(content="You are a helpful and precise materials scientist. ")
    response = llm.invoke([
    system_msg,
    HumanMessage(content=challenges_prompt)
    ])

    try:
        json_start = response.content.index("{")
        json_end = response.content.rindex("}") + 1
        json_str = response.content[json_start:json_end]
    except ValueError:
        raise ValueError("Failed to extract JSON from LLM response. Check the response format.")

    try:
        extracted_output = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {json_str}") from e

    return extracted_output

def group_and_categorize_solutions(
                       solution_texts: list,
                       challenge_stage: str = "synthesis",
                       prompt: str = SOLUTION_COMBINED_PROMPT,
                       api_key: str = None,  
                       azure: bool = True, 
                       model_name: str = None, 
                       temp: float = 0, 
                       azure_api_version: str = None, 
                       azure_endpoint: str = None) -> json:
    """
    Categorize extracted solutions into different categories.

    Parameters:
        solution_texts (list): List of solutions to categorize.
        api_key (str): OpenAI API key.
        azure (bool): Flag to indicate if Azure OpenAI service should be used.
        model_name (str, optional): The name of the Azure deployment or openai model name. Defaults to None.
        temp (float, optional): The temperature for the model. Defaults to 0.   
        azure_api_version (str, optional): The API version for Azure OpenAI service. Defaults to None.
        azure_endpoint (str, optional): The endpoint for Azure OpenAI service. Defaults to None.
        azure_api_version (str): The API version for Azure OpenAI service. Defaults to None.
        
    Returns:
        json: JSON object containing the the categorized solutions.
    """
    if not azure:
        llm = ChatOpenAI(model_name=model_name or os.getenv("OPENAI_MODEL_NAME"),  # Replace with your OpenAI model name
                         temperature=temp, 
                         openai_api_key=api_key or os.getenv("OPENAI_API_KEY"))
    else:
        llm = AzureChatOpenAI(
            azure_deployment=model_name or os.getenv("AZURE_MODEL_DEPLOYMENT_NAME"),  # Replace with your Azure deployment name
            api_version=azure_api_version or os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=temp or 0,
            openai_api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")  # Explicitly pass the endpoint
        )

    solution_prompt = prompt.format(
        solution_texts=solution_texts,
        challenge_stage=challenge_stage
    )
    system_msg = SystemMessage(content="You are a helpful and precise materials scientist. ")
    response = llm.invoke([
    system_msg,
    HumanMessage(content=solution_prompt)
    ])

    # Separate the JSON part of the response
    try:
        json_start = response.content.index("{")
        json_end = response.content.rindex("}") + 1
        json_str = response.content[json_start:json_end]
    except ValueError:
        raise ValueError("Failed to extract JSON from LLM response. Check the response format.")

    try:
        extracted_output = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {json_str}") from e

    return extracted_output

def identify_solution_categories(
                       solution_texts: list,
                       challenge_stage: str = "synthesis",
                       prompt: str = SOLUTION_CATEGORY_IDENTIFICATION_PROMPT,
                       api_key: str = None,  
                       azure: bool = True, 
                       model_name: str = None, 
                       temp: float = 0, 
                       azure_api_version: str = None, 
                       azure_endpoint: str = None) -> json:
    """
    Make categories from list of solutions.

    Parameters:
        solutions_text (list): List of solutions to categorize.
        api_key (str): OpenAI API key.
        azure (bool): Flag to indicate if Azure OpenAI service should be used.
        model_name (str, optional): The name of the Azure deployment or openai model name. Defaults to None.
        temp (float, optional): The temperature for the model. Defaults to 0.   
        azure_api_version (str, optional): The API version for Azure OpenAI service. Defaults to None.
        azure_endpoint (str, optional): The endpoint for Azure OpenAI service. Defaults to None.
        azure_api_version (str): The API version for Azure OpenAI service. Defaults to None.
        
    Returns:
        json: JSON object containing the the categorized solutions.
    """
    if not azure:
        llm = ChatOpenAI(model_name=model_name or os.getenv("OPENAI_MODEL_NAME"),  # Replace with your OpenAI model name
                         temperature=temp, 
                         openai_api_key=api_key or os.getenv("OPENAI_API_KEY"))
    else:
        llm = AzureChatOpenAI(
            azure_deployment=model_name or os.getenv("AZURE_MODEL_DEPLOYMENT_NAME"),  # Replace with your Azure deployment name
            api_version=azure_api_version or os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=temp or 0,
            openai_api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")  # Explicitly pass the endpoint
        )

    solutions_prompt = prompt.format(
        solution_texts=solution_texts,
        challenge_stage=challenge_stage
    )
    # solutions_prompt = SOLUTION_CATEGORIZATION_PROMPT.format(
    system_msg = SystemMessage(content="You are a helpful and precise materials scientist. ")
    response = llm.invoke([
    system_msg,
    HumanMessage(content=solutions_prompt)
    ])

    # Separate the JSON part of the response
    try:
        json_start = response.content.index("{")
        json_end = response.content.rindex("}") + 1
        json_str = response.content[json_start:json_end]
    except ValueError:
        raise ValueError("Failed to extract JSON from LLM response. Check the response format.")

    try:
        extracted_output = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {json_str}") from e

    return extracted_output

def categorize_solutions(
                       solution_texts: list,
                       challenge_stage: str = "synthesis",
                       prompt: str = SOLUTION_CATEGORIZATION_PROMPT,
                       solution_categories: list = None,
                       api_key: str = None,  
                       azure: bool = True, 
                       model_name: str = None, 
                       temp: float = 0, 
                       azure_api_version: str = None, 
                       azure_endpoint: str = None) -> json:
    """
    Categorize extracted solutions into different categories.

    Parameters:
        solutions_text (list): List of solutions to categorize.
        challenge_stage (str): The stage of the challenges (e.g., "synthesis", "characterization").
        solution_categories (list): List of categories to use for categorization.
        api_key (str): OpenAI API key.
        azure (bool): Flag to indicate if Azure OpenAI service should be used.
        model_name (str, optional): The name of the Azure deployment or openai model name. Defaults to None.
        temp (float, optional): The temperature for the model. Defaults to 0.   
        azure_api_version (str, optional): The API version for Azure OpenAI service. Defaults to None.
        azure_endpoint (str, optional): The endpoint for Azure OpenAI service. Defaults to None.
        azure_api_version (str): The API version for Azure OpenAI service. Defaults to None.
        
    Returns:
        json: JSON object containing the the categorized challenges.
    """
    if not azure:
        llm = ChatOpenAI(model_name=model_name or os.getenv("OPENAI_MODEL_NAME"),  # Replace with your OpenAI model name
                         temperature=temp, 
                         openai_api_key=api_key or os.getenv("OPENAI_API_KEY"))
    else:
        llm = AzureChatOpenAI(
            azure_deployment=model_name or os.getenv("AZURE_MODEL_DEPLOYMENT_NAME"),  # Replace with your Azure deployment name
            api_version=azure_api_version or os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=temp or 0,
            openai_api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")  # Explicitly pass the endpoint
        )

    solutions_prompt = prompt.format(
        solution_texts=solution_texts,
        challenge_stage=challenge_stage,
        solution_categories=solution_categories
    )
    system_msg = SystemMessage(content="You are a helpful and precise materials scientist. ")
    response = llm.invoke([
    system_msg,
    HumanMessage(content=solutions_prompt)
    ])

    # Separate the JSON part of the response
    try:
        json_start = response.content.index("{")
        json_end = response.content.rindex("}") + 1
        json_str = response.content[json_start:json_end]
    except ValueError:
        raise ValueError("Failed to extract JSON from LLM response. Check the response format.")

    try:
        extracted_output = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {json_str}") from e

    return extracted_output

