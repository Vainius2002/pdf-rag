from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def embed(text):
      response = client.embeddings.create(
          model="text-embedding-3-small",
          input=text,
      )
      return response.data[0].embedding