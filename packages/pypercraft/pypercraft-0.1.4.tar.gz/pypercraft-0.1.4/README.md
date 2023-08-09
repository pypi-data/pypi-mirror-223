# Pypercraft
### A Novel Application that Harnesses LLMs to Generate Articles and Papers

## Abstract
Introducing a novel Python application that harnesses the expanded capabilities of ChatGPT, 
enabling users to effortlessly compose comprehensive articles and papers on topics of their
choice. Surpassing token constraints, this application empowers users to craft full 
compositions comprising a Title, Introduction, Body, and Conclusion. Accessible through
a user-friendly Streamlit interface or a FastAPI-powered API, the tool seamlessly merges
user input with ChatGPT's contextual understanding, resulting in coherent written pieces.
Offering an additional advantage, users can export their creations as Word documents 
(.docx), enhancing the versatility and utility of the generated content. Whether 
fashioning educational articles or structured research papers, this application 
revolutionizes content creation, amalgamating user ingenuity with ChatGPT's 
linguistic finesse and streamlining written communication with convenience 
and sophistication.

## Live Demo

A live demo of the Streamlit application can be seen [here](https://pypercraft-8c8dd60022df.herokuapp.com/)

## Quick Start Guide

### Clone The Repo:

    git clone git@github.com:alkhalifas/pypercraft.git

    pip install -r requirements.txt

    streamlit run ui.py

### Install With Pip:

Install Library:

    pip install pypercraft

Import and Apply:

    from pypercraft import pypercraft

    craft = pypercraft.Pypercraft(

            # Describe the paper you want to generate
            query= "A Scientific Paper about Deep Learning",

            # Select the topic of your paper
            topic= "Data Science",

            # Select number of pages
            num_pages= 3,

            # Select tone of the writer
            tone= "professional",

            # Enter API key
            api_key= os.getenv("OPENAI_API_KEY"))

    # Construct the paper
    paper = craft.construct()

    # Export final paper
    craft.export_docx('mypaper.docx')
