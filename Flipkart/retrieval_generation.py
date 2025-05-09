from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import history_aware_retriever
from langchain.chains import create_history_aware_retriever
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from Flipkart.data_ingestion import data_ingestion 

from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
model = ChatGroq(model = "llama3-70b-8192", temperature=0.5)

chat_history = []
store = {}

def get_session_history(session_id:str)-> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def generation(vstore):
    retriever = vstore.as_retriever(search_kwargs = {"k":3})
    retriever_prompt = (
    "Given a chat history and the latest user question which might reference context in the chat history,"
    "formulate a standalone question which can be understood without the chat history."
    "Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
    )
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", retriever_prompt),
            MessagesPlaceholder(variable_name = "chat_history"),
            ("human","{input}")
        ]
    )
    
    history_aware_retriever = create_history_aware_retriever(model, retriever, contextualize_q_prompt)
    PRODUCT_BOT_TEMPLATE = """
    Your ecommercebot bot is an expert in product recommendations and customer queries. 
    It analyzes product titles and reviews to provide accurate and helpful responses. 
    Ensure your answers are relevant to the product context and refrain from straying off-topic. 
    Your responses should be concise and informative. 

    CONTEXT: 
    {context}
    
    QUESTION: {input}

    YOUR ANSWER:

    """
    
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", PRODUCT_BOT_TEMPLATE),
            MessagesPlaceholder(variable_name = "chat_history"),
            ("human","{input}")
        ]
    )
    
    question_answer_chain = create_stuff_documents_chain(model, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,                      # This is your LangChain chain (e.g., RetrievalQA or any Runnable)
        get_session_history,        # Function to return a Memory object (like ConversationBufferMemory)
        input_messages_key="input",         # Key in input dict for user input
        history_messages_key="chat_history", # Key used internally to pass previous messages
        output_messages_key="answer",       # Where the chain outputs its result
    )
    
    return conversational_rag_chain


if __name__ == "__main__":
    vstore = data_ingestion("done")
    conversational_rag_chain = generation(vstore)
    user_query_ask_question = input("Ask your question: ")
    answer = conversational_rag_chain.invoke(
        {"input": user_query_ask_question},
        config={
            "configurable": {"session_id": "Shubham"}
        },  # Constructs a key "abc123" in 'store'.
    )["answer"]
    print(answer)
    
    user_query_get_previous_question = input("Want previous question: ")
    answer1 = conversational_rag_chain.invoke(
        {"input": user_query_get_previous_question},
        config={
            "configurable":{"session_id":"Shubham"}
        },
    )["answer"]
    print(answer1)