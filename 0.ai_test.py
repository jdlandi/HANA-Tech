import json

import openai


def load_config(filename: str = "config.json") -> dict:
    """
    Load the configuration file.

    Args:
        filename (str): Name of the configuration file.

    Returns:
        dict: Parsed configuration.
    """
    with open(filename, "r") as file:
        return json.load(file)


def verify_config(config: dict, keys: list[str]) -> None:
    """
    Verify the necessary keys in the configuration.

    Args:
        config (dict): Configuration dictionary.
        keys (list[str]): List of keys to check.

    Raises:
        Exception: If any key is missing or not set.
    """
    for key in keys:
        if not config.get(key):
            raise Exception(f'Configuration {key} must be set or is missing.')


def initialize_openai(config: dict) -> None:
    """
    Initialize OpenAI with the provided configuration.

    Args:
        config (dict): Configuration dictionary.
    """
    openai.organization = config["OPENAI_ORG"]
    openai.api_key = config["OPENAI_KEY"]


def list_model_ids() -> list[str]:
    """
    List all available OpenAI model IDs.

    Returns:
        list[str]: List of model IDs.
    """
    models = openai.Model.list()
    return [model.id for model in models.data]


def ask_openai(question: str, prompt_key: str, model_id: str, prompts: dict) -> str:
    """
    Query OpenAI with a question and get a response.

    Args:
        question (str): The user's question.
        prompt_key (str): The key to retrieve the prompt from the prompts dictionary.
        model_id (str): The OpenAI model ID to use.
        prompts (dict): Dictionary of available prompts.

    Returns:
        str: OpenAI's response.
    """
    chat_completion = openai.ChatCompletion.create(
        model=model_id,
        messages=[
            {"role": "system", "content": prompts[prompt_key]},
            {"role": "user", "content": question}
        ]
    )
    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    CONFIG = load_config()
    REQUIRED_SETTINGS = ["OPENAI_KEY", "GCLOUD_WORKER_FILE", "GCLOUD_BUCKET"]

    verify_config(CONFIG, REQUIRED_SETTINGS)
    initialize_openai(CONFIG)

    PROMPTS = {
        "test_prompt": "This is a test. Please respond with a funny joke about programming that is related to what the user says."
    }

    print(list_model_ids())
    print(ask_openai("I sure love google cloud API", "test_prompt", CONFIG["AI_MODEL"], PROMPTS))
