from setuptools import setup, find_packages

setup(
    name='pypercraft',
    version='0.1.0',
    description='Utilize Large Language Models to Craft Papers and Export them to Documents',
    author='alkhalifas',
    packages=find_packages(),
    install_requires=[
        "fastapi == 0.100.1",
        "langchain == 0.0.249",
        "openai == 0.27.8",
        "uvicorn == 0.23.2",
        "pylint == 2.17.5",
        "httpx == 0.24.1",
        "streamlit == 1.25.0",
        "python-docx == 0.8.11"
    ],
)
