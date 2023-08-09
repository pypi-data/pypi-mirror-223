# Pycurl

## Usage

```
pybasecurl https://nextjsvietnam.com --output nextjsvietnam.com.html
```

## Install env


```sh
pip3 install --user pipenv
pipenv --python 3.9
```

- Activate virtualenv : pipenv shell
- Install dependencies: pipenv install

## References

- [argparse](https://docs.python.org/3/library/argparse.html)
- [packaging project](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Sample package](https://github.com/pypa/sampleproject/blob/main/src/sample/__init__.py)

## Test package

```sh
pip install -e .
```

## Build package


```sh
python -m build
```

## Upload package

```sh
# test
twine upload --repository testpypi dist/*
# production
twine upload --repository pypi dist/*
```