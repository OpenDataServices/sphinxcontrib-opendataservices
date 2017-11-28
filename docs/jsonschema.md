# JSON Schema Directives

`````eval_rst

.. rst:directive:: jsonschema
        
        .. markdown::

            The core `jsonschema` directive, mainatined in [the sphinxcontrib-jsonschema repository](https://github.com/OpenDataServices/sphinxcontrib-jsonschema).

        The exact output of this is somewhat specific to the OCDS usecases, so
        we subclass the directive to create alternatives for other data
        standards, see below.

        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsonschema:: _static/example_schema.json
            ```

.. rst:directive:: jsonschema-titles

    Display titles, but not field names.
        
    Currently only used for 360Giving.

        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsonschema-titles:: _static/example_schema.json
            ```

        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsonschema-titles:: _static/example_schema.json
                :child: subthings
            ```

.. rst:directive:: jsonschema-title-fieldname-map

    Display the mapping between titles and field names.
        
    Currently only used for 360Giving.
  
        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsonschema-title-fieldname-map:: _static/example_schema.json
            ```

.. rst:directive:: jsonschema-array

    Handle a jsonschema where the top element is an array. Don't display titles
    in the table.
        
    Currently only used for OpenReferral.
  
        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsonschema-array:: _static/example_schema_array.json
            ```

`````

## CSS

To display the tables better, add this css to your site: [jsonschema.css](https://github.com/OpenDataServices/sphinxcontrib-opendataservices/blob/master/docs/_static/jsonschema.css).
