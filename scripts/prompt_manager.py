import os
import re
import yaml
from datetime import datetime

# --- Configuration ---
PROMPT_DIRS = ["analysis", "trading"]  # Directories to scan for prompts
METADATA_DIR = "metadata"
PROMPT_INDEX_FILE = os.path.join(METADATA_DIR, "prompt_index.yaml")
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

REQUIRED_FIELDS = [
    "id",
    "title",
    "description",
    "category",
    "tags",
    "version",
    "status",
    "llm_model_compatibility",
]


# --- Helper Functions ---
def extract_front_matter(md_content):
    """
    Extracts YAML front matter from Markdown content.
    Returns (front_matter_dict, content_without_front_matter).
    """
    match = re.match(r"^\s*---\s*\n(.*?)\n\s*---\s*\n(.*)", md_content, re.DOTALL)
    if not match:
        return None, md_content

    front_matter_str = match.group(1)
    content_without_front_matter = match.group(2)
    try:
        front_matter_dict = yaml.safe_load(front_matter_str)
        return front_matter_dict, content_without_front_matter
    except yaml.YAMLError as e:
        print(f"Error parsing YAML front matter: {e}")
        return None, md_content


def validate_front_matter(metadata, file_path):
    """
    Validates the extracted front matter for required fields.
    Returns True if valid, False otherwise.
    """
    is_valid = True
    for field in REQUIRED_FIELDS:
        if field not in metadata:
            print(f"Warning: '{field}' missing in {file_path}")
            is_valid = False

    if not isinstance(metadata.get("tags"), list):
        print(f"Warning: 'tags' field in {file_path} should be a list.")
        is_valid = False
    if not isinstance(metadata.get("llm_model_compatibility"), list):
        print(
            f"Warning: 'llm_model_compatibility' field in {file_path} should be a list."
        )
        is_valid = False
    if "parameters" in metadata and not isinstance(metadata["parameters"], list):
        print(
            f"Warning: 'parameters' field in {file_path} should be a list of dictionaries."
        )
        is_valid = False
    if "plan_steps" in metadata and not isinstance(metadata["plan_steps"], list):
        print(
            f"Warning: 'plan_steps' field in {file_path} should be a list of dictionaries."
        )
        is_valid = False

    return is_valid


def generate_prompt_index():
    """
    Scans specified directories for prompt files, extracts and validates their
    front matter, and generates the prompt_index.yaml file.
    """
    all_prompts_metadata = []

    # Ensure metadata directory exists
    os.makedirs(os.path.join(PROJECT_ROOT, METADATA_DIR), exist_ok=True)

    for prompt_dir in PROMPT_DIRS:
        full_prompt_dir_path = os.path.join(PROJECT_ROOT, prompt_dir)
        if not os.path.isdir(full_prompt_dir_path):
            print(f"Warning: Prompt directory '{prompt_dir}' not found. Skipping.")
            continue

        for root, _, files in os.walk(full_prompt_dir_path):
            for file_name in files:
                if file_name.endswith(".md"):
                    if file_name == "README.md" or file_name == "changelog.md":
                        print(f"Skipping documentation file: {file_name}")
                        continue

                    file_path_abs = os.path.join(root, file_name)
                    file_path_rel = os.path.relpath(file_path_abs, PROJECT_ROOT)

                    with open(file_path_abs, "r", encoding="utf-8") as f:
                        content = f.read()

                    metadata, _ = extract_front_matter(content)

                    if metadata:
                        # Add / update last_modified timestamp
                        metadata["last_modified"] = datetime.now().isoformat()
                        # Add relative file path
                        metadata["file_path"] = file_path_rel
                        if validate_front_matter(metadata, file_path_rel):
                            all_prompts_metadata.append(metadata)
                        else:
                            print(f"Skipping invalid prompt: {file_path_rel}")
                    else:
                        print(
                            f"Warning: No YAML front matter found in {file_path_rel}. Skipping."
                        )

    # Write the aggregated metadata to prompt_index.yaml
    index_file_path = os.path.join(PROJECT_ROOT, PROMPT_INDEX_FILE)
    try:
        with open(index_file_path, "w", encoding="utf-8") as f:
            yaml.dump(
                all_prompts_metadata,
                f,
                sort_keys=False,
                indent=2,
                default_flow_style=False,
            )
        print(
            f"Successfully generated {index_file_path} with {len(all_prompts_metadata)} prompts."
        )
    except Exception as e:
        print(f"Error writing prompt index file: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    print("Generating prompt index...")
    generate_prompt_index()
