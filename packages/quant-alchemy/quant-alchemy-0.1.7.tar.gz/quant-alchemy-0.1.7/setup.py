import setuptools

with open("README.md", "r") as file:
    readme = file.read()

setuptools.setup(
    name="quant-alchemy",
    version="0.1.7",
    author="Eladio Rocha Vizcaino",
    author_email="eladio.rocha99@gmail.com",
    description="Package for quantitative finance.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/EladioRocha/quant-alchemy",
    project_urls={
        "Bug Tracker": "https://github.com/EladioRocha/quant-alchemy/issues"
    },
    license="Apache License 2.0",
    packages=["quant_alchemy"],
    install_requires=["pandas", "numpy", "scipy"],
)