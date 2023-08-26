import os
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


def initialize_openai(config: dict) -> None:
    """
    Initialize OpenAI with the provided configuration.

    Args:
        config (dict): Configuration dictionary.
    """
    openai.organization = config["OPENAI_ORG"]
    openai.api_key = config["OPENAI_KEY"]


def ask_openai(question: str, prompt_key: str, model_id: str, prompts: dict) -> tuple:
    """
    Query OpenAI with a question and get a response.

    Args:
        question (str): The user's question.
        prompt_key (str): The key to retrieve the prompt from the prompts dictionary.
        model_id (str): The OpenAI model ID to use.
        prompts (dict): Dictionary of available prompts.

    Returns:
        tuple: OpenAI's response and the total token usage.
    """
    chat_completion = openai.ChatCompletion.create(
        model=model_id,
        messages=[
            {"role": "system", "content": prompts[prompt_key]},
            {"role": "user", "content": question}
        ]
    )
    return chat_completion.choices[0].message.content, chat_completion.usage.total_tokens


def rename_pdf_based_on_txt(prompts: dict, model_id: str) -> None:
    """
    Rename PDFs based on corresponding TXT file content using OpenAI's suggestion.

    Args:
        prompts (dict): Dictionary of available prompts.
        model_id (str): The OpenAI model ID to use.
    """
    for txt_file in os.listdir('.'):
        if txt_file.endswith('.txt'):
            with open(txt_file, 'r') as f:
                content = f.read()

            suggested_name, usage_cost = ask_openai(content, "filenames", model_id, prompts)
            suggested_name = suggested_name.strip('"')
            if not suggested_name.endswith('.pdf'):
                suggested_name += '.pdf'

            print(f"Suggested name: {suggested_name}")
            print(f"Tokens Used: {usage_cost}")

            original_pdf_name = os.path.splitext(txt_file)[0] + '.pdf'

            if os.path.exists(original_pdf_name):
                os.rename(original_pdf_name, suggested_name)
            else:
                print(f"Error: {original_pdf_name} not found!")


if __name__ == "__main__":
    CONFIG = load_config()
    initialize_openai(CONFIG)
    # Placeholder for prompts (add your prompts here)
    PROMPTS = {
        "filenames": "Your task is to create the most comprehensive name for the following content in a file. A few things to keep in mind: \n Dates matter, make sure that if you find a tax document, the year is on the name, ie '2022 W2 Tax Return', or if there are paystubs, you have the dates the paystubs are for, ie 'Income_Paystub 6.23-.8.13'. "
                     "\n If you have a utility, make sure to note it. ie 'Utility_Gas July 2023'. Or other types such as Bank Statements, Credit Card statements, mortgages, anything like that."
                     "\n The main idea is, in the filename, to have the type of file, a date or year if possible, and/or the company (for example which company's credit card statement?). Please do your best to be as accurate as possible and only respond with your suggested filename, nothing else. Please also limit your use of underscores, prefer spaces.",
    }
    rename_pdf_based_on_txt(PROMPTS, CONFIG["AI_MODEL"])

