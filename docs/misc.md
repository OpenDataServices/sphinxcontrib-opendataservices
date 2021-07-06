# Misc Directives

`````{eval-rst}

.. rst:directive:: csv-table-no-translate

    .. markdown::

        Like
        [csv-table](http://docutils.sourceforge.net/docs/ref/rst/directives.html#csv-table),
        but the text inside the table is not translated. Useful when
        translation is handled by an external process, e.g. codelists.

    | ``included_cols`` is the optional list of indices of columns to include.
    |

.. rst:directive:: markdown

    A directive that renders its contents as markdown, using Recommonmark.


        .. literal-and-parsed-markdown::

            ```{eval-rst}
            .. markdown::

                Some markdown [a URL](http://example.org), `single backtick literals`. 
            ```

    This is not so useful by itself, but allows markdown to be embedded inside
    other directives, e.g.:

        .. literal-and-parsed-markdown::

            ```{eval-rst}
            .. admonition:: Worked example
                :class: hint

                .. markdown::

                    Some markdown [a URL](http://example.org), `single backtick literals`.
            ```

.. rst:directive:: directory_list

    Return a bullet list for files in a directory.

    | ``path`` is the path of the directory.
    | ``url`` is a url prefix to form the links
    |

    Example:

        .. literal-and-parsed-markdown::

            ```{eval-rst}
            .. directory_list::
                :path: exampledir
                :url: https://github.com/OpenDataServices/sphinxcontrib-opendataservices/blob/master/docs/exampledir/
            ```

.. rst:directive:: localization-note
   
   Create a note admonition that only will appear in languages that have "translated" it. This will not appear in the base language (normally English). If a translator wants to mark they have seen the message but do not want to add a note then they can leave a single hyphen '-'. The contents of the translation will be treated as markdown. The text within the directive should contain information useful for the translator and instruct what to do when they encouter this. For example::

    ```{eval-rst}
    .. localization-note:: 

      DO NOT TRANSLATE THIS MESSAGE DIRECTLY

      Instead put some language specific context as to how to interpret this page.
      
      Put a '-' if you do not want this note to appear in this language. 
    ```

`````

## Directives in other repositories 

* [ocds_sphinx_directives](https://github.com/open-contracting/ocds_sphinx_directives) contains extensions that are specific to OCDS docs sites. Currently they all relate to extensions.
* [OpenReferral's JSON Table Schema include](https://github.com/openreferral/specification/blob/master/docs/conf.py#L381), because this is the only docs site we maintain that uses JSON Table Schema.
