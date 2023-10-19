from altair import Description
from sqlalchemy import desc
import streamlit as st
from tabnanny import verbose
from dotenv import load_dotenv
from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL


from langchain.tools.python.tool import PythonREPLTool
from langchain import OpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent, initialize_agent, load_tools
import os

from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.tools import ShellTool




load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def main():
    
    python_function_executor = create_python_agent(
    llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
    tool=PythonREPLTool(),
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    agent_executor_kwargs={"handle_parsing_errors": True},
    )
    

    csv_agent = create_csv_agent(llm=ChatOpenAI(temperature=0, model="gpt-4"),
                                 path='episode_info.csv', verbose=True
                                 )
    
    python_function_executor = create_python_agent(
    llm=OpenAI(temperature=0, max_tokens=1000),
    tool=PythonREPLTool(),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
    shell_tool = ShellTool()
   
    shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace("{", "{{")

    grant_agent = initialize_agent(tools = [
        Tool(name="pythonAgent",
              func = python_function_executor.run,
              description= """Useful when you need to transform natural language and write from it in python and execute the python code 
              return the result of the code execution.
              Dont send python code to this tool              
              """
        ),
        Tool(name="csvAgent",
             func=csv_agent.run,
             description="""Useful when you need to return info from csv file take the entire question as an input and return the answear using pandas calculation"""
             ),
        Tool(name="shelltoool",
             func=shell_tool.run,
             description=""" Usefull when need to run a shell command like if you need to run streamlit python function, run command or generaye pygame interface""")
        ],
        llm=ChatOpenAI(temperature=0,
                       model="gpt-4",
                       verbose=True),
         agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
         verbose=True)  
    
    question = st.text_input("Que voulez vous")                    
    
    grant_agent.run(question)


    
if __name__ == "__main__":
    main()