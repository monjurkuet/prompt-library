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


def validate_front_matter(metadata, file_path_rel):
    """
    Validates the extracted front matter for required fields and consistency.
    Returns True if valid, False otherwise.
    """
    is_valid = True
    for field in REQUIRED_FIELDS:
        if field not in metadata:
            print(f"Warning: '{field}' missing in {file_path_rel}")
            is_valid = False

    if not isinstance(metadata.get("tags"), list):
        print(f"Warning: 'tags' field in {file_path_rel} should be a list.")
        is_valid = False
    if not isinstance(metadata.get("llm_model_compatibility"), list):
        print(
            f"Warning: 'llm_model_compatibility' field in {file_path_rel} should be a list."
        )
        is_valid = False
    if "parameters" in metadata and not isinstance(metadata["parameters"], list):
        print(
            f"Warning: 'parameters' field in {file_path_rel} should be a list of dictionaries."
        )
        is_valid = False
    if "plan_steps" in metadata and not isinstance(metadata["plan_steps"], list):
        print(
            f"Warning: 'plan_steps' field in {file_path_rel} should be a list of dictionaries."
        )
        is_valid = False

    # New check for path-category consistency
    if not check_path_category_consistency(metadata, file_path_rel):
        is_valid = False

    return is_valid


def check_path_category_consistency(metadata, file_path_rel):
    """
    Checks if metadata 'category' and 'sub_category' align with the file path.
    Returns True if consistent, False otherwise.
    """
    is_consistent = True
    path_parts = file_path_rel.split(os.sep)

    # file_path_rel is like 'category/sub_category/file.md'
    # so path_parts[0] should be category, path_parts[1] should be sub_category

    # Check primary category
    if len(path_parts) > 0 and path_parts[0] != metadata.get("category"):
        print(
            f"Error: Category '{metadata.get('category')}' in metadata does not match "
            f"first path part '{path_parts[0]}' for {file_path_rel}"
        )
        is_consistent = False

    # Check sub_category if present in metadata and path
    if "sub_category" in metadata:
        if len(path_parts) > 1 and path_parts[1] != metadata["sub_category"]:
            print(
                f"Error: Sub-category '{metadata['sub_category']}' in metadata does not match "
                f"second path part '{path_parts[1]}' for {file_path_rel}"
            )
            is_consistent = False
        # If sub_category is in metadata but no sub_dir in path (e.g., 'category/file.md')
        elif len(path_parts) <= 1 or (
            len(path_parts) > 1 and path_parts[1].endswith(".md")
        ):
            print(
                f"Error: Sub-category '{metadata['sub_category']}' in metadata found, "
                f"but no corresponding sub-directory in path for {file_path_rel}"
            )
            is_consistent = False
    # If sub_directory is in path but no sub_category in metadata (and it's not a root file like README)
    elif len(path_parts) > 1 and not path_parts[1].endswith(".md"):
        print(
            f"Error: Sub-directory '{path_parts[1]}' found in path, but no 'sub_category' "
            f"in metadata for {file_path_rel}. Consider adding 'sub_category'."
        )
        is_consistent = False  # This is now a hard failure for consistency

    return is_consistent


def check_unique_ids(all_prompts_metadata):
    """
    Checks for unique 'id' values across all collected prompt metadata.
    Returns True if all IDs are unique, False otherwise.
    """
    ids = {}
    is_unique = True
    for meta in all_prompts_metadata:
        prompt_id = meta.get("id")
        file_path = meta.get("file_path", "unknown_file")
        if prompt_id:
            if prompt_id in ids:
                print(
                    f"Error: Duplicate ID '{prompt_id}' found. "
                    f"First instance in {ids[prompt_id]}, duplicate in {file_path}"
                )
                is_unique = False
            else:
                ids[prompt_id] = file_path
        else:
            # This case is already covered by REQUIRED_FIELDS check, but good to note.
            print(
                f"Error: Prompt in {file_path} is missing an 'id'. Cannot check for uniqueness."
            )
            is_unique = False  # If ID is missing, it's not uniquely identifiable

    return is_unique


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
                            # If validate_front_matter returns False, it means there was a critical error for that prompt
                            # We still append to all_prompts_metadata so check_unique_ids can report on it,
                            # but we will fail the overall_validity.
                            pass  # Individual errors are printed in validate_front_matter

    overall_valid = True  # Initialize overall validity flag

    # After collecting all metadata, perform cross-cutting validations
    if not check_unique_ids(all_prompts_metadata):
        overall_valid = False

    # if other cross-cutting validations were added, they would go here
    # e.g., if not check_semantic_versioning(all_prompts_metadata): overall_valid = False

    if not overall_valid:
        print(
            "Error: Prompt index generation halted due to critical validation errors."
        )
        return  # Do not write the index if critical errors exist

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
