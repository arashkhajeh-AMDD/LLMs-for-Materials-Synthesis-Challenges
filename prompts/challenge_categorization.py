CHALLENGE_COMBINED_PROMPT = """
    A list of challenges related to {challenge_stage} of materials has been provided. Your task is to carefully read the following list of challenges and categorize them into different categories.
    At the same time, try to minimize overlapping between the categories by adding new categories if necessary.
    The categories should be based on the content of the challenges and should not be too broad or too specific.
    The categories should be meaningful and relevant to the challenges provided.
    The challenges are as follows:
    {challenge_texts}

    IMPORTANT:
    - The total number of challenges in the output must match the number provided in the input.
    - Each challenge must appear in the output exactly once, under a single category.
    - If a challenge seems ambiguous or hard to categorize, place it in a category like "Unclear" or "Other" rather than omitting it.
    - Return ONLY the output as a JSON object in the following format:
    
    {{
        "Category 1 label": ["challenge 1", "challenge 2"],
        "Category 2 label": ["challenge 3", "challenge 4"]
    }}
    """

CHALLENGE_COMBINED_PROMPT_WITH_IDS = """
    A list of challenges related to {challenge_stage} of materials has been provided. Your task is to carefully read the following list of challenges and categorize them into different categories.
    At the same time, try to minimize overlapping between the categories by adding new categories if necessary.
    The categories should be based on the content of the challenges and should not be too broad or too specific.
    The categories should be meaningful and relevant to the challenges provided.
    The challenges are as follows:
    {challenge_texts}

    IMPORTANT:
    - Each challenge begins with a numeric ID in square brackets (e.g., [0], [1], ...).
    - Your task is to assign each challenge ID (not the full text) to exactly ONE category.
    - Each challenge ID must appear in the output exactly once.
    - You MUST NOT repeat or omit any IDs.
    - If a challenge item seems hard to categorize, place its ID under a category labeled "Other".
    - Return ONLY the output as a valid JSON object in the following format:
    
    {{
        "Category 1 label": [1, 4],
        "Category 2 label": [2, 3]
    }}
    """

CHALLENGE_COMBINED_PROMPT_WITH_IDS_COT = """
You are a materials science expert. A list of challenges related to the "{challenge_stage}" stage of materials research is provided below.

Your task is to **analyze each challenge individually**, reason about its most appropriate category based on content, and **then group the challenge IDs into meaningful, non-overlapping categories**.

The goals are:
- Create well-defined categories that accurately describe the themes of the challenges.
- Avoid overly broad or overly specific categories.
- Minimize overlap across categories by choosing the most relevant one for each challenge.

The challenges are:
{challenge_texts}

---

### STEP 1: Reasoning (Chain of Thought)
For each challenge ID, explain your reasoning to determine the best-fit category.
For example:
[1] discusses capacity loss over cycles → likely belongs to "Cycle stability and degradation".
[2] mentions oxygen release at high temperature → fits in "Thermal instability and oxygen evolution".

Continue this process for every challenge from [1] to [N].

---

### STEP 2: Categorization
Based on the reasoning above, group the challenge IDs into categories. Format the final output **only** as a valid JSON object like this:

{{
    "Category A label": [1, 4],
    "Category B label": [2, 3, 5],
    ...
}}

---

IMPORTANT:
- Each challenge begins with a numeric ID in square brackets (e.g., [1], [2], ...).
- Each challenge ID must appear **exactly once** in the final output.
- DO NOT omit or repeat any IDs.
- If a challenge is ambiguous or hard to classify, assign it to a category labeled "Other".
- Return **only the JSON object** in your final output.
"""


# CHALLENGE_COMBINED_PROMPT_WITH_IDS_COT = """
#     You are a materials synthesis expert tasked with categorizing challenges occuring during {challenge_stage} of materials.
#     A list of challenges has been provided. Your task is to carefully read the following list of challenges and categorize them into different categories.
#     At the same time, try to minimize overlapping between the categories by adding new categories if necessary.
#     The categories should be based on the content of the challenges and should not be too broad or too specific.
#     The categories should be meaningful and relevant to the challenges provided.
#     The challenges are as follows:
#     {challenge_texts}

#     For each ID:
#     - Think aloud about which category it fits best based on the wording and meaning.
#     - Then assign it to one and only one category using the action format:
#     `Assign [ID] -> "Category Name"`

#     At the end, output a final summary JSON grouping the IDs by category.

#     ### Example format:
#     Reasoning:
#     [0]: Mentions capacity fading over cycles → Assign [0] -> "Cycle life and stability issues"
#     [1]: Refers to oxygen release during high temp → Assign [1] -> "Oxygen loss and thermal effects"

#     Final Output:
#     {{
#         "Cycle life and stability issues": [1],
#         "Oxygen loss and thermal effects": [2]
#     }}
#     """

CHALLENGE_CATEGORY_IDENTIFICATION_PROMPT = """
    You are a materials synthesis expert tasked with identifying categories of challenges. A list of challenges related to {challenge_stage} of materials has been provided. Your task is to carefully read the following list of challenges and identify all categories of challenges.
    The categories should be based on the content of the challenges. Try to identify categories that encompass few challenges, but at the same time be specific enough to capture the essence of challenges in each category for materials scientists.
    Each category should be a string representing a range of challenge items related to {challenge_stage} of materials.
    Categories should encompass all challenges in the list.
    The categories should be meaningful and relevant to the challenges provided.
    The challenges are as follows:
    {challenge_texts}

    Return ONLY the output as a JSON object in the following format:

    {{
    "Categories": ["category 1", "category 2"],
    }}
    """

CHALLENGE_CATEGORIZATION_PROMPT = """
    You are a materials synthesis expert tasked with categorizing challenges occuring during {challenge_stage} of materials. A list of challenges related to {challenge_stage} of materials has been provided. Your task is to carefully read the following list of challenges and assign each challenge to the most relevant category.
    A list of challenges and a list of challenge categories have been provided, and your task is to assign each challenge to the most relevant category.

    The challenges are as follows:
    {challenge_texts}

    The categories are as follows:
    {challenge_categories}

    IMPORTANT:
    - You MUST use the exact wording of the input challenge items without any rephrasing, editing, or rewriting.
    - DO NOT paraphrase or summarize the input text.
    - Each challenge must appear in the output exactly once, under a single category.
    - Return ONLY the output as a JSON object in the following format:
    - If a challenge cannot be categorized, assign it to the "Other" category.
    
    {{
        "Category 1": ["challenge 1", "challenge 2"],
        "Category 2": ["challenge 3", "challenge 4"]
    }}
    """


