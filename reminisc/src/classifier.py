from openai import OpenAI
import os
import logging
from config.config import Config
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class Classifier:
    def __init__(self):
        self.model_name = Config.CLASSIFIER_MODEL_NAME
        self.system_prompt = ("Analyze the user's input to determine if it includes information relevant for enhancing future interactions. "
                              "Consider whether the input provides insights into the user’s preferences, activities, personal details, or changes "
                              "that might be significant for future conversations. Should this information be remembered to improve the quality of "
                              "ongoing dialogue? Answer 'yes' to save or 'no' to disregard.")
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def classify(self, query) -> bool:
        try:
            response = self.openai.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {'role': 'user', 'content': query}
                ],
                logit_bias={
                    '1904': 100,  # Token ID for 'true'
                    '3934': 100   # Token ID for 'false'
                },
                max_tokens=1,
                temperature=0,
            )
            decision = response.choices[0].message.content.lower() == 'true'
            logger.info(
                f"Classification decision for query '{query}': {decision}")
            return decision
        except Exception as e:
            logger.error(f"Error in classification: {e}")
            raise e

    def update_system_prompt(self, new_prompt):
        self.system_prompt = new_prompt
        logger.info(f"System prompt updated to: {new_prompt}")
