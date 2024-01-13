import yaml
from pyprojroot import here


class LoadConfig:
    """
    A class for loading configuration settings, including OpenAI credentials.

    This class reads configuration parameters from a YAML file and sets them as attributes.
    It also includes a method to load OpenAI API credentials.

    Attributes:
        gpt_model (str): The GPT model to be used.
        temperature (float): The temperature parameter for generating responses.
        llm_system_role (str): The system role for the language model.
        llm_format_output (str): The formatting constrain of the language model.

    Methods:
        __init__(): Initializes the LoadConfig instance by loading configuration from a YAML file.
        load_openai_credentials(): Loads OpenAI configuration settings.
    """

    def __init__(self) -> None:
        with open(here("config.yml")) as cfg:
            app_config = yaml.load(cfg, Loader=yaml.FullLoader)
        self.gpt_model = app_config["gpt_model"]
        self.temperature = app_config["temperature"]
        self.max_tokens = app_config["max_tokens"]
        self.articles_to_search = app_config["articles_to_search"]
        self.llm_system_role = app_config["llm_system_role"]
        self.llm_format_output = app_config["llm_format_output"]
        self.chunk_size = app_config["chunk_size"]
        self.similarity_top_k = app_config["similarity_top_k"]
