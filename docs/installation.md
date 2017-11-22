# Installation 

Add this line to your `requirements.txt`:

```none
-e git+https://github.com/OpenDataServices/sphinxcontrib-opendataservices.git@23ce17656feaa237584af8822bd57ac39b498f93#egg=sphinxcontrib-opendataservices
```

Then run `pip install -r requirements.txt`.

Edit your doc's `conf.py` and add `sphinxcontrib.opendataservices` to the `extensions` array.

e.g.
```python
extensions = ['sphinxcontrib.opendataservices']
```
