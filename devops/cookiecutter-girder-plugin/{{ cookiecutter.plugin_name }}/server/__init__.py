#!/usr/bin/env python
# -*- coding: utf-8 -*-
{% if cookiecutter.server_events -%}
from girder import events
from girder.utility.model_importer import ModelImporter
{%- endif %}
{% if cookiecutter.server_endpoints -%}
from .rest import {{ cookiecutter.plugin_name}}
{%- endif %}


{% if cookiecutter.server_events -%}
# For more information on the events system, see:
# http://girder.readthedocs.io/en/latest/plugin-development.html#the-events-system
def myAfterSaveEvent(event, item):
    ModelImporter.model('item').setMetadata(item, {
        'my_after_save_event': 'success!'
    })
{%- endif %}


{% if cookiecutter.server_endpoints or cookiecutter.server_events -%}
# For more information on loading custom plugins, see:
# http://girder.readthedocs.io/en/latest/plugin-development.html#extending-the-server-side-application
def load(info):
    {% if cookiecutter.server_endpoints -%}
    info['apiRoot'].{{ cookiecutter.plugin_name }} = {{ cookiecutter.plugin_name }}()
    {%- endif %}

    {% if cookiecutter.server_events -%}
    events.bind('model.item.save.after', 'my_after_save_event', myAfterSaveEvent)
    {%- endif %}
{%- endif %}
