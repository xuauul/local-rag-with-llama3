import os
from pprint import pprint
from langgraph.graph import (
    StateGraph,
    END,
)

from graph import (
    GraphState,
    decide_to_generate,
    generate,
    grade_documents,
    grade_generation,
    retrieve,
    route_question,
    web_search,
)

from utils import load_config

config = load_config()
LANGCHAIN_API_KEY = config["LANGCHAIN_API_KEY"]
os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = LANGCHAIN_API_KEY

workflow = StateGraph(GraphState)
workflow.add_node("websearch", web_search)
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade_documents", grade_documents)
workflow.add_node("generate", generate)

workflow.set_conditional_entry_point(
    route_question,
    {
        "websearch": "websearch",
        "vectorstore": "retrieve",
    },
)
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "websearch": "websearch",
        "generate": "generate",
    },
)
workflow.add_edge("websearch", "generate")
workflow.add_conditional_edges(
    "generate",
    grade_generation,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "websearch",
    },
)

app = workflow.compile()

# Test
inputs = {"question": "What are the types of agent memory?"}
for output in app.stream(inputs):
    for key, value in output.items():
        pprint(f"Finished running: {key}:")
pprint(value["generation"])

pprint("-" * 100)

inputs = {"question": "Who are the Bears expected to draft first in the NFL draft?"}
for output in app.stream(inputs):
    for key, value in output.items():
        pprint(f"Finished running: {key}:")
pprint(value["generation"])