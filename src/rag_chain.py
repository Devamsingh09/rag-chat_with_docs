from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

def create_rag_chain(vectorstore):
    load_dotenv()
    retriever = vectorstore.as_retriever(search_kwargs={"k":3})
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",
                                 temperature=0.2,
                                 google_api_key=os.getenv("GOOGLE_API_KEY")
                                 )

    prompt = ChatPromptTemplate.from_template("""
                                              If answer does not lies in provided context then say -"Information does not lie in uploaded docs" but what I know about this and then generate answer through your own.
                                              Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {question}""")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
