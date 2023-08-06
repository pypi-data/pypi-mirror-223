from setuptools import setup, find_packages

# Read README for the long description
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="tidy-dir",
    version="0.0.2",
    author="mka142",
    author_email="mka@diveinai.com",
    url="https://github.com/mka142/tidy-dir",
    description="A package to tidy up directories using a configuration file",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={"console_scripts": ["tidy-dir = tidy_dir.cli:main"]},
    install_requires=[
        # Add any dependencies required by your package here
    ],
)
