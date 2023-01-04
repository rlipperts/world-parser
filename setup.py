import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

test_deps = [
    'tox',
    'pytest',
    'flake8',
    'pylint',
    'mypy',
]
extras = {
    'test': test_deps
}

setuptools.setup(
    name="world-parser",
    version="0.0.0",
    author="Ruben Lipperts",
    author_email="",
    description="Parses information about the real world from different sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rlipperts/world-parser",
    package_dir={'': 'src'},
    packages=['world_parser'],
    package_data={'world_parser': ['py.typed']},
    tests_require=test_deps,
    extras_require=extras,
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires='~=3.11',
)
