import os
import subprocess
import appdirs
from rich import print
from rich.markdown import Markdown

def confirm_action(message):
    print('', Markdown(f"### {message}"), '')
    response = input("Proceed? (y/n): ").strip().lower()
    return response == 'y'

def get_llama_2_instance():

    # Define the file name
    file_name = "llama-2-13b-chat.ggmlv3.q4_0.bin"

    # Get user data directory for your application
    user_data_dir = appdirs.user_data_dir("open-interpreter")
    default_path = os.path.join(user_data_dir, "models")

    # Ensure the directory exists
    os.makedirs(default_path, exist_ok=True)

    # Define the directories to check
    directories_to_check = [
        default_path,
        "llama.cpp/models/",
        os.path.expanduser("~") + "/llama.cpp/models/",
        "/"
    ]

    # Check for the file in each directory
    for directory in directories_to_check:
        path = os.path.join(directory, file_name)
        if os.path.exists(path):
            model_path = path
            break
    else:
        # If the file was not found, ask for confirmation to download it
        download_path = os.path.join(default_path, file_name)
        message = f"Llama-2 not found. Would you like to download it to `{download_path}`?"
        if confirm_action(message):
            print(f"Downloading Llama-2 to {download_path} ...")
            url = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q4_0.bin"
            subprocess.run(f"curl -L '{url}' -o {download_path}", shell=True)
            model_path = download_path
        else:
            print("Download cancelled. Exiting.")
            return None

    try:
        from llama_cpp import Llama
    except:
        # Ask for confirmation to install the required pip package
        message = "Llama-2 interface not found. Would you like to install the `llama-cpp-python` package?"
        if confirm_action(message):
            print("Downloading Llama-2 interface...")
            subprocess.run(["pip", "install", "llama-cpp-python"])
            from llama_cpp import Llama
        else:
            print("Installation cancelled. Exiting.")
            return None

    print("Llama", Llama)
    print("model_path", model_path)

    # Initialize and return Llama-2
    llama_2 = Llama(model_path=model_path)
    return llama_2