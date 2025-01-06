from setuptools import setup, find_packages

setup(
    name="recipe_rag_packages",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
