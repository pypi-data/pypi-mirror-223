from setuptools import setup, find_packages

setup(
    name="Jakit",
    version="0.4",
    packages=find_packages(),
    author="Idriss Animashaun",
    author_email="idriss.animashaun@intel.com",
    description="Just Another Kappa Information Tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iddy-ani/Jakit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        
    ],
    python_requires='>=3.10',
)
