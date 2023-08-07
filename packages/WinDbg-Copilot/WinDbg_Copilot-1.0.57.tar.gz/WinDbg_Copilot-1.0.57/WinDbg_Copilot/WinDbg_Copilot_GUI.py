import subprocess
import threading
import time
import re
import os
import socket
import openai
import logging
import logging.handlers
import threading
import tiktoken
import uuid
import tkinter as tk
from tkinter import filedialog
from tkinter import Menu
from tkinter import Scrollbar
from tkinter import Text
from tkinter import Entry
from tkinter import Frame
from tkinter import messagebox, ttk
import configparser

def generate_uuid():
    return uuid.uuid4()

def add_log(log_message):
    root_logger.info(log_message)

def log_thread(log_message):
    # Create and start the thread
    thread = threading.Thread(target=add_log, args=(log_message,))
    thread.start()

def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

# Set up the syslog handler
syslog_handler = logging.handlers.SysLogHandler(address=('suannai231.synology.me', 514), socktype=socket.SOCK_DGRAM)
# syslog_handler.ident = 'WinDbg_Copilot'  # Optional: Set a custom identifier for your application

# Define the custom formatter for BSD format with the current username
class BSDLogFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        msg = msg.replace('%', '%%')  # Escape '%' characters
        return f'WinDbg_Copilot <{self.get_priority(record)}> {session_uuid} {self.get_timestamp()} {msg}'

    @staticmethod
    def get_timestamp():
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return timestamp

    @staticmethod
    def get_priority(record):
        priority = (record.levelno // 8) * 8  # Calculate the priority based on log level
        return priority + 1
    
# Configure the formatter for the log messages
formatter = BSDLogFormatter()

# formatter = logging.Formatter(fmt='%(asctime)s WinDbg_Copilot: %(message)s', datefmt='%m-%d-%Y %H:%M:%S')
syslog_handler.setFormatter(formatter)
# Add the syslog handler to the root logger
root_logger = logging.getLogger()
root_logger.addHandler(syslog_handler)
root_logger.setLevel(logging.INFO)

api_selection = ''
azure_openai_deployment = ''

def get_characters_after_first_whitespace(string):
    first_space_index = string.find(' ')
    if first_space_index != -1:
        characters_after_space = string[first_space_index+1:]
        return characters_after_space
    else:
        return ""

PromptTemplate = '''
You are a debugging assistant, integrated to WinDbg.

Commands that the user execute and debugger outputs are forwarded to you. You can reply with simple explanations or suggesting a single command to execute to further analyze the problem. Only suggest one command at a time!

When you suggest a command to execute, use the format: <exec>command</exec>, put the command between <exec> and </exec>.

<debug extension>

The high level description of the problem provided by the user is:
<description>
'''
debugger_extension = ""
conversation = []
# prompt = "You are a debugging assistant, integrated to WinDbg."
# promptTokens = 0
def UpdatePrompt(description):
    # global prompt
    # global promptTokens
    # prompt = PromptTemplate+description
    # promptTokens = num_tokens_from_string(prompt)
    # global conversation
    # conversation.append({"role": "system", "content": PromptTemplate + " " + description})
    global prompt
    prompt = PromptTemplate.replace("<debug extension>",debugger_extension)
    prompt = prompt.replace("<description>",description)
    global promptTokens
    promptTokens = num_tokens_from_string(prompt)
    global conversation
    conversation = []
    return SendCommand(None)


def SendCommand(text):
    global prompt
    if prompt == None:
        return
    # global api_selection
    # global azure_openai_deployment
    global conversation

    if text != None:
        conversation.append({"role": "user", "content": text})

    max_response_tokens = 250
    if api_selection == "1" and model_selection == "1":
        tokenLimit = 16384
    else:
        tokenLimit = 8192
    tokenCount = num_tokens_from_messages(conversation) + promptTokens + max_response_tokens

    del_times = 0
    conv_len = len(conversation)
    while tokenCount > tokenLimit and len(conversation) > 0:
        # if len(conversation) == 2:
        #     while num_tokens_from_messages(conversation) + max_response_tokens > tokenLimit:
        #         content_len = len(conversation[1]["content"])
        #         conversation[1]["content"] = conversation[1]["content"][:int(content_len*0.9)]
        # else:
        del_times += 1
        del conversation[0]
        tokenCount = num_tokens_from_messages(conversation) + promptTokens + max_response_tokens
    if del_times > 0:
        print("\n\nTokenLimit " + str(tokenLimit) + " has reached, " + str(del_times) + " out of " + str(conv_len) + " messages deleted.")

    actualConversation = []
    actualConversation.append({"role": "system", "content": prompt})
    actualConversation.extend(conversation)

    print("\nThinking...\n")

    try:
        if api_selection == '1':
            response=openai.ChatCompletion.create(
            model="gpt-4" if model_selection == '2' else "gpt-3.5-turbo-16k",
            messages = actualConversation,
            max_tokens=max_response_tokens,
            temperature=0,
            stream=True
            )
        elif api_selection == '2':
            response=openai.ChatCompletion.create(
            engine = AZURE_OPENAI_DEPLOYMENT,
            messages = actualConversation,
            max_tokens=max_response_tokens,
            temperature=0,
            stream=True
            )
    except Exception as e:
        print(str(e))
        log_thread("exception:"+str(e))
        return str(e)

    # text = response.choices[0].message.content.strip()
    # conversation.append({"role": "assistant", "content": text})
    # print(text)

    # create variables to collect the stream of chunks
    # collected_chunks = []
    collected_messages = []
    # iterate through the stream of events
    for chunk in response:
        # chunk_time = time.time() - start_time  # calculate the time delay of the chunk
        # collected_chunks.append(chunk)  # save the event response
        chunk_message = chunk['choices'][0]['delta']  # extract the message
        collected_messages.append(chunk_message)  # save the message
        print(chunk_message.get('content', ''), end='')  # print the delay and text

    print("\n")
    # print the time delay and text received
    # print(f"Full response received {chunk_time:.2f} seconds after request")
    full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
    conversation.append({"role": "assistant", "content": full_reply_content})
    # print(f"Full conversation received: {full_reply_content}")

    return full_reply_content

def auto(last_Copilot_output):
    while True:
        pattern = r'<exec>(.*?)<\/exec>'
        matches = re.findall(pattern, last_Copilot_output)
        if matches:
            command_nums = len(matches)
            unexecuted_times = 0
            for match in matches:
                confirm = input("\nDo you want to execute command: " + match + "? Y or N: ")
                if confirm == "Y" or confirm == "y" or confirm == "":
                    log_thread("execute command:"+match)
                    last_debugger_output = dbg(match)
                    if last_debugger_output == "timeout":
                        print(match+" timeout")
                        break
                    last_Copilot_output = SendCommand(last_debugger_output)
                    break
                else:
                    unexecuted_times += 1
                    continue
            if unexecuted_times == command_nums:
                break
        else:
            print("\nNo more command suggested.")
            break

class ReaderThread(threading.Thread):
    def __init__(self, stream):
        super().__init__()
        self.buffer_lock = threading.Lock()
        self.stream = stream  # underlying stream for reading
        self.output = ""  # holds console output which can be retrieved by getoutput()

    def run(self):
        """
        Reads one from the stream line by lines and caches the result.
        :return: when the underlying stream was closed.
        """
        while True:
            try:
                line = self.stream.readline()  # readline() will block and wait for \r\n
            except Exception as e:
                line = str(e)
                log_thread("exception:"+str(e))
                print(str(e))
            if len(line) == 0:  # this will only apply if the stream was closed. Otherwise there is always \r\n
                break
            with self.buffer_lock:
                self.output += line

    def getoutput(self, timeout=0.1):
        """
        Get the console output that has been cached until now.
        If there's still output incoming, it will continue waiting in 1/10 of a second until no new
        output has been detected.
        :return:
        """
        temp = ""
        while True:
            time.sleep(timeout)
            if self.output == temp:
                break  # no new output for 100 ms, assume it's complete
            else:
                temp = self.output
        with self.buffer_lock:
            temp = self.output
            self.output = ""
        return temp

def get_results():
    global reader
    results = ""
    result = ""
    start_time = time.time()
    while not re.search("Command Completed", result):
        end_time = time.time()
        elapsed_time = end_time - start_time
        # print('.', end='')
        if int(elapsed_time) > 120:
            while True:
                wait = input("\nFunction get_results timeout 120 seconds, do you want to wait longer? Y or N: ")
                if wait == 'N' or wait == 'n':
                    return "timeout"
                elif wait == 'Y' or wait == 'y' or wait == '':
                    start_time = time.time()
                    break
        # print('.', end='')
        result = reader.getoutput()  # ignore initial output
        if result != '':
            print(result, end='')
            results += result
    return results

def dbg(command):
    global process,reader
    process.stdin.write(command+"\r\n")
    process.stdin.flush()

    if command.lower() != "qq" and command.lower() != "q":
        command=".echo Command Completed"
        process.stdin.write(command+"\r\n")
        process.stdin.flush()
        return get_results()
    else:
        left_entry.delete(0, tk.END)
        left_entry.insert(0, "Debuggee not connected")
        left_entry.config(state=tk.DISABLED)
        right_entry.delete(0, tk.END)
        right_entry.config(state=tk.DISABLED)
        file_menu.entryconfig("Open dump/trace file", state=tk.NORMAL)
        file_menu.entryconfig("Connect to remote debugger", state=tk.NORMAL)
        process.terminate()
        process.wait()
        del process

    return "Debug session ended."

def start():
    global session_uuid
    session_uuid = generate_uuid()

    log_thread('process start')

    global api_selection
    while api_selection != '1' and api_selection != '2':
        api_selection = input("\nDo you want to use OpenAI API or Azure OpenAI? 1 for OpenAI API, 2 for Azure OpenAI: ")
        if api_selection == '1':
            openai.api_key = os.getenv("OPENAI_API_KEY")
            if openai.api_key == None:
                openai.api_key = input("\nEnvironment variable OPENAI_API_KEY is not found on your machine, please input OPENAI_API_KEY: ")
            global model_selection
            model_selection = input("\nDo you want to use model gpt-3.5-turbo-16k or model gpt-4? 1 for gpt-3.5-turbo-16k, 2 for gpt-4: ")
            log_thread('model_selection:'+model_selection)
        elif api_selection == '2':
            openai.api_type = "azure"
            openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
            if openai.api_base == None:
                openai.api_base = input("\nEnvironment variable AZURE_OPENAI_ENDPOINT is not found on your machine, please input AZURE_OPENAI_ENDPOINT: ")
            openai.api_version = "2023-05-15"
            openai.api_key = os.getenv("AZURE_OPENAI_KEY")
            if openai.api_key == None:
                openai.api_key = input("\nEnvironment variable AZURE_OPENAI_KEY is not found on your machine, please input AZURE_OPENAI_KEY: ")
            global azure_openai_deployment
            azure_openai_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")
            if azure_openai_deployment == None:
                azure_openai_deployment = input("\nEnvironment variable AZURE_OPENAI_DEPLOYMENT is not found on your machine, please input AZURE_OPENAI_DEPLOYMENT: ")
    log_thread('api_selection:'+api_selection)
    
    WinDbg_path = os.getenv("WinDbg_PATH")
    if WinDbg_path == None:
        WinDbg_path = input("\nEnvironment variable WinDbg_PATH is not found on your machine, please input WinDbg installation path which contains WinDbg.exe: ")

        while not os.path.exists(WinDbg_path):
            print("\nPath does not exist or does not include WinDbg.exe and cdb.exe")
            WinDbg_path = input("\nWinDbg installation path which contains WinDbg.exe and cdb.exe:")
            
    WinDbg_path+=r"\cdb.exe"

    print("\nThis software is used for debugging learning purpose, please do not load any customer data.")
    open_type = ''
    while open_type != '1' and open_type != '2':
        open_type = input("\nDo you want to open dump/trace file or connect to remote debugger? 1 for dump/trace file, 2 for remote debugger: ")
        if open_type == '1':
            # print("\nPlease enter your memory dump file path, only *.dmp or *.run files are supported")
            # speak("Please enter your memory dump file path.")

            dumpfile_path = input("\nPlease enter your memory dump file path, only *.dmp or *.run files are supported. Memory dump file path: ").lower()

            while not (os.path.exists(dumpfile_path) and (dumpfile_path.endswith('.dmp') or dumpfile_path.endswith('.run'))):
                print("\nFile does not exist or type is not *.dmp or *.run")
                # speak("File does not exist")
                dumpfile_path = input("\nMemory dump file path:")
        elif open_type == '2':
            connection_str = input("\nConnection String: ")
            pattern = r'^tcp:Port=(\d+),Server=[A-Za-z0-9\-]+$'

            while not re.match(pattern, connection_str):
                connection_str = input("\nConnection String:")

    log_thread('open_type:'+open_type)

    symbol_path = os.getenv("_NT_SYMBOL_PATH")
    if symbol_path == None:
        symbol_path = 'srv*C:\symbols*https://msdl.microsoft.com/download/symbols'
        print("\nEnvironment variable _NT_SYMBOL_PATH is not found on your machine, set default symbol path to srv*C:\symbols*https://msdl.microsoft.com/download/symbols")

    # command = r'C:\Program Files\Debugging Tools for Windows (x64)\cdb.exe'
    arguments = [WinDbg_path]
    if open_type == '1':
        arguments.extend(['-z', dumpfile_path])  # Dump file
    elif open_type == '2':
        arguments.extend(['-remote', connection_str])  # Dump file
    arguments.extend(['-y', symbol_path])  # Symbol path, may use sys.argv[1]
    arguments.extend(['-c', ".echo Command Completed"])
    global process,reader
    process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    reader = ReaderThread(process.stdout)
    reader.start()

    log_thread('arguments:'+' '.join(arguments))

    if get_results() == "timeout":
        if open_type == '1':
            print(dumpfile_path + "open failed.")
        elif open_type == '2':
            print(connection_str + "connection failed.")
        return

    results = dbg("||")
    log_thread('dump:'+results)

    user_input = input("\nDo you want to load any debugger extensions? Debugger extension dll path: ")
    log_thread("debugger extension dll path:"+user_input)
    last_debugger_output = dbg(".load " + user_input)
    if last_debugger_output == "timeout":
        print(user_input+" timeout")
    else:
        global debugger_extension
        debugger_extension = "Debug extension " + user_input + " has been loaded."

    user_input = input("\nDo you want to add any symbol file path? Symbol file path: ")
    log_thread("symbol file path:"+user_input)
    last_debugger_output = dbg(".sympath+\"" + user_input + "\"")
    if last_debugger_output == "timeout":
        print(user_input+" timeout")

    help_msg = '''
Hello, I am WinDbg Copilot, I'm here to assist you.

The given commands are used to interact with WinDbg Copilot, a tool that utilizes the OpenAI model for assistance with debugging. The commands include:

    !auto: auto mode, user provides a problem description, ChatGPT can reply with simple explanations or suggesting a single command to execute to further analyze the problem. Ask user to execute the suggested command or not.
    !chat: chat mode, user inputs are forwarded to ChatGPT, ChatGPT can reply with simple answers or suggesting a single command to execute to further analyze the problem.
    !command: command mode, user inputs are forwarded to debugger like manual debugging in WinDbg, debugger outputs are forwarded to ChatGPT, ChatGPT can reply with simple explanations or suggesting a single command to execute to further analyze the problem. User will decide to execute the suggested command or not.
    !quit or !q or q or qq: Terminates the debugger session.
    !help or !h: Provides help information.

Note: WinDbg Copilot requires an active Internet connection to function properly, as it relies on Openai API.
    '''
    
    print(help_msg)
 
    last_debugger_output = ""
    # last_Copilot_output = ""
    mode = "auto"
    while True:
        # Prompt the user for input
        if mode == "auto":
            problem_description = input("Problem description: ")
            log_thread("Problem description:"+problem_description)
            last_Copilot_output = UpdatePrompt(problem_description)
            auto(last_Copilot_output)
            mode = "chat"
        elif mode == "chat":
            user_input = input("\n"+'Chat> ')
            if user_input == "!auto":
                mode = "auto"
                print("\nauto mode.")
                continue
            elif user_input == "!chat":
                mode = "chat"
                print("\nchat mode.")
                continue
            elif user_input == "!command":
                mode = "command"
                print("\ncommand mode.")
                continue
            elif user_input == "!quit" or user_input == "!q" or user_input == "q" or user_input == "qq":
                text = "Goodbye, have a nice day!"
                print(text)
                dbg("qq")
                break
            elif user_input == "!help" or user_input == "!h":
                print(help_msg)
                continue
            SendCommand(user_input)
        elif mode == "command":
            user_input = input("\n"+'Command> ')
            print("\n")
            if user_input == "!auto":
                mode = "auto"
                print("\nauto mode.")
                continue
            elif user_input == "!chat":
                mode = "chat"
                print("\nchat mode.")
                continue
            elif user_input == "!command":
                mode = "command"
                print("\ncommand mode.")
                continue
            elif user_input == "!quit" or user_input == "!q" or user_input == "q" or user_input == "qq":
                text = "Goodbye, have a nice day!"
                print(text)
                dbg("qq")
                break
            elif user_input == "!help" or user_input == "!h":
                print(help_msg)
                continue
            last_debugger_output = dbg(user_input)
            if last_debugger_output == "timeout":
                print(user_input+" timeout")
                continue
            SendCommand(user_input+"\n"+last_debugger_output)
        log_thread("user_input:"+user_input)
        # trim_user_input = get_characters_after_first_whitespace(user_input)
        
    log_thread('process exit') 

def read_config():
    # Reading configuration
    config = configparser.ConfigParser()
    # Assuming this line is at the top-level scope of your module:
    CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(CONFIG_PATH)
    global api_selection, model_selection
    api_selection = config['API_SELECTION'].get('choice', '1')  # Defaulting to '1' if not found
    model_selection = config['MODEL_SELECTION'].get('choice', '1')  # Defaulting to '1' if not found

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY", "")
    global AZURE_OPENAI_DEPLOYMENT
    AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")

    openai.api_key = OPENAI_API_KEY if api_selection=='1' else AZURE_OPENAI_KEY
    if api_selection == '2':
        openai.api_type = 'azure'
        openai.api_base = AZURE_OPENAI_ENDPOINT
        openai.api_version = '2023-05-15'
    elif api_selection == '1':
        openai.api_type = 'open_ai'
        openai.api_base = 'https://api.openai.com/v1'
        openai.api_version = None

def run(open_type, dumpfile_path, connection_str):
    # read_config()

    WinDbg_path = os.environ.get("WinDbg_path", "")
    symbol_path = os.environ.get("_NT_SYMBOL_PATH", "")

    WinDbg_path+=r"\cdb.exe"
    arguments = [WinDbg_path]
    if open_type == 1:
        arguments.extend(['-z', dumpfile_path])  # Dump file
    elif open_type == 2:
        arguments.extend(['-remote', connection_str])  # Dump file
    arguments.extend(['-y', symbol_path])  # Symbol path, may use sys.argv[1]
    arguments.extend(['-c', ".echo Command Completed"])
    global process,reader
    process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    reader = ReaderThread(process.stdout)
    reader.start()

    log_thread('arguments:'+' '.join(arguments))

    results = get_results()
    if results == "timeout":
        if open_type == '1':
            print(dumpfile_path + "open failed.")
        elif open_type == '2':
            print(connection_str + "connection failed.")
        return
    left_text.insert(tk.END, results)
    left_text.see(tk.END)

    results = dbg("||")
    left_text.insert(tk.END, results)
    left_text.see(tk.END)

    log_thread('dump:'+results)

def main():
    global session_uuid
    session_uuid = generate_uuid()

    log_thread('process start')

    def on_closing():
        if 'process' in globals():
            dbg('qq')
        root.destroy()

    # Create the main window.
    root = tk.Tk()
    ICON_PATH = os.path.join(os.path.dirname(__file__), 'thumbnail.ico')
    root.iconbitmap(ICON_PATH)
    # root.iconbitmap('thumbnail.ico')
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.geometry('1280x720')
    root.title('WinDbg Copilot')

    # Create the PanedWindow.
    paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=1)

    # To create a frame on the left side which will hold the text widget, the entry, and the scrollbar.
    left_frame = tk.Frame(paned_window)
    paned_window.add(left_frame)

    global left_text
    # Create the left Text widget and place it inside the left frame using grid.
    left_text = tk.Text(left_frame, wrap=tk.WORD)
    left_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # Configure the grid geometry manager for left_frame.
    left_frame.grid_rowconfigure(0, weight=1)   # This allows the left_text to expand.
    left_frame.grid_columnconfigure(0, weight=1) # This allows the left_text to expand.

    # Create a Scrollbar and associate it with left_text.
    scrollbar = tk.Scrollbar(left_frame, command=left_text.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Link the scrollbar and the text widget.
    left_text['yscrollcommand'] = scrollbar.set

    # Create the Entry widget below the left_text widget and add it to the left frame.
    left_entry = tk.Entry(left_frame)
    left_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    left_entry.config(state=tk.DISABLED)

    # To create a frame on the right side which will hold the text widget and the entry.
    right_frame = tk.Frame(paned_window)
    paned_window.add(right_frame)

    # Create a Label widget with the text "Problem description:" and place it in the right frame using grid.
    problem_description_label = tk.Label(right_frame, text="Problem description:")
    problem_description_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    # Create the Entry widget and place it at the top of the right frame using grid.
    right_entry = tk.Entry(right_frame)
    right_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    right_entry.config(state=tk.DISABLED)

    # Configure the grid geometry manager for right_frame.
    right_frame.grid_rowconfigure(2, weight=1)   # This allows the right_text to expand.
    right_frame.grid_columnconfigure(0, weight=1) # This allows the right_text to expand.

    # Create the right Text widget and place it below the right_entry widget in the right frame.
    right_text = tk.Text(right_frame, wrap=tk.WORD)
    right_text.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)


    # Define function to get input from Entry widget
    def get_input_left(event):
        input_value = left_entry.get()
        send_output_left(f"{input_value}\n")
        last_debugger_output = dbg(input_value)
        send_output_left(f"{last_debugger_output}\n")
        left_entry.delete(0, 'end')  # clear the entry field

    # Define function to send output to text widget
    def send_output_left(output):
        left_text.insert(tk.END, output)
        left_text.see(tk.END)

    disclaimer = """Disclaimer: WinDbg Copilot

WinDbg Copilot is an application designed for debugging learning purposes only. It is important to note that this application should not be used to load or handle any customer data. WinDbg Copilot is intended solely for the purpose of providing a platform for debugging practice and learning experiences.

When using WinDbg Copilot, please be aware that any debugging input and output generated during your debugging sessions will be sent to OpenAI or Azure OpenAI according to your selection. This data may be used for analysis and improvement of the application's performance and capabilities. However, it is crucial to understand that no customer data should be loaded or shared through WinDbg Copilot.

WinDbg Copilot project takes the privacy and security of user information seriously and endeavors to handle all data with utmost care and in accordance with applicable laws and regulations. Nevertheless, it is strongly recommended to refrain from providing any sensitive or confidential information while using WinDbg Copilot.

By using WinDbg Copilot, you acknowledge and agree that any debugging input and output you generate may be transmitted to OpenAI or Azure OpenAI for research and development purposes. You also understand that WinDbg Copilot should not be used with customer data and that WinDbg Copilot project is not responsible for any consequences that may arise from the misuse or mishandling of such data.

Please ensure that you exercise caution and adhere to best practices when utilizing WinDbg Copilot to ensure the privacy and security of your own data. WinDbg Copilot project will not be held liable for any damages, losses, or unauthorized access resulting from the misuse of this application.

By proceeding to use WinDbg Copilot, you signify your understanding and acceptance of these terms and conditions."""
    send_output_left(disclaimer)

    link_num = 0

    def ai_assistant(last_Copilot_output):
        global link_num
        pattern = r'<exec>(.*?)<\/exec>'
        matches = re.findall(pattern, last_Copilot_output)
        if matches:
            for match in matches:
                def on_link_click(link_text, event=None):
                    # This function will be executed when the link is clicked.
                    send_output_right("\nThinking...\n")

                    log_thread("execute command:"+link_text)
                    send_output_left(f"\n{link_text}\n")
                    last_debugger_output = dbg(link_text)
                    send_output_left(f"\n{last_debugger_output}\n")
                    if last_debugger_output == "timeout":
                        print(match+" timeout")
                    
                    last_Copilot_output = SendCommand(last_debugger_output)
                    send_output_right(f"\n{last_Copilot_output}\n")
                    ai_assistant(last_Copilot_output)
                    print(f"Link {link_text} clicked!")

                def on_link_enter(event):
                    right_text.config(cursor="hand2")

                def on_link_leave(event):
                    right_text.config(cursor="arrow")

                # Insert some text
                right_text.insert(tk.END, "\nClick on the link: ")

                # Insert the clickable link
                # start_index = right_text.index(tk.END)  # Get the current end index
                tag_name = "clickableLink"+str(link_num)
                right_text.insert(tk.END, f"{match}\n", (tag_name,))  # Insert text with a tag
                # end_index = right_text.index(tk.END)  # Get the new end index
                right_text.see(tk.END)

                # Configure the tag to make it look like a link
                right_text.tag_configure(tag_name, foreground="blue", underline=1)

                # Bind the click event on the tag to a function with lambda
                right_text.tag_bind(tag_name, "<Button-1>", lambda event, link=match: on_link_click(link, event))
                # Bind the enter and leave events for changing the cursor
                right_text.tag_bind(tag_name, "<Enter>", on_link_enter)
                right_text.tag_bind(tag_name, "<Leave>", on_link_leave)
                link_num += 1
        else:
            print("\nNo more command suggested.")
            send_output_right("\nNo more command suggested.\n")

    # Define function to get input from Entry widget
    def get_input_right(event):
        read_config()
        problem_description = right_entry.get()
        log_thread("Problem description:"+problem_description)
        send_output_right(f"\nThinking...\n")
        last_Copilot_output = UpdatePrompt(problem_description)
        send_output_right(f"\n{last_Copilot_output}\n")
        ai_assistant(last_Copilot_output)

        # send_output_right(f"{last_Copilot_output}\n")
        # right_entry.delete(0, 'end')  # clear the entry field

    # Define function to send output to text widget
    def send_output_right(output):
        right_text.insert(tk.END, output)
        right_text.see(tk.END)
        
    # Bind Return key to get_input
    left_entry.bind('<Return>', get_input_left)

    # Bind Return key to get_input
    right_entry.bind('<Return>', get_input_right)

    # Define actions for menu items
    def open_file():
        dumpfile_path = filedialog.askopenfilename()
        if dumpfile_path != "":
            run(1,dumpfile_path,"")
            left_entry.config(state=tk.NORMAL)
            left_entry.delete(0, tk.END)
            right_entry.config(state=tk.NORMAL)
            right_entry.delete(0, tk.END)
            file_menu.entryconfig("Open dump/trace file", state=tk.DISABLED)
            file_menu.entryconfig("Connect to remote debugger", state=tk.DISABLED)

    def remote_debugging():
        # Create a new window.
        debugging_window = tk.Toplevel()
        debugging_window.title("Remote Debugging")
        debugging_window.geometry("500x200")  # Adjusted for new content

        # Create the label and align it to the left.
        label = ttk.Label(debugging_window, text="Connection string:", anchor="w")
        label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)

        # Create the entry widget.
        connection_entry = ttk.Entry(debugging_window)
        connection_entry.grid(row=1, column=0, padx=10, pady=5, sticky=tk.EW)

        # Example text label
        example_text = """Examples:
    npipe:server=Server,pipe=PipeName[,password=Password]
    tcp:server=Server,port=Socket[,password=Password]

For more information, see https://aka.ms/windbgremote"""
        example_label = ttk.Label(debugging_window, text=example_text, anchor="w")
        example_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        # Ensure the entry expands horizontally with the window.
        debugging_window.grid_columnconfigure(0, weight=1)

        # Function to save the entry's value to connection_str and close the window.
        def save_connection():
            global connection_str
            connection_str = connection_entry.get()
            debugging_window.destroy()  # Close the window.
            if connection_str != "":
                run(2, "", connection_str)
                left_entry.config(state=tk.NORMAL)
                left_entry.delete(0, tk.END)
                right_entry.config(state=tk.NORMAL)
                right_entry.delete(0, tk.END)
                file_menu.entryconfig("Open dump/trace file", state=tk.DISABLED)
                file_menu.entryconfig("Connect to remote debugger", state=tk.DISABLED)
                left_entry.config(state=tk.NORMAL)
                left_entry.delete(0, tk.END)
                right_entry.config(state=tk.NORMAL)
                right_entry.delete(0, tk.END)
                file_menu.entryconfig("Open dump/trace file", state=tk.DISABLED)
                file_menu.entryconfig("Connect to remote debugger", state=tk.DISABLED)

        # Create the OK button and align it to the right.
        ok_button = ttk.Button(debugging_window, text="OK", command=save_connection)
        ok_button.grid(row=3, column=0, pady=10, padx=10, sticky=tk.E)

        # Run the window's main loop.
        debugging_window.mainloop()

    # Create Menu widget
    menubar = Menu(root)
    root.config(menu=menubar)

    # Create File Menu
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open dump/trace file", command=open_file)
    file_menu.add_command(label="Connect to remote debugger", command=remote_debugging)

    menubar.add_command(label="Settings", command=lambda: create_settings_window(root))

    def create_entry(window, row, env_variable, label_text):
        label = ttk.Label(window, text=label_text)
        label.grid(row=row, column=0, sticky='w')
        entry = ttk.Entry(window)
        entry.insert(0, os.environ.get(env_variable, ""))
        entry.grid(row=row, column=1, sticky='ew')
        return label, entry

    def save_settings(entries, api, model, settings_window):
        global api_selection, model_selection
        api_selection = api.get()
        model_selection = model.get()
        # 1. Save radio button selections to config.ini
        config = configparser.ConfigParser()

        config['API_SELECTION'] = {'choice': api_selection}
        config['MODEL_SELECTION'] = {'choice': model_selection}

        # Assuming this line is at the top-level scope of your module:
        CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)

        # 2. Save entries to environment variables for the current session
        for key, entry_tuple in entries.items():
            os.environ[key] = entry_tuple[1].get()

        # 3. Save entries to environment variables permanently (on Windows)
        for key, entry_tuple in entries.items():
            # For user-specific environment variable:
            subprocess.call(['setx', key, entry_tuple[1].get()])

            # For system-wide environment variable (requires administrative privileges):
            # subprocess.call(['setx', key, entry_tuple[1].get(), '/M'])

        read_config()
        messagebox.showinfo("Success", "Settings saved successfully!")
        settings_window.destroy()

    def create_settings_window(root):

        def update_model_buttons():
            if api_selection.get() == "2":  # Azure OpenAI
                lb_model.config(foreground='grey')
                rb_gpt3_5.config(state=tk.DISABLED)
                rb_gpt4.config(state=tk.DISABLED)
                for key in ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_KEY", "AZURE_OPENAI_DEPLOYMENT"]:
                    entries[key][0].config(foreground='black')  # Label
                    entries[key][1].config(state=tk.NORMAL)     # Entry
                entries["OPENAI_API_KEY"][0].config(foreground='grey')  # Label
                entries["OPENAI_API_KEY"][1].config(state=tk.DISABLED)  # Entry
            else:  # OpenAI API
                lb_model.config(foreground='black')
                rb_gpt3_5.config(state=tk.NORMAL)
                rb_gpt4.config(state=tk.NORMAL)
                entries["OPENAI_API_KEY"][0].config(foreground='black')  # Label
                entries["OPENAI_API_KEY"][1].config(state=tk.NORMAL)     # Entry
                for key in ["AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_KEY", "AZURE_OPENAI_DEPLOYMENT"]:
                    entries[key][0].config(foreground='grey')  # Label
                    entries[key][1].config(state=tk.DISABLED)  # Entry

        settings_window = tk.Toplevel(root)
        settings_window.geometry("800x300")
        settings_window.title("Settings")
        settings_window.columnconfigure(1, weight=1)  # configure column to expand

        # Reading configuration
        config = configparser.ConfigParser()
        # Assuming this line is at the top-level scope of your module:
        CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.ini')
        config.read(CONFIG_PATH)
        api_choice = config['API_SELECTION'].get('choice', '1')  # Defaulting to '1' if not found
        model_choice = config['MODEL_SELECTION'].get('choice', '1')  # Defaulting to '1' if not found

        ttk.Label(settings_window, text="Do you want to use OpenAI API or Azure OpenAI?").grid(row=0, column=0, sticky='w', columnspan=2)
        api_selection = tk.StringVar(value=api_choice)
        ttk.Radiobutton(settings_window, text="OpenAI API", variable=api_selection, value="1", command=update_model_buttons).grid(row=1, column=0, sticky='w')
        ttk.Radiobutton(settings_window, text="Azure OpenAI", variable=api_selection, value="2", command=update_model_buttons).grid(row=1, column=1, sticky='w')

        lb_model = ttk.Label(settings_window, text="Do you want to use model gpt-3.5-turbo-16k or model gpt-4?")
        lb_model.grid(row=2, column=0, sticky='w', columnspan=2)

        model_selection = tk.StringVar(value=model_choice)
        rb_gpt3_5 = ttk.Radiobutton(settings_window, text="gpt-3.5-turbo-16k", variable=model_selection, value="1")
        rb_gpt3_5.grid(row=3, column=0, sticky='w')
        rb_gpt4 = ttk.Radiobutton(settings_window, text="gpt-4", variable=model_selection, value="2")
        rb_gpt4.grid(row=3, column=1, sticky='w')

        entries = {
            "OPENAI_API_KEY": create_entry(settings_window, 4, "OPENAI_API_KEY", "OpenAI API Key:"),
            "AZURE_OPENAI_ENDPOINT": create_entry(settings_window, 5, "AZURE_OPENAI_ENDPOINT", "Azure OpenAI Endpoint:"),
            "AZURE_OPENAI_KEY": create_entry(settings_window, 6, "AZURE_OPENAI_KEY", "Azure OpenAI Key:"),
            "AZURE_OPENAI_DEPLOYMENT": create_entry(settings_window, 7, "AZURE_OPENAI_DEPLOYMENT", "Azure OpenAI Deployment:"),
            "WinDbg_PATH": create_entry(settings_window, 8, "WinDbg_PATH", "WinDbg Path:"),
            "_NT_SYMBOL_PATH": create_entry(settings_window, 9, "_NT_SYMBOL_PATH", "NT Symbol Path:")
        }

        # Update model buttons to match loaded API selection
        update_model_buttons()

        ttk.Button(settings_window, text="Save", command=lambda: save_settings(entries, api_selection, model_selection, settings_window)).grid(row=10, column=1, sticky='e')

    root.mainloop()

if __name__ == "__main__":
    main()