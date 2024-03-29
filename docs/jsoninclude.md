# JSON Include Directives

## Standard JSON Include

`````{eval-rst}

.. rst:directive:: jsoninclude

    .. markdown::

        Include a section of a JSON file, given a [jsonpointer](https://tools.ietf.org/html/rfc6901).
        
        e.g. using [this json file](_static/example.json):

    ..

        .. literal-and-parsed-markdown::
            
            ```{eval-rst}
            .. jsoninclude:: _static/example.json
                :jsonpointer: /a/0/b
                :expand: e
            ```

    The ``expand`` option is needed to expand a list when the json is folded by javascript. For more info see :ref:`jsoninclude_javascript` below.

    ``exclude`` option:

        .. literal-and-parsed-markdown::
            
            ```{eval-rst}
            .. jsoninclude:: _static/example.json
                :jsonpointer: /a/0/b
                :exclude: e,g
            ```

    ``include_only`` option:

        .. literal-and-parsed-markdown::
            
            ```{eval-rst}
            .. jsoninclude:: _static/example.json
                :jsonpointer: /a/0/b
                :include_only: e,g
                :expand: e
            ```

.. _jsoninclude_javascript:
`````
### Javascript

To fold the JSON with javascript, you need to include  the following files:

* [renderjson.css](https://github.com/OpenDataServices/sphinxcontrib-opendataservices/blob/master/docs/_static/renderjson.css)
* [renderjson.js](https://github.com/OpenDataServices/sphinxcontrib-opendataservices/blob/master/docs/_static/renderjson.js)
* [json-example-format.js](https://github.com/OpenDataServices/sphinxcontrib-opendataservices/blob/master/docs/_static/json-example-format.js)

You need to add the files to a `_static` folder within your docs, and then add the following to `_templates/layout.html`.

```
{% extends "!layout.html" %}
{% set css_files = css_files + ["_static/renderjson.css"] %}
{% set script_files = script_files + ["_static/renderjson.js", "_static/json-example-format.js"] %}
```

The option `expand` can be used to control which lists are expanded initially. The option `title` can be used to give the json include a title; only one of consecutive includes will be shown, with a select box to switch:

`````{eval-rst}

.. literal-and-parsed-markdown::

    ```{eval-rst}
    .. jsoninclude:: _static/example.json
        :jsonpointer: 
        :title: collapsed

    .. jsoninclude:: _static/example.json
        :jsonpointer: 
        :expand: a,b,e,h
        :title: expanded
    ```

`````

## Flat JSON Include

`````{eval-rst}

.. rst:directive:: jsoninclude-flat

    .. markdown::

        Include a section of a JSON file, **flattened into a table representation**, given a [jsonpointer](https://tools.ietf.org/html/rfc6901).
        
        Examples, using [this json file](_static/example.json):

    ..

        .. literal-and-parsed-markdown::
            
            ```{eval-rst}
            .. jsoninclude-flat:: _static/example.json
                :jsonpointer: /a/0/b
            ```

    ``recursive`` (include nested dicts and lists):

        .. literal-and-parsed-markdown::
            
            ```{eval-rst}
            .. jsoninclude-flat:: _static/example.json
                :jsonpointer: /a/0/b
                :recursive:
            ```

    List of items directly under the json pointer:

        .. literal-and-parsed-markdown::

            ```{eval-rst}
            .. jsoninclude-flat:: _static/example.json
                :jsonpointer: /h
            ```

    Remove part of the path from the headings uwsing ``ignore_path``:

        .. literal-and-parsed-markdown::
            
            ```{eval-rst}
            .. jsoninclude-flat:: _static/example.json
                :jsonpointer: /a/0/b
                :ignore_path: /a/0/b/
            ```

    ``jsoninclude-flat`` also has the options ``exclude`` and ``include_only``, the
    same as for ``jsoninclude`` (see above).

`````


## JSON Include Quoted

`````{eval-rst}

.. rst:directive:: jsoninclude-quote

    .. markdown::

        Include a value from a JSON file, inside a blockquote, given a [jsonpointer](https://tools.ietf.org/html/rfc6901).

        e.g. using [this json file](_static/example_schema.json):

    ..

        .. literal-and-parsed-markdown::

            ```{eval-rst}
            .. jsoninclude-quote:: _static/example_schema.json
                :jsonpointer: /properties/lorem/description
            ```

`````
