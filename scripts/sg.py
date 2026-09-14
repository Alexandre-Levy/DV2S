from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

prompts_dir = os.path.join(os.getcwd(), "prompts")
rules_path = os.path.join(prompts_dir, "rules.txt")
template_path = os.path.join(prompts_dir, "template.txt")
manifest_path = os.path.join(prompts_dir, "examples_manifest.txt")
examples_dir = os.path.join(prompts_dir, "examples")
examples_path = os.path.join(os.getcwd(), "sg_examples.txt")
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
    descriptions = [line.strip() for line in f.readlines() if line.strip()]

os.makedirs(folder_result, exist_ok=True)

for i, description in enumerate(descriptions):
    print(description)

    prompt_scenario = prompt_scenario_base.replace("***DESCRIPTION_TO_REPLACE***", description)

    # with open(folder_result + "scenario_%02d.txt" % i, "w") as f:
    #     f.write(description)

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

    # save prompt message and result to a file
    # with open(folder_result + "scenario_%02d.txt" % i, "w") as f:
    #     f.write(f"Prompt: {prompt_scenario}")

    new_name = folder_result + "scenario_%02d.scenic" % i
    with open(new_name, "w") as f:
        f.write(print_result)

    print("Saved:", new_name)
