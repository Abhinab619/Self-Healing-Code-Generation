from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.schema import SystemMessage
from handler import ChatModelStartHandler
import os
from dotenv import load_dotenv
load_dotenv()


# Tool Imports
from tool1 import tool1
from tool2 import tool2
from tool3 import tool3



handler1 = ChatModelStartHandler()  





llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    callbacks=[handler1]
)

tools = [tool1, tool2, tool3]

# Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an Python developer who give syntax errors and fixes it using tool3.
     
You Have access to tools. (run every tool only once and in the same order as mentioned)

     
- Use {{tool1}} to Write Python code(only the code, nothing else), input will be the task, always give code with syntax errors, dont improve, i need to test the error handling capabilities of the agent.
- Use {{tool2}} to Execute Python code, input will be the code to execute and the output will code_path and log_path. 
- Use {{tool3}} to Fix the code based on the log of its execution, input will be code_path and log_path from tool2, Output will be the only the raw code.
- Use {{tool2}} again to execute the fixed provided code from tool3, input will be the fixed code, output will be the status

Important:
     - Dont improve the code, use the code as is, i need to test the error handling capabilities of the agent,
     use only the tool3 to fix the code




Final output will be the last ouput of tool2. i.e, status


    
     
"""),
    ("human", "{input}"),

    
    MessagesPlaceholder(variable_name="agent_scratchpad")
])



agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)


response = agent_executor.invoke({
   "input" : "code for Adding two numbers(6 and 99) in Python, (WITH SYNTAX ERRORS) and print output "

})

print(response["output"])

