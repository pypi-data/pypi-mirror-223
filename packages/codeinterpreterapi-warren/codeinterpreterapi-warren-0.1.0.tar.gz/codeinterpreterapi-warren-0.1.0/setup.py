from setuptools import setup, find_packages  
  
setup(  
    name="codeinterpreterapi-warren",  
    version="0.1.0",  
    packages=find_packages(),  
    install_requires=[  
        # List your library's dependencies here  
    ],  
    author="Warren Wong",  
    author_email="wwwc@outlook.com",  
    description="Fork of https://github.com/shroominic/codeinterpreter-api",  
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",  
    url="https://github.com/somethingwentwell/codeinterpreter-api",  
    classifiers=[  
        "Development Status :: 3 - Alpha",  
        "License :: OSI Approved :: MIT License",  
        "Programming Language :: Python :: 3",  
        "Programming Language :: Python :: 3.6",  
        "Programming Language :: Python :: 3.7",  
        "Programming Language :: Python :: 3.8",  
        "Programming Language :: Python :: 3.9",  
        "Programming Language :: Python :: 3 :: Only",
    ],  
)  