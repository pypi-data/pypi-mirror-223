# OMSens - python package builder

OpenModelica sensitivity analysis and optimization module.

## Dependencies

- [OpenModelica](https://openmodelica.org)
- [Python >= 3.6](https://www.python.org/)
- [Python setuptools](https://pypi.org/project/setuptools/)

## Supported platforms

- Linux

## Build/Install instructions


Install the dependencies mentioned above and then run the following commands in the `terminal`.

```bash
$ python3 -m build
```

Publish package in pypi repository
```bash
$ python3 -m twine upload --repository testpypi dist/*
```
