sphinxcontrib-opendataservices
==============================

`````eval_rst

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
`````


