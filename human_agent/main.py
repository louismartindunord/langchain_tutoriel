   
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
import os

from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def main():
 
    llm = ChatOpenAI(temperature=0.0)
    math_llm = OpenAI(temperature=0.0)
    tools = load_tools(
        ["human", "llm-math"],
        llm=math_llm,
    )

    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    agent_chain.run("What's my friend Eric's surname?")

    
if __name__  == "__main__":
    main()