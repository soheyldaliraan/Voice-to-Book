from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class TextService:
    def __init__(self):
        self.client = OpenAI()

    def format_as_article(self, text: str) -> str:
        """Format the transcribed text as a book article using ChatGPT"""
        logger.info("Starting article formatting with ChatGPT")
        
        prompt = f"""Please format the following Persian text as a well-structured book article.
        Fix any spelling or grammar errors.
        Don't change the words or the meaning of the text.
        Do not add any new words or phrases.
        Add proper punctuation.
        Keep the same words and meaning.
        Keep the text in Persian.
        Keep the text in the same order as the original text.
        Keep the text in the same length as the original text.
        Keep the text in the same words as the original text.
        Keep the text in the same meaning as the original text.
        
        Text: {text}
        """
        
        response = self.client.chat.completions.create(
            model="o1",
            messages=[
                {"role": "system", "content": "You are a professional Persian book editor"},
                {"role": "user", "content": prompt}
            ],
        )
        
        formatted_text = response.choices[0].message.content
        logger.info("Article formatting completed successfully")
        return formatted_text 