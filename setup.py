from setuptools import setup, find_packages

setup(
    name="chain-translator",
    version="1.0.0",
    description="Multi-language chain translation tool with audio output",
    author="LingLan",
    author_email="3047493305@qq.com",
    url="https://github.com/vers123/chain-translator",
    py_modules=["translator_chain"],
    install_requires=[
        "gTTS>=2.5.0",
        "translators>=5.9.0",
        "deep-translator>=1.11.0",
        "urllib3==1.26.18",
    ],
    entry_points={
        "console_scripts": [
            "chain-translator=translator_chain:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)