import dotenv
import os
from datetime import datetime
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown
from rich.align import Align

dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")
client = genai.Client(api_key=GEMINI_API_KEY)

def read_file(filename):
    with open(os.path.join("context", f"{filename}.txt"), 'r') as file:
        return file.read()
    
def write_file(filename,content):
    with open(os.path.join("context", f"{filename}.txt"), 'a') as file:
        file.write(content+"\n")

def file_list():
    if not os.path.exists("context"):
        os.makedirs("context")
    return os.listdir("context")

def extract_title_from_file(filename):
    with open(os.path.join("context", f"{filename}"), 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("Title:"):
                return line.replace("Title:", "").strip()
    return None

def print_file_list():
    files = file_list()
    print("Files in context directory:")
    i=1
    for file in files:
        print(f"{i}. {extract_title_from_file(file)}")
        i+=1

def generate_title(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            prompt,
            "Give a title for this. Respond in 6-7 words or less. you dont have to explpain anything or write any code. Just give the title."
        ],
    )
    cleaned_response = response.text.replace('**', '')
    return cleaned_response

def save_context(filename, context):
    if not os.path.exists("context"):
        os.makedirs("context")
    write_file(filename, context)
    print(f"Context saved to {filename}.txt")

def put_title_in_file(filename, title):
    with open(os.path.join("context", f"{filename}.txt"), 'a') as file:
        file.write(f"Title:{title}\n")



def chat_session(fileNo):
    console = Console()

    if (fileNo==0):
        console.print("[bold #efd3d7]Starting a new chat session.[/bold #efd3d7]")
        console.print("[bold #8e9aaf]=========================[/bold #8e9aaf]")
        console.print("[bold #dee2ff]You can ask me anything.[/bold #dee2ff]")
        console.print("[bold orange]Type 'exit' to end the session.[/bold orange]")

        timeandDate = datetime.now()
        timeandDate = timeandDate.strftime("%Y-%m-%d_%H-%M-%S")
        
        chat_session = client.chats.create(model="gemini-2.0-flash")
        prompt = ""
        while(prompt != "exit"):
            console.print("[bold #BB86FC]You:[/bold #BB86FC] ", end="")
            prompt = input()
            if(prompt == "exit"):
                console.print("[bold red]Ending the session.[/bold red]")
                console.print("[bold red]=========================[/bold red]")
                console.print("[bold green]Saving this session.[/bold green]")
                
                messages = chat_session.get_history()
                message = messages[0].parts[0].text
                
                title = generate_title(message)
                console.print(f"[bold]Title:[/bold] {title}")
                filename = f"{timeandDate}"
                put_title_in_file(filename, title)
                context_content = ""
                for message in messages:
                    role = message.role
                    text = message.parts[0].text
                    context_content += f"{role}: {text}\n\n"
                
                save_context(filename, context_content)
                break
            
            response = chat_session.send_message(prompt)
            
            markdownResponse = Markdown(response.text)
            console.print("[bold #03DAC5]Gemini:[/bold #03DAC5] ", end="")
            console.print(markdownResponse)
    else:
        read_filename = file_list()[fileNo-1].replace(".txt", "")
        context = read_file(read_filename)
        console.print("[bold #dee2ff]You can ask me anything.[/bold #dee2ff]")
        console.print("[bold #8e9aaf]=========================[/bold #8e9aaf]")
        console.print(f"[bold #BB86FC]Loading context from {read_filename}.txt[/bold #BB86FC]")
        console.print("[bold orange]Type 'exit' to end the session.[/bold orange]")
        chat_session = client.chats.create(model="gemini-2.0-flash")
        chat_session.send_message(context)
        prompt = ""
        previous_response = Markdown(context)
        console.print(previous_response)
        while(prompt != "exit"):

            console.print("[bold #BB86FC]You:[/bold #BB86FC] ", end="")
            prompt = input()
            if(prompt == "exit"):
                console.print("[bold red]Ending the session.[/bold red]")
                console.print("[bold red]=========================[/bold red]")
                console.print("[bold green]Saving this session.[/bold green]")
                
                messages = chat_session.get_history()
                message = messages[0].parts[0].text

                title = generate_title(message)
                console.print(f"[bold]Title:[/bold] {title}")
                filename = f"{read_filename}"
                context_content = ""
                for message in messages:
                    role = message.role
                    text = message.parts[0].text
                    context_content += f"{role}: {text}\n\n"
                
                save_context(filename, context_content)
                break
            
            response = chat_session.send_message(prompt)
            
            markdownResponse = Markdown(response.text)
            console.print("[bold #03DAC5]Gemini:[/bold #03DAC5] ", end="")
            console.print(markdownResponse)
def main_chat():
    console = Console()
    
    # Check if any context files exist
    files = file_list()
    
    if not files:  # Empty list check
        console.print("[bold red]No saved contexts found. Starting a new session.[/bold red]")
        chat_session(0)
        return
    
    # If we have files, print them and get user selection
    print_file_list()
    
    fileNo = -1
    while True:
        try:
            fileNo_input = input("Enter the context number you want to load (or 0 for a new session): ")
            fileNo = int(fileNo_input)
            if fileNo < 0 or fileNo > len(files):
                console.print("[bold red]Invalid number. Please enter a number between 0 and " + 
                              f"{len(files)}.[/bold red]")
                continue
            break
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a valid number.[/bold red]")
    
    chat_session(fileNo)

main_chat()
