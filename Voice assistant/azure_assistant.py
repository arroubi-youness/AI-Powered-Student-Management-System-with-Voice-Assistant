from openai import AzureOpenAI

from TextToSpeech import text_to_speech_fnc


class Azure_assistant:
    def __init__(self):
        self.endpoint = "https://zakh-m5jqxxjr-swedencentral.openai.azure.com/"
        self.deployment = "gpt-4"

        self.text_to_speech_fnc = text_to_speech_fnc
        self.subscription_key = "2U5qjJv1j4SYUilaPZqkGTwfuiD3zuzdh0SOBTfDN5IlgyDuoeJgJQQJ99BAACfhMk5XJ3w3AAAAACOGbjM5"
        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.subscription_key,
            api_version="2024-05-01-preview",
        )