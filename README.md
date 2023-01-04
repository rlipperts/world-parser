# python_package_template
_Default files and structure for python package repositories (aimed at personal use)_

## installation
There are no PyPI releases. Neither are they planned.

### manual
For installation with pip directly from this GitHub repository simply open a terminal and type
```
pip install git+ssh://git@github.com/rlipperts/python_package_template.git
```

### setup.py
To automatically install <your package name> with your python package include these lines in your setup.py
```python
install_requires = [
    'python-package-template @ git+ssh://git@github.com/rlipperts/python-package-template.git@master#egg=python-package-template-0.0.0',
],
```
Make sure you update the version in the `egg=python-package-template-...` portion to the correct version specified in the <your package name> setup.py. This might not work if you plan on publishing your package on PyPI.

## usage

Write a more or less detailed description on how to use your package!
