import os
import re
import yaml
from datetime import datetime
import argparse  # Added argparse

# --- Configuration ---
PROMPT_DIRS = [
    "analysis",
    "trading",
    "utilities",
    "development",
    "content",
]  # Directories to scan for prompts
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
                    else:
                        print(
                            f"Warning: No YAML front matter found in {file_path_rel}. Skipping."
                        )

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

        # Update READMEs after successful indexing
        update_category_readmes(all_prompts_metadata)

    except Exception as e:
        print(f"Error writing prompt index file: {e}")


def update_category_readmes(all_prompts_metadata):
    """
    Updates README.md files in each category directory with a list of prompts.
    """
    print("Updating category READMEs...")

    # Group prompts by directory
    prompts_by_dir = {}
    for prompt in all_prompts_metadata:
        file_path_rel = prompt.get("file_path")
        if not file_path_rel:
            continue

        dir_path = os.path.dirname(os.path.join(PROJECT_ROOT, file_path_rel))
        if dir_path not in prompts_by_dir:
            prompts_by_dir[dir_path] = []
        prompts_by_dir[dir_path].append(prompt)

    # Markers
    START_MARKER = "<!-- AUTOMATED_PROMPTS_LIST_START -->"
    END_MARKER = "<!-- AUTOMATED_PROMPTS_LIST_END -->"

    for dir_path, prompts in prompts_by_dir.items():
        readme_path = os.path.join(dir_path, "README.md")

        # Skip if README doesn't exist (we don't create new READMEs, only update existing)
        if not os.path.exists(readme_path):
            continue

        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Generate list content
        list_content = "\n"
        for p in sorted(prompts, key=lambda x: x.get("title", "Untitled")):
            rel_link = os.path.basename(p["file_path"])
            desc = p.get("description", "No description.")
            list_content += f"### [{p.get('title', 'Untitled')}]({rel_link})\n"
            list_content += f"{desc}\n\n"
            # Add metadata badges/bullets
            meta_items = []
            if "version" in p:
                meta_items.append(f"**Version:** {p['version']}")
            if "tags" in p:
                meta_items.append(f"**Tags:** {', '.join(p['tags'])}")
            if meta_items:
                list_content += f"- {' | '.join(meta_items)}\n\n"
            list_content += "---\n\n"

        # Check for markers
        if START_MARKER in content and END_MARKER in content:
            # Replace existing block
            pattern = re.compile(
                f"{re.escape(START_MARKER)}.*?{re.escape(END_MARKER)}", re.DOTALL
            )
            new_block = f"{START_MARKER}\n{list_content}{END_MARKER}"
            new_content = pattern.sub(new_block, content)
        else:
            # Append markers
            # Try to find a logical place
            if "## Prompts" in content:
                # Insert after ## Prompts header if strictly no markers found yet
                # This is a bit complex regex, simpler to just append or replace
                pass

            # Simple strategy: If no markers, append to end or find ## Prompts
            # Let's append to the end for now if not found, with a header
            header = (
                "\n## Available Prompts\n"
                if "## Prompts" not in content and "## Available Prompts" not in content
                else "\n"
            )
            new_block = f"{header}{START_MARKER}\n{list_content}{END_MARKER}\n"
            new_content = content + new_block

        if new_content != content:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {os.path.relpath(readme_path, PROJECT_ROOT)}")
        else:
            print(f"No changes needed for {os.path.relpath(readme_path, PROJECT_ROOT)}")


def create_new_prompt(args):
    """
    Guides the user through creating a new prompt file with YAML front matter.
    """
    print("\n--- Creating New Prompt ---")

    # 1. Gather metadata interactively
    # Required fields first
    prompt_metadata = {}
    prompt_metadata["id"] = input(
        "Enter unique ID for the prompt (e.g., 'my-new-prompt'): "
    ).strip()
    while not prompt_metadata["id"]:
        prompt_metadata["id"] = input("ID cannot be empty. Enter unique ID: ").strip()

    prompt_metadata["title"] = input("Enter title for the prompt: ").strip()
    while not prompt_metadata["title"]:
        prompt_metadata["title"] = input("Title cannot be empty. Enter title: ").strip()

    prompt_metadata["description"] = input("Enter a brief description: ").strip()
    while not prompt_metadata["description"]:
        prompt_metadata["description"] = input(
            "Description cannot be empty. Enter description: "
        ).strip()

    # Category and sub_category - suggest from PROMPT_DIRS or existing structure
    print(f"\nAvailable primary categories: {', '.join(PROMPT_DIRS)}")
    prompt_metadata["category"] = input(
        "Enter primary category (e.g., 'analysis', 'trading'): "
    ).strip()
    while not prompt_metadata["category"]:
        prompt_metadata["category"] = input(
            "Category cannot be empty. Enter primary category: "
        ).strip()

    prompt_metadata["sub_category"] = input(
        "Enter sub-category (optional, e.g., 'data_processing', 'bot_development'). Leave blank if none: "
    ).strip()

    # Other required fields with sensible defaults or interactive input
    prompt_metadata["tags"] = [
        tag.strip()
        for tag in input("Enter tags (comma-separated, e.g., 'RAG, NLP'): ").split(",")
        if tag.strip()
    ]
    prompt_metadata["version"] = (
        input("Enter version (e.g., '1.0.0', default '1.0.0'): ") or "1.0.0"
    )
    prompt_metadata["status"] = (
        input(
            "Enter status (e.g., 'active', 'draft', 'deprecated', default 'active'): "
        )
        or "active"
    )
    prompt_metadata["llm_model_compatibility"] = [
        model.strip()
        for model in input(
            "Enter compatible LLM models (comma-separated, e.g., 'gpt-4o, claude-3-opus', default 'any'): "
        ).split(",")
        if model.strip()
    ] or ["any"]

    # Optional fields like parameters, plan_task, plan_steps
    if input("Does this prompt require parameters? (y/N): ").lower() == "y":
        prompt_metadata["parameters"] = []
        while True:
            param_name = input(
                "  Enter parameter name (leave blank to finish): "
            ).strip()
            if not param_name:
                break
            param_type = (
                input(
                    f"    Enter type for '{param_name}' (e.g., 'string', 'integer', default 'string'): "
                )
                or "string"
            )
            param_desc = input(f"    Enter description for '{param_name}': ").strip()
            prompt_metadata["parameters"].append(
                {"name": param_name, "type": param_type, "description": param_desc}
            )

    if input("Is this a multi-step plan prompt? (y/N): ").lower() == "y":
        prompt_metadata["plan_task"] = input("  Enter overall plan task: ").strip()
        prompt_metadata["plan_steps"] = []
        while True:
            step_title = input(
                "  Enter plan step title (leave blank to finish): "
            ).strip()
            if not step_title:
                break
            step_details = input(f"    Enter details for '{step_title}': ").strip()
            step_agent = input(
                f"    Enter agent name for '{step_title}' (optional): "
            ).strip()
            step_data = {"title": step_title, "details": step_details}
            if step_agent:
                step_data["agent_name"] = step_agent
            prompt_metadata["plan_steps"].append(step_data)

    # 2. Construct file path
    file_name = f"{prompt_metadata['id']}.md"
    target_dir = os.path.join(
        PROJECT_ROOT,
        prompt_metadata["category"],
        prompt_metadata["sub_category"] if prompt_metadata["sub_category"] else "",
    )
    # Clean up empty strings or None from path components
    target_dir_parts = [p for p in target_dir.split(os.sep) if p]
    target_dir = os.path.join(*target_dir_parts)

    target_file_path = os.path.join(target_dir, file_name)

    # Check for existing file
    if os.path.exists(target_file_path):
        print(f"Error: A prompt file already exists at {target_file_path}. Aborting.")
        return

    # 3. Generate content
    # Simple initial Markdown content
    markdown_content = f"# {prompt_metadata['title']}\n\n"
    markdown_content += f"## Purpose\n{prompt_metadata['description']}\n\n"
    markdown_content += "## Prompt\n\n[Your prompt content goes here]\n"

    full_content = f"---\n{yaml.dump(prompt_metadata, sort_keys=False, indent=2, default_flow_style=False)}---\n{markdown_content}"

    # 4. Write to file
    try:
        os.makedirs(target_dir, exist_ok=True)
        with open(target_file_path, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"\nSuccessfully created new prompt at: {target_file_path}")
        print(
            "Remember to add your main prompt content and then run 'uv run python scripts/prompt_manager.py index' to update the master index."
        )
    except Exception as e:
        print(f"Error creating prompt file: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage your prompt library.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Index command
    index_parser = subparsers.add_parser(
        "index", help="Generate/update the prompt index."
    )

    # New prompt command
    new_prompt_parser = subparsers.add_parser(
        "new-prompt", help="Create a new prompt file."
    )
    # Add arguments for new-prompt if we want non-interactive mode later

    args = parser.parse_args()

    if args.command == "index":
        print("Generating prompt index...")
        generate_prompt_index()
    elif args.command == "new-prompt":
        create_new_prompt(args)
    else:
        parser.print_help()
