import os
import subprocess


def get_llama_2_instance():

  # Define the file name
  file_name = "llama-2-13b-chat.ggmlv3.q4_0.bin"

  # Define the directories to check
  directories_to_check = [
    "llama.cpp/models/",  # Relative path from current working directory
    os.path.expanduser("~") + "/llama.cpp/models/",  # Path in home directory
    "/"  # Global path
  ]

  # Check for the file in each directory
  for directory in directories_to_check:
    path = os.path.join(directory, file_name)
    if os.path.exists(path):
      model_path = path
      break
  else:
    # If the file was not found, download it
    download_path = os.path.expanduser("~") + "/llama-2/" + file_name
    print(f"Llama-2 not found. Downloading it to {download_path} ...")
    url = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q4_0.bin"
    subprocess.run(f"curl -L '{url}' -o {download_path}", shell=True)
    model_path = download_path

  try:
    from llama_cpp import Llama
  except:
    print("Downloading Llama-2 interface...")
    subprocess.run(["pip", "install", "llama-cpp-python"])
    from llama_cpp import Llama

  print("Llama", Llama)
  print("model_path", model_path)

  # Initialize and return Llama-2
  llama_2 = Llama(model_path=model_path)
  return llama_2
