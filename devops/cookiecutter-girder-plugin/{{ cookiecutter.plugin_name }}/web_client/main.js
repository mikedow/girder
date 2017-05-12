import { registerPluginNamespace } from 'girder/pluginUtils';
import * as {{ cookiecutter.plugin_nice_name|title|replace(" ", "") }} from './index';

registerPluginNamespace('{{ cookiecutter.plugin_name }}', {{ cookiecutter.plugin_nice_name|title|replace(" ", "") }});
