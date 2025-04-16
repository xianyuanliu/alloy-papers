#  🧪 Extracting Alloy Data from Scientific PDFs – TOTEMIC Training School - 2025

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/xianyuanliu/alloy-property-extraction-demo/blob/main/NLP_for_Materials.ipynb)

Welcome to the GitHub repository for the session at the **TOTEMIC Training School 2025: "Tools for Energy Materials Modelling Acceleration"** on Extracting Alloy Data from PDF Files. This repository contains all the code, tools, and examples you’ll need to automatically extract alloy composition and phase information from scientific papers using **Nougat** and **LLMs (LLaMA via Hugging Face Transformers)**. All steps are designed to be run on **Google Colab**, making use of its free GPU resources.



## Authors 

- Xianyuan Liu <sup>1,2</sup>
- Alan Thomas <sup>1,2</sup>
- Joshua Berry <sup>3</sup>
- Katerina Christofidou <sup>3</sup>

1. _School of Computer Science, University of Sheffield, UK_
2. _AI Research Engineering, Centre for Machine Intelligence, University of Sheffield, UK_
3. _Material Science and Engineering Department, University of Sheffield, UK_



## Aim

The goal of this training session is to **demonstrate and walk through** an end-to-end workflow for:
- Converting academic papers in PDF format into markdown text
- Cleaning and preparing that text
- Extracting alloy and phase information using a large language model (LLM)
- Reviewing and saving the extracted data

The training is designed for **both coders and non-coders**, with **interactive input boxes** provided to guide users through each step without needing to write code.



## Setup & Usage Guide

All steps are run on **Google Colab**. You do not need to install anything locally. <br />
Make sure to access the GPU. <br />
**Runtime > Change runTime type > T4 GPU** 

You will also need to [Sign up for Hugging Face](https://huggingface.co/join) for free to use Hugging Face via the Transformers Library.

You will need to agree to the license terms and conditions to use the LLaMA models. You can find the terms for the [**LLaMA-3.2-3B** model](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) here.

---

### 1. Download Papers
- Dummy PDF papers or open-access academic PDF papers are preloaded from Google Drive or this repository.

---

### 2. Convert PDF to Raw Text
- **Install Nougat** from GitHub (an open-source OCR-based tool for PDF parsing).
- Run Nougat to convert PDFs to `.mmd` markdown files.
- **Preview extracted text** using `IPython.display` and compare it with the original PDF.
- _Optional_: Open the `.mmd` markdown file to find which format the PDF is converted to.

---

### 3. Clean Raw Text
- **Remove unwanted sections** (e.g., acknowledgements, references).
- _Optional_: Remove abstract and introduction.
- Re-preview the `.mmd` file as above to confirm it's clean.

---

### 4. Login to Hugging Face
- You'll be prompted to **enter your Hugging Face access token**.
- This is required to use the LLaMA model via the Transformers library.

---

### 5. Upgrade to Transformers v4.49.0
- This specific version of Hugging Face Transformers is needed for compatibility with LLaMA models.
- Runtime will **restart automatically** after installation.

---

### 6. Extract Alloy and Phase Information
- Use a **LLaMA-based LLM** to extract structured data from `.mmd` files.
- The model:
  - Identifies alloy compositions
  - Extracts phase-related information
  - Cleans the output and saves it in JSON format in a `.json` file in an output folder

---

### 7. Preview Extracted Data
- Load and display the structured JSON data of extracted alloy and phase information.
- Easy to review in table or dictionary format.

---

### 8. Utilities _(Optional)_
If you run into memory or performance issues:
- **Free GPU Memory**: Clears unused variables and CUDA memory caches.
- **Clear Cache**: Choose to clean Hugging Face and/or PyTorch caches. Otherwise, they will be stored in your account storage.

---

## 📚 Citations

The following tools are used in the construction of this work:

- **Nougat**: 
  > @misc{blecher2023nougat,
  > title={Nougat: Neural Optical Understanding for Academic Documents},
  > author={Lukas Blecher and Guillem Cucurull and Thomas Scialom and Robert Stojnic},
  > year={2023},
  > eprint={2308.13418},
  > archivePrefix={arXiv},
  > primaryClass={cs.LG}
}

- **LLaMA**:
  > @misc{touvron2023llama,  
  > title={LLaMA: Open and Efficient Foundation Language Models},  
  > author={Hugo Touvron and Thibaut Lavril and Gautier Izacard et al.},  
  > year={2023},  
  > eprint={2302.13971},  
  > archivePrefix={arXiv},  
  > primaryClass={cs.CL}  
  > }


