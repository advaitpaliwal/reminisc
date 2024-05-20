from openai import OpenAI
import os
import logging
from reminisc.config.config import Config

logger = logging.getLogger(__name__)


class MemoryClassifier:
    def __init__(self, openai_api_key: str):
        self.model_name = Config.CLASSIFIER_MODEL_NAME

        self.system_prompt = (
            "Analyze the user's input to determine if it contains any information worth remembering for future conversations.\n"
            "Consider a broad range of details that could enhance the quality and personalization of ongoing interactions, such as:\n"
            "- Personal facts: name, age, occupation, location, interests, preferences, etc.\n"
            "- Significant life events or experiences shared by the user\n"
            "- Important context about the user's current situation, challenges or goals\n"
            "- Any other details that provide valuable insights into the user's personality, perspective or needs\n"
            "If the input contains any such noteworthy information, respond with 'yes' to save it as a memory.\n"
            "If the input does not contain any important details worth saving, respond with 'no' to disregard it.\n"
        )
        self.openai = OpenAI(api_key=openai_api_key)

    def classify(self, query) -> bool:
        try:
            response = self.openai.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {'role': 'user', 'content': query}
                ],
                logit_bias={
                    '9891': 100,  # Token ID for 'yes'
                    '2201': 100   # Token ID for 'no'
                },
                max_tokens=1,
                temperature=0,
            )
            decision = response.choices[0].message.content.lower() == 'yes'
            logger.info(
                f"Classification decision for query '{query}': {decision}")
            return decision
        except Exception as e:
            logger.error(f"Error in classification: {e}")
            raise e

    def update_system_prompt(self, new_prompt):
        self.system_prompt = new_prompt
        logger.info(f"System prompt updated to: {new_prompt}")
