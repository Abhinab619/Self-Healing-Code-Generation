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
    code_path : str
    log_path : str




# log = ""

def generate_python_code(code_path, log_path):

    with open(code_path, "r", encoding="utf-8") as code_file:
        code_content = code_file.read()
    with open(log_path, "r", encoding="utf-8") as log_file:
        log_content = log_file.read()



    prompt = f"""You are an expert Python developer. 
    You are given a python code and the log of its execution. code = {code_content} and log = {log_content}.
    process them both in str format
    Analyze the code entirely and the log, and provide a new version of the code that fixes the issues in code and logs properly, make sure the new code is correct

    You should only provide the code, no explanations or comments, no ``` symbols, no markdown, no logs, only the raw code generated.
    nothing else, only the raw code should be the output (with proper formatting).

    
    """

    response = llm.invoke(prompt)

    base_dir = os.path.dirname(code_path)
    new_code_path = os.path.join(base_dir, "new_" + os.path.basename(code_path))
    # new_log_path = os.path.join(base_dir, "new_" + os.path.basename(log_path))

    with open(new_code_path, "w", encoding="utf-8") as new_code_file:
        new_code_file.write(response.content)

    # with open(new_log_path, "w", encoding="utf-8") as new_log_file:
    #     new_log_file.write(log)
    

    return response.content
    
    
    




     

tool3 = StructuredTool.from_function(
    func=generate_python_code,
    name="tool3",
    description="""Use this tool to Fix the code based on the log of its execution. Input MUST be: {"code_path": "<path to .py file>", "log_path": "<path to .log file>"},convert it in this format if not before using tool,  " \
    "Also save the new code in a file named new_unique name as (same as code) .py(only the raw fixed code, nothing else, no paths, only the raw generated code ) .
    Only Return the raw code(nothing else), handlind unicode and special characters.
    """,
    args_schema=WebsiteTesterToolInput 
)



