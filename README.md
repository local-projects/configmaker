configmaker
===========

The `configmaker.py` script generates output based on a jinja template, 
by prompting for the values for each variable it encounters while
parsing the template.

The output is two files:

* rc_file, which contains all the variables
* config_file, which has the interpolated output based on the template and vars

An example is:

    configmaker.py --template config.yml.tmpl --rc_file rcfile --config_file config.yml

If the `rc_file` already exists, the variables in it will be used as the 
defaults in the prompts.

