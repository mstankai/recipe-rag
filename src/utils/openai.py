import keyring
from openai import OpenAI

def get_openai_completion(
        client: OpenAI, 
        model: str, 
        messages: list[str], 
        n_choices: int = 1, 
        top_p: float = 1.0
    ) -> list[str]:
    """
    Get completions from the OpenAI API.

    Args:
        client (OpenAI): OpenAI client.
        model (str): madel name
        messages (list[str]): List of messages.
        n_choices (int, optional): Number of choices. Defaults to 1.
        top_p (float, optional): Froction of probability density distribution of answers to use. Defaults to 1.0.

    Returns:
        list[str]: List of completions.
    """
    completion = client.chat.completions.create(
        model = model,
        messages = messages,
        top_p = top_p,
        n = n_choices
    )

    answer = [ c.message.content for c in completion.choices ]

    return answer