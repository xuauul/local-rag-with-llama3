from rag.response_generator import load_response_generator

response_generator = load_response_generator()

def generate(state):
    """
    Generate answer using RAG on retrieved documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    
    generation = response_generator.invoke({"context": documents, "question": question})
    return {"documents": documents, "question": question, "generation": generation['text']}