sphinxcontrib-opendataservices
==============================

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

.. rst:directive:: jsoninclude-flat

    .. markdown::

        Include a section of a JSON file, **flattened into a table representation table**, given a [jsonpointer](https://tools.ietf.org/html/rfc6901).

        Examples, using [this json file](_static/example.json):

    ..

        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsoninclude-flat:: _static/example.json
                :jsonpointer: /a/0/b
            ```

    List of items directly under the json pointer:

        .. literal-and-parsed-markdown::

            ```eval_rst
            .. jsoninclude-flat:: _static/example.json
                :jsonpointer: /g
            ```

.. rst:directive:: csv-table-no-translate

    .. markdown::

        Like
        [csv-table](http://docutils.sourceforge.net/docs/ref/rst/directives.html#csv-table),
        but the text inside the table is not translated. Useful when
        translation is handled by an external process, e.g. codelists.


.. rst:directive:: markdown

    A directive that renders its contents as markdown, using Recommonmark.


        .. literal-and-parsed-markdown::

            ```eval_rst
            .. markdown::

                Some markdown [a URL](http://example.org), `single backtick literals`. 
            ```

    This is not so useful by itself, but allows markdown to be embedded inside
    other directives, e.g.:

        .. literal-and-parsed-markdown::

            ```eval_rst
            .. admonition:: Worked example
                :class: hint

                .. markdown::

                    Some markdown [a URL](http://example.org), `single backtick literals`.
            ```

.. rst:directive:: directory_list

`````


