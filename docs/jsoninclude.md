# JSON Include Directives

`````eval_rst

.. rst:directive:: jsoninclude

    .. markdown::

        Include a section of a JSON file, given a [jsonpointer](https://tools.ietf.org/html/rfc6901).
        
        e.g. using [this json file](_static/example.json):

    ..

        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsoninclude:: _static/example.json
                :jsonpointer: /a/0/b
            ```

    ``exclude`` option:

        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsoninclude:: _static/example.json
                :jsonpointer: /a/0/b
                :exclude: e,g
            ```

    ``include_only`` option:

        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsoninclude:: _static/example.json
                :jsonpointer: /a/0/b
                :include_only: e,g
            ```

.. rst:directive:: jsoninclude-flat

    .. markdown::

        Include a section of a JSON file, **flattened into a table representation**, given a [jsonpointer](https://tools.ietf.org/html/rfc6901).
        
        Examples, using [this json file](_static/example.json):

    ..

        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsoninclude-flat:: _static/example.json
                :jsonpointer: /a/0/b
            ```

    ``recursive`` (include nested dicts and lists):

        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsoninclude-flat:: _static/example.json
                :jsonpointer: /a/0/b
                :recursive:
            ```

    List of items directly under the json pointer:

        .. literal-and-parsed-markdown::

            ```eval_rst
            .. jsoninclude-flat:: _static/example.json
                :jsonpointer: /h
            ```

    Remove part of the path from the headings uwsing ``ignore_path``:

        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsoninclude-flat:: _static/example.json
                :jsonpointer: /a/0/b
                :ignore_path: /a/0/b/
            ```

    ``jsoninclude-flat`` also has the options ``exclude`` and ``include_only``, the
    same as for ``jsoninclude`` (see above).

`````
