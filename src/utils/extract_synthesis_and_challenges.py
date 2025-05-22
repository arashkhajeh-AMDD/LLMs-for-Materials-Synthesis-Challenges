import os
import json
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

def extract_synthesis(api_key: str,
                      synthesis_text: str,
                      synthesis_output_schema: dict,
                      azure: bool = True, 
                      model_name: str=None,
                      temp: float=0,
                      azure_api_version: str=None,
                      azure_endpoint: str=None) -> str:
    """
    Extract synthesis procedure from a given text.

    Parameters:
        api_key (str): OpenAI API key.
        synthesis_text (str): The text containing synthesis information.
        azure (bool): Flag to indicate if Azure OpenAI service should be used.
        model_name (str, optional): The name of the Azure deployment or openai model name. Defaults to None.
        temp (float, optional): The temperature for the model. Defaults to 0.
        azure_api_version (str, optional): The API version for Azure OpenAI service. Defaults to None.
        azure_endpoint (str, optional): The endpoint for Azure OpenAI service. Defaults to None.
        
    Returns:
        List[Dict]: List of dictionaries containing the extracted synthesis procedure.
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

    synthesis_prompt = f"""
    You are a materials synthesis extraction assistant.

    Your task is to read the synthesis procedure from a scientific paper and extract the full synthesis process for **each distinct material synthesized**. If multiple materials are synthesized, return a list of JSON objects, one for each material.

    Only use information from the synthesis text provided in the Input section. If no synthesis information is present, return an empty list (`[]`).

    Each material's synthesis should be structured as follows:

    {synthesis_output_schema}

    ### Input:
    {synthesis_text}

    ### Output:
    Return ONLY the output as list of dictionaries List[Dict], corresponding to each material synthesized, and nothing else
    """
    # Create a system message to set the context for the assistant
    # and provide the synthesis prompt
    # The system message is used to set the behavior and role of the assistant
    # in the conversation. In this case, it is set to be a materials synthesis extraction assistant.
    # The HumanMessage is the actual prompt that contains the synthesis text and instructions for extraction.
    # The assistant will read the synthesis text and extract the synthesis procedure for each material.
    # The assistant is expected to return a list of JSON objects, each containing the material name and its synthesis steps.
    system_msg = SystemMessage(content="You are a materials synthesis extraction assistant.")
    
    response = llm.invoke([
    system_msg,
    HumanMessage(content=synthesis_prompt)
    ])

    # Separate the JSON part of the response
    try:
        json_start = response.content.index("[")
        json_end = response.content.rindex("]") + 1
        json_str = response.content[json_start:json_end]
    except ValueError:
        raise ValueError("Failed to extract JSON from LLM response. Check the response format.")

    try:
        extracted_output = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {json_str}") from e

    return extracted_output


def extract_challenges(
                       synthesis_text: str,
                       challenges_output_schema: dict,
                       api_key: str = None,  
                       azure: bool = True, 
                       model_name: str = None, 
                       temp: float = 0, 
                       azure_api_version: str = None, 
                       azure_endpoint: str = None) -> str:
    """
    Extract challenges information from a given text.

    Parameters:
        synthesis_text (str): The text containing challenges information.
        api_key (str): OpenAI API key.
        azure (bool): Flag to indicate if Azure OpenAI service should be used.
        model_name (str, optional): The name of the Azure deployment or openai model name. Defaults to None.
        temp (float, optional): The temperature for the model. Defaults to 0.   
        azure_api_version (str, optional): The API version for Azure OpenAI service. Defaults to None.
        azure_endpoint (str, optional): The endpoint for Azure OpenAI service. Defaults to None.
        azure_api_version (str): The API version for Azure OpenAI service. Defaults to None.
        
    Returns:
        str: JSON string containing the extracted challenges.
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

    challenges_prompt = f"""

    Your task is to carefully read the provided text about the synthesis, characterization, testing, and application of one or more materials. For each material discussed, identify any key **challenges** encountered during the research and the corresponding **solutions** the authors proposed or used.

    Only use information from the provided text. If no challenges are described for a material, do not include it in the output. If the text does not mention any challenges at all, return an empty list (`[]`).

    Return the results as a list of JSON objects. Each object should represent a single challenge related to a specific material and follow this format:

    {challenges_output_schema}

    ### Input:
    {synthesis_text}

    ### Output:
    Return ONLY the output as list of dictionaries List[Dict], and nothing else.
    """
    system_msg = SystemMessage(content="You are a helpful and precise materials research analysis assistant.")
    response = llm.invoke([
    system_msg,
    HumanMessage(content=challenges_prompt)
    ])

    # Separate the JSON part of the response
    try:
        json_start = response.content.index("[")
        json_end = response.content.rindex("]") + 1
        json_str = response.content[json_start:json_end]
    except ValueError:
        raise ValueError("Failed to extract JSON from LLM response. Check the response format.")

    try:
        extracted_output = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {json_str}") from e

    return extracted_output

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
# # Set the OpenAI API key
# openai_api_key = os.getenv("OPENAI_API_KEY")
# print(f"OPENAI_API_KEY: {openai_api_key[:4]}...")
# if not openai_api_key:
#     raise ValueError("OPENAI_API_KEY environment variable not set.")
                           
# azure_deployment=os.getenv("AZURE_MODEL_DEPLOYMENT_NAME")
# azue_api_version=os.getenv("AZURE_OPENAI_API_VERSION")
# azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")


# # An example synthesis text for testing:
# # synthesis_text = '''Synthesis and Coin Cell Preparation. NaxMnO2+z (NMO) and
# # NaxCo0.1Mn0.9O2+z (NCO) flakes were synthesized by combustion
# # synthesis as described previously.29,36−38 NaNO3 (Sigma-Aldrich,
# # ≥99%) and Mn(CH3COO)2 (Alfa Aesar, anhydrous, 98%) were
# # mixed (molar ratio Na:Mn = 0.7) and subsequently dissolved in
# # deionized water. For NCO, additional Co(NO3)2 was added, such that
# # the molar ratio of Na:Co:Mn was 0.7:0.1:0.9. Concentrated HNO3
# # (≥69%, Honeywell) was added, followed by 1.5 g of gelatin. The
# # solution was heated until spontaneous combustion occurred. The
# # resulting dark brownish powder was annealed at 800°C for 4 h,
# # followed by another step at 610°C for 9 h and quenching to room
# # temperature. Elemental composition, as determined by inductively
# # coupled plasma optical emission spectrometry (ICP-OES), was
# # Na0.6MnO2+z for the NMO flakes and Na0.6Co0.1Mn0.9O2+z for the
# # NCO flakes;“
# # z
# # ” in the above-mentioned formula units accounts for
# # Mn-vacancies and is typically between 0.05 and 0.25 for the P2
# # phase.13 Spherical NMO was synthesized as reported previously, with
# # a slightly modified annealing procedure.35 NH4HCO3 was dissolved in
# # deionized water, followed by a dropwise addition of ethanol (10%
# # volume of the NH4HCO3 solution) and a solution of MnSO4 in
# # deionized water. To form spherical MnCO3, the solution was stirred at
# # room temperature. After filtration and subsequent washing, the
# # product was annealed in air at 400°C for 5 h to form MnO2. Then, it
# # was dispersed in a solution of NaOH in deionized water and ethanol.
# # Next, both water and ethanol were evaporated, and the residue was
# # first annealed at 320°C in air for 3 h, followed by an annealing step in
# # air at 800 °C for 4 h and an additional step at 610°C for 9 h and
# # finally by quenching to room temperature. Chemical composition
# # according to ICP-OES was Na0.7MnO2+z. For NCO spheres the same
# # process was employed; however, CoSO4 was added to the MnSO4
# # solution to achieve a 10% ratio of cobalt in the final product. Chemical
# # composition according to ICP-OES was Na0.6Co0.1Mn0.9O2+z. As
# # shown previously,35 the surface area of flakes and spheres as measured
# # by BET is∼5 m2 g−1 for both materials.'''

# from src.utils.pymupdf_loader import PyMuPDFLoader
# data_dir = here("data/papers/Na-Mn-O")
# pdf_loader = PyMuPDFLoader(data_dir)
# file_name = "000690060.pdf"
# pdf_text = pdf_loader.load_a_pdf(file_name)

# synthesis_text = '''{text}'''.format(text="\n".join(pdf_text))

# synthesis_info = extract_synthesis(
#                                    synthesis_text=synthesis_text,
#                                    api_key=azure_openai_api_key,
#                                    azure=True,
#                                    model_name=azure_deployment,
#                                    temp=0)

# challenges_info = extract_challenges(
#                                      synthesis_text=synthesis_text,
#                                      api_key=azure_openai_api_key,
#                                      azure=True,
#                                      model_name=azure_deployment,
#                                      temp=0)

# # cancat the the extracted synthesis and challenges info with the file name and save it into a json file
# import json
# import os
# output_dir = here("data/papers/Na-Mn-O")
# output_file = os.path.join(output_dir, "synthesis_and_challenges.json")
# with open(output_file, "w") as f:
#     json.dump({"file_name": file_name.replace(".pdf", ""),
#         "synthesis_info": synthesis_info,
#         "challenges_info": challenges_info
#     }, f, indent=4)

# print(f"Number tokens of PDFs loaded: {len(pdf_text)}")
# print(type(pdf_text))
# print(pdf_text[:100])

# synthesis_text = '''{text}'''.format(text=pdf_text)
# print(pdf_text[:100])

# print("Synthesis Info:", synthesis_info)
# print("Challenges Info:", challenges_info)


# # Example Response:
# # {
# #   "material": "Na0.6Co0.1Mn0.9O2+z",
# #   "synthesis": {
# #     "steps": [
# #       {
# #         "step": 1,
# #         "label": "Precursor Mixing",
# #         "details": {
# #           "reagents": ["NaNO3", "Mn(CH3COO)2", "Co(NO3)2"],
# #           "temperature": "room temperature",
# #           "duration": "not specified"
# #         }
# #       },
# #       {
# #         "step": 2,
# #         "label": "Combustion Synthesis",
# #         "details": {
# #           "reagents": ["Concentrated HNO3", "gelatin"],
# #           "temperature": "not specified",
# #           "duration": "until spontaneous combustion occurred"
# #         }
# #       },
# #       {
# #         "step": 3,
# #         "label": "Annealing",
# #         "details": {
# #           "reagents": ["dark brownish powder"],
# #           "temperature": "800 °C",
# #           "duration": "4 h"
# #         }
# #       },
# #       {
# #         "step": 4,
# #         "label": "Second Annealing",
# #         "details": {
# #           "reagents": ["resulting powder"],
# #           "temperature": "610 °C",
# #           "duration": "9 h"
# #         }
# #       },
# #       {
# #         "step": 5,
# #         "label": "Quenching",
# #         "details": {
# #           "reagents": ["annealed powder"],
# #           "temperature": "room temperature",
# #           "duration": "immediate"
# #         }
# #       }
# #     ]
# #   }
# # }

# # Challenges Info:
# # [
# #   {
# #     "stage": "Synthesis",
# #     "challenge": "The presence of stacking faults or inhomogeneities of the Na+ distribution in the hollow spheres.",
# #     "impact": "These defects can lead to broader reflections in XRD patterns, indicating potential structural issues.",
# #     "solution": "The authors used a short annealing time which can lead to these defects, but they also noted that the Co-doped materials are more crystalline, suggesting that Co facilitates the formation of the P2 phase during synthesis.",
# #     "evidence": "Discussed in the Physical Characterization section, particularly in the context of the XRD analysis of the materials."
# #   },
# #   {
# #     "stage": "Characterization",
# #     "challenge": "The presence of a two-phase region in NMO flakes during discharge.",
# #     "impact": "This phase transition is attributed to the increased amount of Jahn−Teller active Mn3+, leading to structural changes.",
# #     "solution": "Co-doping was used to suppress these structural transformations, preventing the phase transition to an orthorhombic phase.",
# #     "evidence": "Discussed in the Structural Studies section, particularly in the context of the XRD analysis of NMO and NCO flakes."
# #   },
# #   {
# #     "stage": "Testing",
# #     "challenge": "Capacity fading in NMO flakes.",
# #     "impact": "Capacity fading can reduce the effectiveness and lifespan of the battery.",
# #     "solution": "The authors investigated manganese dissolution and found it to be negligible, suggesting that structural changes rather than dissolution are responsible for capacity fading.",
# #     "evidence": "Discussed in the Manganese Dissolution section."
# #   },
# #   {
# #     "stage": "Testing",
# #     "challenge": "Lower diffusion coefficients in undoped materials.",
# #     "impact": "Lower diffusion coefficients indicate slower Na+ transport, which can affect the rate capability and cycling stability.",
# #     "solution": "Co-doping was shown to enhance Na+ conductivity, resulting in higher diffusion coefficients and better rate capability.",
# #     "evidence": "Discussed in the Diffusion and Conductivity Properties section, particularly in the context of GITT and EIS measurements."
# #   }
# # ]