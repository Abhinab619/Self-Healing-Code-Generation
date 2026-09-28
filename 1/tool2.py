from groq import Groq
from langchain_groq import ChatGroq
from langchain.tools import StructuredTool
from pydantic import BaseModel

import os
from dotenv import load_dotenv
load_dotenv()



# Automation _tool_imports
client = Groq(api_key=os.getenv("GROQ_API_KEY"))





# class WebsiteTesterToolInput(BaseModel):
#     code : str



import subprocess
import uuid




class code_generator(BaseModel):
    code : str

def execute_python_code(code: str) :
    
    # Ensure directory exists
    os.makedirs("codes", exist_ok=True)

    # Generate unique filename
    file_name = f"code_{uuid.uuid4().hex}.py"
    file_path = os.path.join("codes", file_name)

    # Write code to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    file_path = file_path.replace("\\", "/")  # Handle Windows paths

    # Execute the file
    result = subprocess.run(
        ["python", file_path],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0:
        print(f"Execution succeeded. Output: {result.stdout}")
        return "Code ran successfully"

    
    else:
        error_log_path = os.path.join("codes", f"error_{uuid.uuid4().hex}.log")
        with open(error_log_path, "w", encoding="utf-8") as error_file:
            error_file.write(result.stderr)
        print(f"Execution failed. Error: {result.stderr}")
        
        error_log_path = error_log_path.replace("\\", "/")
        return {
    "code_path": file_path,
    "log_path": error_log_path
}




    

tool2 = StructuredTool.from_function(
    name="tool2",
    description="Use this tool to execute Python code. The input is the Python code to execute in str format,(properly treat unicodes and special characters, and formatting only) ,(save the code and the error message in a file named new_code and   error_unique name as (same as code) .log) "
    "Also return the path of the code and the log file.",
    func=execute_python_code, 
)



