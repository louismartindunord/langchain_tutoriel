from tabnanny import verbose
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI 

from langchain.agents import initialize_agent, Tool, AgentType

from tools.tools import get_profile_url



def lookup(name:str)-> str:
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    template = "Given the full name {name_of_person}, i want you to get me a link to their linkedin profile page.your answear should only contain the URL"
    tools_for_agent = [
        Tool(
                name="Crawl Google for linkedin profile page",
                func= get_profile_url,
                description="useful when you need to get a linkedin Page URL"
            )
        ]
    agent = initialize_agent(tools=tools_for_agent,
                             llm=llm, 
                             agent= AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                             verbose=True )
    
    prompt =  PromptTemplate(template=template, input_variables=['name_of_person'])
    linked_profile_url = agent.run(prompt.format_prompt(name_of_person=name))
    return linked_profile_url
    