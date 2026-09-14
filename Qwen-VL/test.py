from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
torch.manual_seed(1234)

import os

# Define the file path
file_path = "questions.txt"

# Initialize lists to store video paths and questions
video_paths = []
questions = []
videos_location = "/home/alevy/phd/videos/CARLA/filtered/"
# Read the file and process its content
with open(file_path, "r") as file:
    lines = file.readlines()

    current_video = None
    current_question = []

    for line in lines:
        line = line.strip()
        if line.endswith(".mp4"):
          line = line.split("/")[-1]
          line = videos_location + line
          video_paths.append(line)
        if line.startswith("This is a video of the ego car from a camera attached to the back of the vehicle."):
          questions.append(line)



# Note: The default behavior now has injection attack prevention off.
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)

# use bf16
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat", device_map="auto", trust_remote_code=True, bf16=True).eval()
# use fp16
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat", device_map="auto", trust_remote_code=True, fp16=True).eval()
# use cpu only
# model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat", device_map="cpu", trust_remote_code=True).eval()
# use cuda device
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen-VL-Chat", device_map="cuda", trust_remote_code=True).eval()

# Specify hyperparameters for generation
model.generation_config = GenerationConfig.from_pretrained("Qwen/Qwen-VL-Chat", trust_remote_code=True)

# 1st dialogue turn
for question, video in zip(questions, video_paths):
  query = tokenizer.from_list_format([
      {'video': video}, # Either a local path or an url
      {'text': question},
  ])
  response, history = model.chat(tokenizer, query=query, history=None)
  print(response)
  