sphinxcontrib-opendataservices
==============================

```eval_rst

.. rst:directive:: csv-table-no-translate

    .. markdown::

        Like
        [csv-table](http://docutils.sourceforge.net/docs/ref/rst/directives.html#csv-table),
        but the text inside the table is not translated. Useful when
        translation is handled by an external process, e.g. codelists.


.. rst:directive:: markdown

    A directive that renders its contents as markdown, using Recommonmark.


    .. markdown::

        Some markdown [a URL](http://example.org), `single backtick literals`. 

        ```eval_rst
        And even embedded ``eval_rst`` sections, if you need to use directives:

        .. csv-table-no-translate::

            1,2,3
            4,5,6
        ```

```
