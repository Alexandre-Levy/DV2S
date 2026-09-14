import gradio as gr
import os
import random
import json
from typing import List, Dict, Tuple
from datetime import datetime
import pandas as pd
from filelock import FileLock, Timeout
import uuid

# -------------------------------
# Manager for Image Comparisons
# -------------------------------
class ImageArenaManager:
    def __init__(self, base_dir: str = "images", data_dir: str = "./data", description_file="scenario_descriptions.txt"):
        self.base_dir = base_dir
        self.data_dir = data_dir
        self.description_file = description_file
        self.image_types = [
            {"name": "Chat Scene", "prefix": "chatscene_"},
            {"name": "LCT", "prefix": "lct_"},
            {"name": "Trajectory", "prefix": "trajectory_"}
        ]
        self.total_sets = 23

        os.makedirs(self.data_dir, exist_ok=True)
        self.data_file = os.path.join(self.data_dir, "arena_data.json")
        self.data_lock = FileLock(os.path.join(self.data_dir, "arena_data.lock"))
        self.data = self._load_data()
        self.usernames = set()
        self.descriptions = self._load_descriptions()

    def _load_data(self) -> Dict:
        """Load or initialize comparison data."""
        try:
            with self.data_lock.acquire(timeout=10):
                if os.path.exists(self.data_file):
                    with open(self.data_file, "r") as f:
                        return json.load(f)
                else:
                    data = {"results": {"comparisons": []}}
                    with open(self.data_file, "w") as f:
                        json.dump(data, f, indent=2)
                    return data
        except Timeout:
            return {"results": {"comparisons": []}}

    def _load_descriptions(self) -> Dict[int, str]:
        """Load scenario descriptions from a file."""
        descriptions = {}
        try:
            with open(self.description_file, "r") as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:self.total_sets]):
                    descriptions[i + 1] = line.strip()
        except FileNotFoundError:
            descriptions = {i + 1: f"Scenario {i + 1} description not available." for i in range(self.total_sets)}
        return descriptions

    def load_random_set(self) -> Tuple[List[str], List[str], int, str]:
        """Select a random image set and shuffle the order."""
        set_index = random.randint(1, self.total_sets)
        images = []
        labels = []
        for it in self.image_types:
            filename = f"{it['prefix']}{str(set_index).zfill(2)}.png"
            images.append(os.path.join(self.base_dir, filename))
            labels.append(it["name"])

        combined = list(zip(images, labels))
        random.shuffle(combined)
        images, labels = zip(*combined)

        description = self.descriptions.get(set_index, "No description available.")
        return list(images), list(labels), set_index, description

    def save_comparison(self, set_index: int, ratings: Dict[str, int], winner: str, username: str):
        """Save user ratings and preferred selection."""
        try:
            with self.data_lock.acquire(timeout=10):
                if os.path.exists(self.data_file):
                    with open(self.data_file, "r") as f:
                        self.data = json.load(f)

                comparison = {
                    "timestamp": datetime.now().isoformat(),
                    "set_index": set_index,
                    "ratings": ratings,
                    "winner": winner,
                    "username": username,
                }
                self.data["results"]["comparisons"].append(comparison)

                with open(self.data_file, "w") as f:
                    json.dump(self.data, f, indent=2)
        except Timeout:
            print(f"Could not acquire lock on {self.data_file}")

    def download_file(self, file_name: str):
        """Return file path for download if it exists."""
        file_path = os.path.join(self.data_dir, file_name)
        return file_path if os.path.exists(file_path) else None

# -------------------------------
# Create the Gradio Interface
# -------------------------------
def create_arena_interface(data_dir: str = None):
    manager = ImageArenaManager(data_dir=data_dir)

    with gr.Blocks(title="Driving Scenario generation") as demo:
        gr.Markdown("""
            ### 🚗 Driving Scenario Generation 
            
            Welcome! This survey aims to evaluate and compare different AI models that generate driving scenarios based on textual descriptions.These scenarios represent real-world traffic situations.

            #### 🔹 How It Works  
            - You will be presented with **a driving scenario description and three representations of it**. 
            - We model different traffic entities—such as **cars, pedestrians, and traffic cones**—using **rectangles in different colors**.  
            - Each entity’s **future trajectory** is displayed in the **same color** as the entity itself, starting from its position in the scene.  
            - **Two future trajectories crossing** each other represent a **potential collision**.
            - **A trajectory going through another entity** represents a **potential collision**.
            - Your task is to **rate each representation** on a scale from **1 to 5**, where:  
                - **1 = Poorly represents the description**  
                - **5 = Perfectly matches the description**   
            - Finally, **choose the scenario representaion that best fits the description** based on your understanding.  

            #### 🛣 Why This Matters  
            By participating in this survey, you are helping to improve **AI-driven scenario generation** for autonomous driving research. Your feedback will contribute to a better understanding of how well we can generate **driving scenarios based on descriptions**.  

            🚦 **Let’s get started!** \n
            By pushing Answer A, Answer B or Answer C, you will select the image that best represents the driving description. But before pushing any of them, grade each one of the answer with the grading cursor (beneath each image). \n
            Use the grading sliders (beneath each image) to rate each representation, then click **Answer A, Answer B, or Answer C** to select the best match.  \n
            Press **Skip to Next Question** if you already evaluated the images in a previous question. \n

            ---
        """)

        # ---------------------------
        # Scenario Description Section
        # ---------------------------
        gr.Markdown("""
            ### 📜 **Scenario Description**
            <div style='text-align: center; font-size: 20px; font-weight: bold; color: #007BFF;'>Below is the driving scenario description:</div>
        """, elem_id="scenario-description-header")


        description_box = gr.Markdown("")

        current_set = gr.State()
        current_labels = gr.State()
        username = gr.State(str(uuid.uuid4())[:8])

        with gr.Row():
            image_A = gr.Image(height=300)
            image_B = gr.Image(height=300)
            image_C = gr.Image(height=300)

        with gr.Row():
            rating_A = gr.Slider(1, 5, step=1, label="Rate Image A")
            rating_B = gr.Slider(1, 5, step=1, label="Rate Image B")
            rating_C = gr.Slider(1, 5, step=1, label="Rate Image C")

        with gr.Row():
            btn_A = gr.Button("Answer A")
            btn_B = gr.Button("Answer B")
            btn_C = gr.Button("Answer C")

        # ---------------------------
        # Load New Scenario
        # ---------------------------
        def load_new_comparison():
            """Load a new random image set and its description."""
            images, labels, set_index, description = manager.load_random_set()
            return images[0], images[1], images[2], labels, set_index, description

        def handle_choice(choice_index: int, set_index: int, rating_A: int, rating_B: int, rating_C: int, current_labels: List[str], current_username: str):
            """Handles user selection and ratings, then resets sliders."""
            ratings = {current_labels[0]: rating_A, current_labels[1]: rating_B, current_labels[2]: rating_C}
            winner = current_labels[choice_index]
            manager.save_comparison(set_index, ratings, winner, current_username)
    
            # Load new comparison and reset sliders
            images, labels, new_set_index, description = manager.load_random_set()
            return images[0], images[1], images[2], labels, new_set_index, description, 0, 0, 0


        # ---------------------------
        # Button Click Actions
        # ---------------------------
        btn_A.click(fn=lambda s, rA, rB, rC, l, u: handle_choice(0, s, rA, rB, rC, l, u), 
            inputs=[current_set, rating_A, rating_B, rating_C, current_labels, username], 
            outputs=[image_A, image_B, image_C, current_labels, current_set, description_box, rating_A, rating_B, rating_C])

        btn_B.click(fn=lambda s, rA, rB, rC, l, u: handle_choice(1, s, rA, rB, rC, l, u), 
                    inputs=[current_set, rating_A, rating_B, rating_C, current_labels, username], 
                    outputs=[image_A, image_B, image_C, current_labels, current_set, description_box, rating_A, rating_B, rating_C])

        btn_C.click(fn=lambda s, rA, rB, rC, l, u: handle_choice(2, s, rA, rB, rC, l, u), 
                    inputs=[current_set, rating_A, rating_B, rating_C, current_labels, username], 
                    outputs=[image_A, image_B, image_C, current_labels, current_set, description_box, rating_A, rating_B, rating_C])

        with gr.Row():
            skip_btn = gr.Button("Skip to Next Question")

        # Skip Button Action
        skip_btn.click(fn=load_new_comparison, 
                       inputs=[], 
                       outputs=[image_A, image_B, image_C, current_labels, current_set, description_box])


        demo.load(fn=load_new_comparison, inputs=[], outputs=[image_A, image_B, image_C, current_labels, current_set, description_box])

        # ---------------------------
        # Download Section
        # ---------------------------
        gr.Markdown("### 📥 Download Results")
        file_select = gr.Dropdown(choices=["arena_data.json", "arena_data.lock"], label="Select File")
        download_button = gr.Button("Download")
        download_output = gr.File(label="Download File")

        download_button.click(fn=manager.download_file, inputs=[file_select], outputs=[download_output])

    return demo

# -------------------------------
# Main: Run the Interface
# -------------------------------
if __name__ == "__main__":
    data_dir = "./data"
    demo = create_arena_interface(data_dir=data_dir)
    demo.launch()
