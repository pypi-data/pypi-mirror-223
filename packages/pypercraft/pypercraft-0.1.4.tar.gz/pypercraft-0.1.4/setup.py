from setuptools import setup, find_packages

setup(
    name='pypercraft',
    version='0.1.4',
    description='Utilize Large Language Models to Craft Papers and Export them to Documents',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='alkhalifas',
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "langchain",
        "openai",
        "uvicorn",
        "pylint",
        "httpx",
        "streamlit",
        "python-docx"
    ],
)
