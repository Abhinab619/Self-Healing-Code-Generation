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
    code_path : str

def execute_python_code(code_path: str) :
    
    with open(code_path, "r", encoding="utf-8") as code_file:
        code = code_file.read()
    
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
        error_log_path = os.path.join("codes", f"{uuid.uuid4().hex}.log")
        with open(error_log_path, "w", encoding="utf-8") as error_file:
            error_file.write("\n  No errors. \n\n OUTPUT = " + result.stdout)
        print(f"Execution successful. Output: {result.stdout}")
        error_log_path = error_log_path.replace("\\", "/")
        return {
    "code_path": file_path,
    "log_path": error_log_path
}
    
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




    

tool4 = StructuredTool.from_function(
    name="tool4",
    description="Use this tool to execute Python code. The input is the Python code to execute in str format,(properly treat unicodes) ( Use the code as is, dont improve anything) , Return only if code ran successfully or not,",
    func=execute_python_code, 
)



