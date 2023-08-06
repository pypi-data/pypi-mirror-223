Just for probing to upload to public PyPI repo.

```shell
py -3.9 -m venv ./.venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt --upgrade
python -m unittest tests.test_foo
python setup.py sdist bdist_wheel
```
