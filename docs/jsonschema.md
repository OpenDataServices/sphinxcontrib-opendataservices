# JSON Schema Directive

The core `jsonschema` directive is mainatined in another repository: [sphinxcontrib-jsonschema](https://github.com/OpenDataServices/sphinxcontrib-jsonschema)


`````eval_rst

.. rst:directive:: jsonschema

        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsonschema:: _static/example_schema.json
            ```

.. rst:directive:: jsonschema-titles
        
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
        
    Currently only used for 360Giving.
  
        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsonschema-title-fieldname-map:: _static/example_schema.json
            ```

.. rst:directive:: jsonschema-array
        
    Currently only used for OpenReferral.
  
        .. literal-and-parsed-markdown::
            
            ```eval_rst
            .. jsonschema-array:: _static/example_schema_array.json
            ```

````
