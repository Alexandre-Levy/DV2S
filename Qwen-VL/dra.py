from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer, AutoProcessor
from qwen_vl_utils import process_vision_info

model = Qwen2VLForConditionalGeneration.from_pretrained(
    "Qwen/Qwen2-VL-72B-Instruct", torch_dtype="auto", device_map="auto"
)

processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-72B-Instruct")
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


def query_video(prompt, use_frames=True, frames_path="/home/qwen2_vl/content/frames", video_path=None):
    if use_frames:
        # Get the frames
        selected_frames = get_frame_list(output_path)

        # Create messages structure for frames
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "video",
                        "video": selected_frames,
                        "fps": 1.0,
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ]
    else:
        # Create messages structure for the entire video
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "video",
                        "video": f"file://{video_path}",
                        "max_pixels": 360 * 420,
                        "fps": 1.0,
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ]

    # print(f"Using {'frames' if use_frames else 'entire video'} for inference.")

    # Preparation for inference
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(
        text=[text],
        images=image_inputs,
        videos=video_inputs,
        padding=True,
        return_tensors="pt",
    )
    inputs = inputs.to("cuda")

    # Inference
    with torch.no_grad():  # Use no_grad to save memory during inference
        generated_ids = model.generate(**inputs, max_new_tokens=128)

    # Trim the generated output to remove the input prompt
    generated_ids_trimmed = [
        out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
    ]

    # Decode the generated text
    output_text = processor.batch_decode(
        generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )

    print(output_text[0])

# 1st dialogue turn
i = 0
for question, video in zip(questions, video_paths):
  print(video)
  print(question)
  query_video(question, use_frames=False, frames_path="", video_path=video)
  i+=1
#   if i > 10:
#     exit(-1)
torch.cuda.empty_cache()
