import langchain
from langchain import OpenAI, PromptTemplate 
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

from third_parties.linkedin import scrape_linkedin_profile, clean_json_data
from agent.linkedin_lookup_agent import lookup as linkedin_lookup_agent

 
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SERPAPI_API_KEY = os.environ.get("SERPAPI_API_KEY")
nubela_api_key = os.environ.get("NUBELA")



if __name__ == "__main__":
    
    
    linkedin_profile_url = linkedin_lookup_agent(name="louis Martin du Nord")
    
    summary_template = """
         given the Linkedin information {information} about a person from I want you to create:
         1. a short summary
         2. two interesting facts about them
     """
    
    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
    
    print(chain.run(information=linkedin_data))
   