from setuptools import setup, find_packages
import platform

with open('requirements.txt') as f:
    install_requirement = f.readlines()

setup(
    name="chatGPT",
    description="A simple Python class for interacting with OpenAI's chatGPT using Playwright",
    packages=find_packages(),
    install_requires=install_requirement,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "chatgpt = chatgpt_wrapper.chatgpt:main"
        ]
    },
    scripts=["postinstall.bat"] if platform.system() == "Windows" else ["postinstall.sh"],
)
