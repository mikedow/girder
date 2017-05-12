get_filename_component(PLUGIN ${CMAKE_CURRENT_LIST_DIR} NAME)

{% if cookiecutter.server_tests -%}
# Add test for plugin_tests/{{ cookiecutter.plugin_name }}_test.py
add_python_test({{ cookiecutter.plugin_name }} PLUGIN ${PLUGIN})

# Add static analysis (style) tests for python files in server and plugin_tests
add_python_style_test(python_static_analysis_${PLUGIN}
  "${PROJECT_SOURCE_DIR}/plugins/${PLUGIN}/server")
add_python_style_test(python_static_analysis_${PLUGIN}_tests
  "${PROJECT_SOURCE_DIR}/plugins/${PLUGIN}/plugin_tests")
{%- endif %}

{% if cookiecutter.client_tests -%}
# Add JS test for plugin_tests/{{ cookiecutter.plugin_name }}Spec.js
add_web_client_test(${PLUGIN}
  "${PROJECT_SOURCE_DIR}/plugins/${PLUGIN}/plugin_tests/{{ cookiecutter.plugin_name }}Spec.js"
  PLUGIN ${PLUGIN})

# For more on linting/style checking, see:
# http://girder.readthedocs.io/en/latest/plugin-development.html#linting-and-style-checking-client-side-code

# Add static analysis (style) tests for any JavaScript files in web_client
add_eslint_test(${PLUGIN} "${PROJECT_SOURCE_DIR}/plugins/${PLUGIN}/web_client")

# Add static analysis (style) tests for any Pug files in templates
add_puglint_test(${PLUGIN} "${PROJECT_SOURCE_DIR}/plugins/${PLUGIN}/web_client/templates")
{%- endif %}
