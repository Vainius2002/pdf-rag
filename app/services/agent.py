from typing import TypedDict #using typedict for more hints than regular dict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.services.llm import llm
from app.services.embeddings import embed
from app.services.storage import get_top_chunks

#State = shared dict for the whole graph:
class AgentState(TypedDict):
    question: str
    document_id: int
    chunks: str
    grade: str #YES or NO set by grade_node
    answer: str
    attempts: int

#prompts:
grade_prompt = ChatPromptTemplate.from_template(
    "Question: {question}\n\n"
    "Context:\n{context}\n\n"
    "Does the context contain enough information to answer the question? "
    "Reply with one word only: YES or NO"
)

answer_prompt = ChatPromptTemplate.from_template(
    "Answer the question based only on the context below. "
    "If the answer isn't in the context, say you don't know.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}"
)

#creation of both chains:
grade_chain = grade_prompt | llm | StrOutputParser()
answer_chain = answer_prompt | llm | StrOutputParser()


#nodes:
def retrieve_node(state: AgentState):
    #embed question and fetch top-k chunks:
    question_embedded = embed(state["question"])
    chunks = get_top_chunks(state["document_id"], question_embedded, k=5)
    
    context = ""
    for chunk in chunks:
        context += chunk.chunk_text + "\n"
    
    return {
        "chunks" : context,
        "attempts" : state.get("attempts", 0) + 1, #i use 0, in case theres no attempts, meaning i wont get an error.
    }
    
def grade_node(state: AgentState):
    "answer logic based on if chunks actually answer question with YES or NO"
    grade = grade_chain.invoke({"question" : state["question"], "context" : state["chunks"]})
    return {"grade" : grade.strip().upper()} #overwriting tyepdicts grade w new value

def answer_node(state: AgentState):
    "Actual answer logic"
    answer = answer_chain.invoke({"question" : state["question"], "context" : state["chunks"]})
    return {"answer" : answer} 


#Router (conditional edge):
def should_retry(state: AgentState):
    "What happens after grade_node runs"
    if state["attempts"] >= 2:
        return "have_enough"
    if state["grade"] == "YES":
        return "have_enough"
    return "try_again"

#graph building:

graph_builder = StateGraph(AgentState)

graph_builder.add_node("retrieve", retrieve_node)
graph_builder.add_node("grade", grade_node)
graph_builder.add_node("answer", answer_node)

graph_builder.set_entry_point("retrieve") #we start from this node/function

graph_builder.add_edge("retrieve", "grade") #after retrieve nodes/functions - activate grade node.
graph_builder.add_edge("answer", END) #after answer node/function END loop.

# we set up logic for should retry
graph_builder.add_conditional_edges(
    "grade", #after grade func finishes:
    should_retry, #run should_retry
    {
        "have_enough" : "answer", #if should_retry returns answer - it should route to answer node
        "try_again" : "retrieve", #if should_retry returns retrieve - it should route to retrieve node
    },
)

agent = graph_builder.compile()


