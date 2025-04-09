# @title 🧼 Data Cleaning for MMD Files
# @markdown Remove Acknowledgement and References.

# @markdown If you want to further remove Abstract and Introduction, please uncomment the relevant code.

input_folder = "papers/nougat"  # @param {type:"string"}
output_folder = "papers/cleaned"  # @param {type:"string"}

# --- Script starts here ---
from tqdm import tqdm
import os
import re

def remove_abstract_introduction(text):
    # Define patterns to match Abstract, Introduction, and Experiment sections
    abstract_pattern = re.compile(r"(?i)^#+\s*([ivxlcdm\d]*\s*)?a\s*bstract\s*(.*?)", re.DOTALL | re.MULTILINE)
    introduction_pattern = re.compile(r"(?i)^#+\s*([ivxlcdm\d]*\s*)?introduction\s*(.*?)", re.DOTALL | re.MULTILINE)
    experiment_pattern = re.compile(
        r"(?i)^#+\s*([ivxlcdm\d]*\s*)?(experiment(?:al|s)?|materials and methods|methodology)\s*(.*?)(?=#+|$)", re.DOTALL | re.MULTILINE
    )

    # Search for matches
    abstract_matches = list(abstract_pattern.finditer(text))
    introduction_match = re.search(introduction_pattern, text)
    experiment_match = re.search(experiment_pattern, text)

    # Check if multiple abstracts exist
    if len(abstract_matches) > 1:
        # If multiple abstracts exist, keep the last one
        abstract_match = abstract_matches[-1]
    elif len(abstract_matches) == 1:
        abstract_match = abstract_matches[0]
    else:
        abstract_match = None

    # Check if abstract exists
    if abstract_match:
        if introduction_match:
            if experiment_match:
                # If abstract, introduction and experiment exist, remove content before experiment
                text = text[experiment_match.start() :]
            else:
                # If abstract and introduction exist but experiment does not exist, remove content before introduction
                text = text[introduction_match.start() :]
        else:
            # If abstract exists but introduction and experiment do not exist, only remove content before
            # abstract to avoid removing the useful content
            text = text[abstract_match.start() :]
    else:
        if introduction_match:
            if experiment_match:
                # If abstract does not exist but introduction and experiment exist, remove content before experiment
                text = text[experiment_match.start() :]
            else:
                # If abstract and experiment do not exist but introduction exists, only remove content before
                # introduction
                text = text[introduction_match.start() :]
        else:
            # If abstract, introduction and experiment do not exist, keep the content
            text = text

    return text.strip()


def remove_references_acknowledgement(text):
    # Remove 'References' section (any heading level, with optional numbering)
    text = re.sub(
        r"^#{1,6}\s*\d*\s*References\b.*?(?=^#{1,6}\s|\Z)",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE | re.MULTILINE
    )

    sections_to_remove = [
        "Acknowledgements",
        "Acknowledgments",
        "Conflicts of interest",
        "Declaration of competing interest",
        "Disclosure statement",
        "Funding",
        "Conflicts of Interest",
        "Supporting Information",
        "Author Contributions",
    ]

    # Match any heading level (# to ######), optional numbering, section name, and its content
    pattern = (
            r"^#{1,6}\s*\d*\s*(?:" +
            "|".join(re.escape(s) for s in sections_to_remove) +
            r")\b.*?(?=^#{1,6}\s|\Z)"
    )

    text = re.sub(pattern, "", text, flags=re.DOTALL | re.MULTILINE | re.IGNORECASE)
    return text


def remove_repetitions(text, threshold=3):
    pattern = re.compile(r'\b(.+?)\b(?:\s+\1\b){{{},}}'.format(threshold - 1))
    cleaned = pattern.sub(r'\1', text)
    return cleaned


def process_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in tqdm(os.listdir(input_folder)):
        if file_name.endswith(".mmd"):  # Assuming the articles are in text files
            with open(os.path.join(input_folder, file_name), "r", encoding="utf-8") as file:
                text = file.read()

            cleaned_text = remove_repetitions(text)
            cleaned_text = remove_references_acknowledgement(cleaned_text)
            cleaned_text = remove_abstract_introduction(cleaned_text)

            output_file_name = f"{file_name}"
            with open(os.path.join(output_folder, output_file_name), "w", encoding="utf-8") as output_file:
                output_file.write(cleaned_text)

process_files(input_folder, output_folder)