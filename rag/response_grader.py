from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser


def load_response_grader():
    llm = ChatOllama(model="llama3", format="json", temperature=0, num_predict=-1)
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are a grader assessing whether an 
        answer is useful to resolve a question. Give a binary score 'yes' or 'no' to indicate whether the answer is 
        useful to resolve a question. Provide the binary score as a JSON with a single key 'score' and no preamble or explanation.
        <|eot_id|><|start_header_id|>user<|end_header_id|> Here is the answer:
        \n ------- \n
        {generation} 
        \n ------- \n
        Here is the question: {question} <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
        input_variables=["generation", "question"],
    )
    return LLMChain(prompt=prompt, llm=llm, output_parser=JsonOutputParser())