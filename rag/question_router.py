from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser


def load_question_router():
    llm = ChatOllama(model="llama3", format="json", temperature=0, num_predict=-1)
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an expert at routing a 
        user question to a vectorstore or web search. Use the vectorstore for questions on LLM  agents, 
        prompt engineering, and adversarial attacks. You do not need to be stringent with the keywords 
        in the question related to these topics. Otherwise, use web-search. Give a binary choice 'web_search' 
        or 'vectorstore' based on the question. Return the a JSON with a single key 'datasource' and 
        no premable or explaination. Question to route: {question} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
        input_variables=["question"],
    )
    return LLMChain(prompt=prompt, llm=llm, output_parser=JsonOutputParser())