from setuptools import setup, find_packages

setup(
    name="for-your-service",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.31.0",
        "pydantic>=2.0.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "sentence-transformers>=2.2.0",
        "torch>=2.0.0",
    ],
    author="Free Hall",
    author_email="whall4.wh@gmail.com",
    description="AI-powered veteran job matching platform",
    url="https://github.com/For-Your-Service/For-Your-Service",
    python_requires=">=3.11",
)
