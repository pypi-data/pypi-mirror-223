from setuptools import find_packages, setup


with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="deployment_package",
    version="0.0.9",
    description="Package for preprocessing functions used during Model Deployment module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidbognar201/Model_deployment_package",
    author="David Bognar",
    author_email="david.bognar@gmail.com",
    install_requires=["bson", "pandas", "scikit-learn", "numpy", "pydantic"],
    extras_require={
        "dev": ["pytest", "twine"],
    },
    python_requires=">=3.8",
    include_package_data=True,
    data_files=[("test_data", ["app/deployment_utils/test/data/test.pkl"])]
)