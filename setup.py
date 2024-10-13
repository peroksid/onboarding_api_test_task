from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()


def topfile_contents(file_name):
    return (here / file_name).read_text(encoding="utf-8")


def topfile_lines(file_name):
    return [x for x in topfile_contents(file_name).splitlines() if x.strip() != '']


setup(
    name="onboarding_api",
    version="0.0.1",
    description="An example API to upload and parse files",
    long_description=topfile_contents("README.md"),
    long_description_content_type="text/markdown", 
    url="https://github.com/pypa/sampleproject",
    author="Alexander Pugachev",
    author_email="alexander.pugachev@gmail.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.11, <4",
    install_requires=topfile_lines("requirements.txt"),
    extras_require={
        "dev": topfile_lines("dev_requirements.txt"),
        "test": topfile_lines("test_requirements.txt")
    },
    include_package_data=True
)