from distutils.core import setup

description = """
Python package to read and write network graphs in GDF (Graph Data Format).
"""

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="gdf",
    version="1.0.1",
    description=description.strip(),
    long_description=long_description,
    install_requires=install_requires,
    url="https://github.com/nelsonaloysio/gdf",
    author="Nelson Aloysio Reis de Almeida Passos",
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=["GDF", "Graph", "Network", "NetworkX"],
    python_requires=">=3",
    py_modules=["gdf"],
    project_urls={
        "Source": "https://github.com/nelsonaloysio/gdf",
        "Tracker": "https://github.com/nelsonaloysio/gdf/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
