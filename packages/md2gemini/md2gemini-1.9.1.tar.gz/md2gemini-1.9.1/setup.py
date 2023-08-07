import setuptools
from md2gemini import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="md2gemini",  # Replace with your own username
    version=__version__,
    author="makeworld",
    author_email="makeworld@protonmail.com",
    description="Convert Markdown to the Gemini text format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/makeworld-the-better-one/md2gemini",
    packages=["md2gemini"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: General",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mistune>=2.0.0,<3",
        "cjkwrap",
        "wcwidth",
    ],
    entry_points={"console_scripts": ["md2gemini = md2gemini:main"]},
)
