#Setp 1: Setup API keys for Groq and Tavily
import os
from dotenv import load_dotenv
load_dotenv()


GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
OPEN_API_KEY=os.environ.get("OPEN_API_KEY")


#step2: Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

#openai_llm=ChatOpenAI(model="gpt-40-mini")
groq_llm=ChatGroq(model="llama-3.3-70b-versatile")

#Step3: Setup AI Agent with search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

system_prompt="Act as an AI chatbot who is smart and friendly"

def get_response_from_ai_agent(llm_id, query, allow_serch, system_prompt, provider):
    if provider=="Groq":
        llm=ChatGroq(model=llm_id)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=llm_id)
    
    tools=[TavilySearchResults(max_results=2)] if allow_serch else [] 
    agent=create_react_agent(
    model=llm,
    tools=tools,
    state_modifier=system_prompt
    )
    state={"messages": query}
    response=agent.invoke(state)
    messages=response.get("messages")
    ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]