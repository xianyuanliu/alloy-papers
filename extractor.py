# @title 🔍 Extract Alloy & Phase Info from MMD Files
# @markdown This cell runs an LLM-based extraction pipeline on MMD files generated from academic PDFs.
# @markdown It identifies alloy compositions, and phase information based on structured prompts,
# @markdown then cleans and saves the output as JSON in the specified output folder.

llm_model = "meta-llama/Llama-3.2-3B-Instruct" # @param {type:"string"}
input_folder = "papers/cleaned" # @param {type:"string"}
output_dir = "papers/output" # @param {type:"string"}
max_len = "120000" # @param {type:"string"}
quantize = "" # @param {type:"string"}

# --- Script starts here ---
import json
import os
import re

import torch
from tqdm import tqdm
from transformers import pipeline


def split(tokenizer, text, max_len):
    chunks, c = [], []
    for line in text.split("\n"):
        c.append(line)
        if len(tokenizer.tokenize("\n".join(c))) > max_len:
            chunks.append("\n".join(c[:-1]))
            c = [line]
    chunks.append("\n".join(c))
    return chunks


def chat(generator, dialog):
    terminators = [
        generator.tokenizer.eos_token_id,
        generator.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
    ]

    outputs = generator(
        dialog,
        max_new_tokens=1024,
        eos_token_id=terminators,
        pad_token_id=generator.tokenizer.eos_token_id,
        do_sample=True,
        temperature=0.1,
    )

    return outputs[0]["generated_text"][-1]["content"]


def clean(text):
    pattern = re.compile(r"\{.*?\}", re.DOTALL)
    match = pattern.findall(text)
    cleaned = "[" + ",".join(match) + "]" if match else "[]"
    try:
        json.loads(cleaned)
        return cleaned
    except json.JSONDecodeError:
        return "[]"

def prompt_1(text):
    return f"""You are a helpful assistant. Your task is to extract alloy and its corresponding phase information from the text.

    Please follow these instructions carefully:

    **Extract alloy and phase information** from the paper text, delimited by —————.
        Please use the following JSON schema to generate the output:
    {{
       "Alloy": "XXX",
       "Phase": "XXX"       
    }}
    
    "Alloy": Elemental composition of the alloy mentioned in the paper (e.g., AlFeNiTiVZr). Alloy compositions should contain multiple chemical elements. Ignore invalid entries. Ignore alloys that include unknown placeholders (e.g., "X", "Y", or invalid symbols).
    "Phase": Phase information of the alloy in this paper with possible values: 'BCC', 'FCC', 'Im', 'FCC + BCC', 'BCC + Im', 'FCC + Im', 'FCC + BCC + Im'
       
    Return a list of JSON objects if there are several alloys. Only return valid JSON objects, with no additional text.
—————
{text}
—————
"""


# def prompt_1(text):
#     return f"""You are a helpful assistant. Your task is to extract data from materials science papers.
#
# Extract alloy and phase information from the paper text, delimited by —————.
#
# Please use the following JSON schema to generate the output:
# {{
#    "Alloy": "",
#    "Phase": ""
# }}
#
# "Alloy": Elemental composition of the alloy mentioned in the paper (e.g., AlFeNiTiVZr).
# "Phase": Phase information of the alloy with possible values: 'BCC', 'FCC', 'Im', 'FCC + BCC', 'BCC + Im', 'FCC + Im', 'FCC + BCC + Im'
#
# Return a list of JSON objects if there are several alloys. Only return valid JSON objects, with no additional text.
#
# —————
# {text}
# —————
# """
#
# def prompt_2(text):
#     return f"""Ensure that the alloy compositions contain multiple elements. If it does not, remove it from the list.
#
# Return the updated list of JSON objects with only valid entries.
#
# Here is the list:
# —————
# {text}
# —————
# """
#
# def prompt_3(text):
#     return f"""Ensure that the phase information is valid. It may need to be changed or simplified.
#
# Possible values are:
# 'BCC', 'FCC', 'Im', 'FCC + BCC', 'BCC + Im', 'FCC + Im', 'FCC + BCC + Im'.
# Note that 'BCC' is body-centred cubic, 'FCC' is face-centred cubic, and 'Im' is intermetallic.
# If other values are mentioned, please simplify to one of the possible values.
#
# For example:
# - 'FCC + B2' --> 'FCC+Im'
# - 'B2' --> 'Im'
# - 'BCC + HCP' --> 'BCC'
# - 'BCC + HCP - 1' --> 'BCC'
# - 'B2 + BCC + FCC + SIGMA' --> 'BCC+FCC+Im'
# - 'FCC + LAVES' --> 'FCC+Im'
# - 'AMORPHOUS + FCC + IM' --> 'FCC+Im'
# - 'FCC + L12' --> 'FCC+Im'
# - 'BCC + FCC + FCC' --> 'BCC+FCC'
# - 'HCP + Im' --> 'Im'
#
# Return the updated list of JSON objects with only valid entries.
#
# Here is the list:
# —————
# {text}
# —————
# """

def main(model, folder, output_dir, max_len, quantize):
    generator = pipeline(
        "text-generation",
        model=model,
        model_kwargs={
            "torch_dtype": torch.bfloat16,
            "load_in_4bit": quantize == "4bit",
            "load_in_8bit": quantize == "8bit",
            # "llm_int8_enable_fp32_cpu_offload": quantize == "8bit",
        },
        device_map="auto",
    )

    results = "{}/{}-{}-{}".format(output_dir, model.split("/")[-1], quantize, max_len)
    print(f"Results will be saved in {results}")
    if not os.path.exists(results):
        os.makedirs(results)

    # Step 1: Get all .mmd files in the folder
    paper_list = [f[:-4] for f in os.listdir(folder) if f.endswith(".mmd")]

    # Step 2: Loop through them
    for mmd in tqdm(sorted(paper_list)):
        print("Processing:", mmd)
        mmd_path = os.path.join(folder, mmd + ".mmd")

        if not os.path.exists(mmd_path):
            print("File not found:", mmd_path)
            continue

        with open(mmd_path, "r") as f:
            ocr = f.read()
            paper = split(generator.tokenizer, ocr, max_len)

        outputs = []
        for part in paper:
            dialog = [{"role": "user", "content": prompt_1(part)}]
            response = clean(chat(generator, dialog))
            # dialog.append({"role": "assistant", "content": response})

            # dialog.append({"role": "user", "content": prompt_2(response)})
            # response = clean(chat(generator, dialog))
            # dialog.append({"role": "assistant", "content": response})
            #
            # dialog.append({"role": "user", "content": prompt_3(response)})
            # response = clean(chat(generator, dialog))

            outputs.append(response)
            del dialog, response
            torch.cuda.empty_cache()

        merged = []
        for o in outputs:
            merged.extend(json.loads(o))
        # unique = [dict(t) for t in {tuple(sorted(d.items())) for d in merged}]
        unique = [
            dict(t) for t in {
                tuple(sorted((k, tuple(v) if isinstance(v, list) else v) for k, v in d.items()))
                for d in merged
            }
        ]
        with open(os.path.join(results, mmd), "w") as f:
            f.write(json.dumps(unique, indent=2))

max_len = int(max_len)
print("Files to process:", os.listdir(input_folder))
main(llm_model, input_folder, output_dir, max_len, quantize)
