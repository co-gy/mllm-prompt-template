import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mllm-prompt-template",
    version="2.0.0",
    author="co-gy",
    author_email="948628463@qq.com",
    description="A Python template library for multimodal large language models (MLLM) that supports image substitution in prompts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/co-gy/mllm-prompt-template",
    packages=setuptools.find_packages(),
    install_requires=[
        "Pillow>=9.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.8",
)