from groq import Groq
from langchain_groq import ChatGroq
from langchain.tools import StructuredTool
from pydantic import BaseModel

import os
from dotenv import load_dotenv
load_dotenv()


# Automation _tool_imports

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
)



client = Groq(api_key=os.getenv("GROQ_API_KEY"))



class WebsiteTesterToolInput(BaseModel):
    task : str


def generate_python_code(task):
    prompt = f"""You are an expert Python developer. 
    Write Python code to accomplish the following task: {task}. 
    Only provide the code, no explanations or comments.
    
    Rules:
    - Only provide the code, no explanations or comments, no ``` symbols, no markdown, only the raw code.
    

    Important:
    - Give code with syntax errors, dont improve, i need to test the error handling capabilities of the agent.
    """

    response = llm.invoke(prompt)
    return response.content
    
    
    




     

tool1 = StructuredTool.from_function(
    func=generate_python_code,
    name="tool1",
    description="Use this tool to generate only one Python code for a given task. The input should be a description of the task you want to accomplish, and the output will be the generated Python code (in str format) that can be used to achieve that task",
    args_schema=WebsiteTesterToolInput  
)



