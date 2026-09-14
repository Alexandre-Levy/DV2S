from openai import OpenAI
import cv2
import base64
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

prompts_dir = os.path.join(os.getcwd(), "prompts")
rules_path = os.path.join(prompts_dir, "rules.txt")
template_path = os.path.join(prompts_dir, "template.txt")
manifest_path = os.path.join(prompts_dir, "examples_manifest.txt")
examples_dir = os.path.join(prompts_dir, "examples")
examples_path = os.path.join(os.getcwd(), "dra_sg_examples.txt")
folder_result = "results_scenic/"


def load_example(file_name):
    with open(os.path.join(examples_dir, file_name), "r") as f:
        header, _, code = f.read().partition("\n\n")
    prefix = "# Description:"
    if header.startswith(prefix):
        header = header[len(prefix):]
    description = header.strip()
    return f"Description:\n{description}\nCode:\n{code.rstrip()}\n"


def build_prompt_scenario_base():
    with open(rules_path, "r") as f:
        rules = f.read().rstrip()

    with open(manifest_path, "r") as f:
        example_files = [line.strip() for line in f.readlines() if line.strip()]
    examples = "\n".join(load_example(name) for name in example_files)

    with open(template_path, "r") as f:
        template = f.read()

    return f"{rules}\n\nHere are examples: \n{examples}\n{template}"


prompt_scenario_base = build_prompt_scenario_base()

with open(examples_path, "r") as f:
    video_paths = [line.strip() for line in f.readlines() if line.strip()]

os.makedirs(folder_result, exist_ok=True)


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


def analyze_video(video_path):
    frames = extract_frames(video_path)

    question = " What driving case happened in this driving video that could have caused an accident ? The maneuver causing the potential accident can also come from the other cars(a sudden brake, deceleration, speeding, ...). What maneuver is doing the ego vehicle at the potential accident moment (decelerating, braking, turn left, turn right, follow lane ...)? At an intersection, it can only turn left or turn right or follow lane. With what type of actors (pedestrians, cars , objects, wall) ? How many actors are there from the end to the beginning ? If it is a vehicle at an intersection, from what side of the intersection they were coming, considering the initial coming lane of the ego vehicle ? ( If the ego is turning left at an intersection and the vehicle is on its right at the end of the turn, it comes from the opposite lane. If it is the case, just tell me that it is coming from the opposite lane) Describe the behaviors of the other actors, what might have been difficult for the car to assess. If there is a pedestrian involved in the scene, please describe the pedestrian's behavior (from which side, frontal, sidelanes or other lanes and speed) and if an object (parked car on the right sidewalks, bus stop,  advertising panel, bin, other persons, a parked car,...) altered the sight of the car of the pedestrian. If a pedestrian crosses, explicitly state: initial side (relative to ego), final side (relative to ego), direction of motion (left to right or right to left). If the final frame of the pedestrian appearing is on the left, it was crossing from right to left. If you are not 100% sure about the side, say “uncertain” instead of guessing."
    question = "This is a video of the ego car from a camera attached to the back of the vehicle." + question + "And what road section is this ? (highway, T-intersection, highway entry ramp, highway exit ramp, intersection, straight road,  three way road). The highway entry ramps can be really curvy. Differentiate well an entry or exit highway ramp from intersections. Give a 3 sentences answer."

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
        "model": "gpt-4.1",
        "messages": PROMPT_MESSAGES,
        "max_tokens": 400,
        "temperature": 0.0,
    }

    result = client.chat.completions.create(**params)
    return result.choices[0].message.content


def generate_scenic(description):
    prompt_scenario = prompt_scenario_base.replace("***DESCRIPTION_TO_REPLACE***", description)

    PROMPT_MESSAGES = [
        {
            "role": "user",
            "content": prompt_scenario,
        },
    ]
    params = {
        "model": "gpt-4o",
        "messages": PROMPT_MESSAGES,
        "max_tokens": 2000,
        "temperature": 0.0,
    }

    result = client.chat.completions.create(**params)
    print_result = result.choices[0].message.content

    if "```scenic" in print_result:
        print_result = print_result.split("```scenic")[1].split("```")[0]
    elif "```python" in print_result:
        print_result = print_result.split("```python")[1].split("```")[0]

    return print_result


for video_path in video_paths:
    print(video_path)
    video_name = os.path.basename(video_path).split("_images")[0].rsplit(".", 1)[0]

    print("Analyzing video...")
    description = analyze_video(video_path)
    print(description)

    with open(folder_result + video_name + ".txt", "w") as f:
        f.write(description)

    print("Generating Scenic script...")
    scenic_code = generate_scenic(description)

    new_name = folder_result + video_name + ".scenic"
    with open(new_name, "w") as f:
        f.write(scenic_code)

    print("Saved:", new_name)
