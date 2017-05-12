import os
import shutil

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)
PLUGIN_TEST_DIR = os.path.exists(os.path.join(PROJECT_DIRECTORY, 'plugin_tests'))

if '{{ cookiecutter.server_tests }}' == 'n' and '{{ cookiecutter.client_tests }}' == 'n':
    if os.path.exists(PLUGIN_TEST_DIR):
        shutil.rmtree(PLUGIN_TEST_DIR)

    if os.path.exists(os.path.join(PROJECT_DIRECTORY, 'plugin.cmake')):
        os.remove(os.path.join(PROJECT_DIRECTORY, 'plugin.cmake'))
elif '{{ cookiecutter.server_tests }}' == 'n':
    if os.path.exists(os.path.join(PLUGIN_TEST_DIR, '{{ cookiecutter.plugin_name }}_test.py')):
        os.remove(os.path.join(PLUGIN_TEST_DIR, '{{ cookiecutter.plugin_name }}_test.py'))

    if os.path.exists(os.path.join(PLUGIN_TEST_DIR, '__init__.py')):
        os.remove(os.path.join(PLUGIN_TEST_DIR, '__init__.py'))
elif '{{ cookiecutter.client_tests }}' == 'n':
    if os.path.exists(os.path.join(PLUGIN_TEST_DIR, '{{ cookiecutter.plugin_name }}Spec.js')):
        os.path.join(PLUGIN_TEST_DIR, '{{ cookiecutter.plugin_name }}Spec.js')
