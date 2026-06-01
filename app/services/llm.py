from langchain_openai import ChatOpenAI
from app.config import OPENAI_API_KEY

llm = ChatOpenAI(
    model="gpt-5-mini",
    api_key=OPENAI_API_KEY,
    temperature=0,
)

# llm = a pre-configured "caller" object for the OpenAI chat model.
# Anywhere we need to ask the LLM something, we just call llm.invoke(prompt).
# temperature=0 = deterministic answers (good for Q&A; raise for creative output).