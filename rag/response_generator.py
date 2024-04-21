from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser


def load_response_generator():
    llm = ChatOllama(model="llama3", temperature=0, num_predict=-1)
    prompt = PromptTemplate(
        template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|> You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. 
        Use three sentences maximum and keep the answer concise <|eot_id|><|start_header_id|>user<|end_header_id|>
        Question: {question} 
        Context: {context} 
        Answer: <|eot_id|><|start_header_id|>assistant<|end_header_id|>""",
        input_variables=["question", "document"],
    )
    return LLMChain(prompt=prompt, llm=llm, output_parser=StrOutputParser())