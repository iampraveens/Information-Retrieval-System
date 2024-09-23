import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    
__version__ = "0.0.1"

REPO_NAME = "Information-Retrieval-System"
AUTHOR_USER_NAME = "iampraveens"
SRC_REPO = "InformationRetrievalSystem"
AUTHOR_EMAIL = "praveensivaprakasham@gmail.com"

setuptools.setup(
    name=SRC_REPO,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    version=__version__,
    description="A python package for an Gen-AI App",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)