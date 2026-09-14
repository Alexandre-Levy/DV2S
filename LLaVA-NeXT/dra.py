from llava.model.builder import load_pretrained_model
from llava.mm_utils import get_model_name_from_path, process_images, tokenizer_image_token
from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN, IGNORE_INDEX
from llava.conversation import conv_templates, SeparatorStyle
from PIL import Image
import requests
import copy
import torch
import sys
import warnings
from decord import VideoReader, cpu
import numpy as np
import os
from decord import VideoReader, cpu
warnings.filterwarnings("ignore")
file_path = "/home/alevy/phd/code/Qwen-VL/questions.txt"
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

def load_video(video_path, max_frames_num,fps=1,force_sample=False):
    if max_frames_num == 0:
        return np.zeros((1, 336, 336, 3))
    
    vr = VideoReader(video_path, ctx=cpu(0), num_threads=1)
    total_frame_num = len(vr)
    video_time = total_frame_num / vr.get_avg_fps()
    fps = round(vr.get_avg_fps()/fps)
    frame_idx = [i for i in range(0, len(vr), fps)]
    frame_time = [i/fps for i in frame_idx]
    if len(frame_idx) > max_frames_num or force_sample:
        sample_fps = max_frames_num
        uniform_sampled_frames = np.linspace(0, total_frame_num - 1, sample_fps, dtype=int)
        frame_idx = uniform_sampled_frames.tolist()
        frame_time = [i/vr.get_avg_fps() for i in frame_idx]
    frame_time = ",".join([f"{i:.2f}s" for i in frame_time])
    spare_frames = vr.get_batch(frame_idx).asnumpy()
    # import pdb;pdb.set_trace()
    return spare_frames,frame_time,video_time
pretrained = "lmms-lab/LLaVA-Video-72B-Qwen2"
model_name = "llava_qwen"
device = "cuda"
device_map = "auto"
tokenizer, model, image_processor, max_length = load_pretrained_model(pretrained, None, model_name, torch_dtype="bfloat16", device_map=device_map)  # Add any other thing you want to pass in llava_model_args
model = torch.nn.DataParallel(model, device_ids=[0, 1,2,3,4,5])
model.eval()
i=0
for question, video in zip(questions, video_paths):
    print(video)
    print(question)
    max_frames_num = 64
    video,frame_time,video_time = load_video(video, max_frames_num, 1, force_sample=True)
    video = image_processor.preprocess(video, return_tensors="pt")["pixel_values"].cuda().bfloat16()
    video = [video]
    conv_template = "qwen_1_5"  # Make sure you use correct chat template for different models
    # time_instruciton = f"The video lasts for {video_time:.2f} seconds, and {len(video[0])} frames are uniformly sampled from it. These frames are located at {frame_time}.Please answer the following questions related to this video."
    question = DEFAULT_IMAGE_TOKEN + question #  f"\n{time_instruciton}\nPlease describe this video in detail."
    conv = copy.deepcopy(conv_templates[conv_template])
    conv.append_message(conv.roles[0], question)
    conv.append_message(conv.roles[1], None)
    prompt_question = conv.get_prompt()
    input_ids = tokenizer_image_token(prompt_question, tokenizer, IMAGE_TOKEN_INDEX, return_tensors="pt").unsqueeze(0).to(device)
    # print(f"Video tensor shape: {video[0].shape}, dtype: {video[0].dtype}, device: {video[0].device}")
    cont = model.module.generate(
        input_ids,
        images=video,
        modalities= ["video"],
        do_sample=False,
        temperature=0,
        max_new_tokens=4096,
    )
    text_outputs = tokenizer.batch_decode(cont, skip_special_tokens=True)[0].strip()
    print(text_outputs)
    # i+=1
    # if i > 10:
    #     exit(-1)
torch.cuda.empty_cache()