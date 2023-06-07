from setuptools import setup, find_packages
import platform

with open('requirements.txt') as f:
    install_requirement = f.readlines()

setup(
    name="Job Application Bot",
    description="A Python termnial program that fetches jobs, writes and sends job applications!",
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
            "jabot = jabot.main:main"
        ]
    },
    scripts=["postinstall.bat"] if platform.system() == "Windows" else ["postinstall.sh"],
)
