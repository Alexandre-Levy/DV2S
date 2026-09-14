from openai import OpenAI
import cv2
import base64
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

examples_path = os.path.join(os.getcwd(), "dra_examples.txt")
output_path = os.path.join(os.getcwd(), "dra_file_results.txt")

video_paths = []
questions = []

with open(examples_path, "r") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

for i, line in enumerate(lines):
    if i % 2 == 0:
        video_paths.append(line)
    else:
        questions.append(line)


def extract_frames(video_path, stride=7):
    video_capture = cv2.VideoCapture(video_path)
    base64_frames = []
    while video_capture.isOpened():
        success, frame = video_capture.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64_frames.append(base64.b64encode(buffer).decode("utf-8"))
    video_capture.release()

    sampled_frames = base64_frames[0::stride]
    if base64_frames and base64_frames[-1] not in sampled_frames:
        sampled_frames.append(base64_frames[-1])
    return sampled_frames


def query_video(question, video_path):
    frames = extract_frames(video_path)

    PROMPT_MESSAGES = [
        {
            "role": "user",
            "content": [
                *map(
                    lambda x: {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{x}"},
                    },
                    frames,
                ),
                {"type": "text", "text": question},
            ],
        },
    ]
    params = {
        "model": "gpt-4o",
        "messages": PROMPT_MESSAGES,
        "max_tokens": 400,
        "temperature": 0.0,
    }
    result = client.chat.completions.create(**params)
    return result.choices[0].message.content


with open(output_path, "w") as out_f:
    for video, question in zip(video_paths, questions):
        print(video)
        print(question)

        answer = query_video(question, video)
        print(answer)

        out_f.write(video + "\n")
        out_f.write(question + "\n")
        out_f.write(answer + "\n\n")

print("Saved:", output_path)
