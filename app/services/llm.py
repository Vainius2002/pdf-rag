from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def llm_message(question, pdf_polished):
    response = client.responses.create(
        model="gpt-5-mini",
        input=f"{question} : {pdf_polished}"
    )
    return response.output_text
    