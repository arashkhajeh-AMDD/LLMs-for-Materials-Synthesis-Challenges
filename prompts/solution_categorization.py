SOLUTION_COMBINED_PROMPT = """
    A list of solutions related to {challenge_stage} of materials has been provided. Your task is to carefully read the following list of solutions and categorize them into different categories.
    At the same time, try to minimize overlapping between the categories by adding new categories if necessary.
    The categories should be based on the content of the solutions and should not be too broad or too specific.
    The categories should be meaningful and relevant to the solutions provided.
    Ensure that each solution is assigned to one and only one category.

    The solutions are as follows:
    {solution_texts}

    IMPORTANT:
    - The total number of solutions in the output must match the number provided in the input.
    - Each solution must appear in the output exactly once, under a single category.
    - If a solution seems ambiguous or hard to categorize, place it in a category like "Unclear" or "Other" rather than omitting it.
    - Return ONLY the output as a JSON object in the following format:
    
    {{
        "Category 1 label": ["solution 1", "solution 2"],
        "Category 2 label": ["solution 3", "solution 4"]
    }}
    """

SOLUTION_CATEGORY_IDENTIFICATION_PROMPT = """
    You are a materials synthesis expert tasked with identifying categories of solutions. A list of solutions related to {challenge_stage} of materials has been provided. Your task is to carefully read the following list of solutions and identify all categories of solutions.
    The categories should be based on the content of the solutions. Try to identify categories that encompass few solutions, but at the same time be specific enough to capture the essence of solutions in each category for materials scientists.
    Each category should be a string representing a range of solution items related to {challenge_stage} of materials.
    Categories should encompass all solutions in the list.
    The categories should be meaningful and relevant to the solutions provided.
    The solutions are as follows:
    {solution_texts}

    Return ONLY the output as a JSON object in the following format:

    {{
    "Categories": ["category 1", "category 2"],
    }}
    """

SOLUTION_CATEGORIZATION_PROMPT = """
    You are a materials synthesis expert tasked with categorizing solutions occuring during {challenge_stage} of materials. A list of solutions related to {challenge_stage} of materials has been provided. Your task is to carefully read the following list of solutions and assign each solution to the most relevant category.
    A list of solutions and a list of solution categories have been provided, and your task is to assign each solution to the most relevant category.

    The solutions are as follows:
    {solution_texts}

    The categories are as follows:
    {solution_categories}

    IMPORTANT:
    - Each solution must appear in the output exactly once, under a single category.
    - Return ONLY the output as a JSON object in the following format:
    - If a solution cannot be categorized, assign it to the "Other" category.

    {{
        "Category 1": ["solution 1", "solution 2"],
        "Category 2": ["solution 3", "solution 4"]
    }}
    """


