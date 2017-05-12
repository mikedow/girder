{% if cookiecutter.server_endpoints -%}
from girder.api import access
from girder.api.describe import Description, autoDescribeRoute
from girder.api.rest import Resource
{%- endif %}


{% if cookiecutter.server_endpoints -%}
# For more information on adding new resources to the Web API, see:
# http://girder.readthedocs.io/en/latest/plugin-development.html#adding-a-new-resource-type-to-the-web-api
class {{ cookiecutter.plugin_name }}(Resource):
    def __init__(self):
        super({{ cookiecutter.plugin_name }}, self).__init__()
        self.resourceName = '{{ cookiecutter.plugin_name }}'

        self.route('GET', (), self.listResource)
        self.route('GET', (':id',), self.getResource)

    # For more information on adding routes to the Web API, see:
    # http://girder.readthedocs.io/en/latest/plugin-development.html#adding-a-new-route-to-the-web-api
    @access.public
    @autoDescribeRoute(
        Description('List resources.'))
    def listResource(self, params):
        return ['resource1', 'resource2']

    @access.public
    @autoDescribeRoute(
        Description('Get a resource by ID.')
        .param('id', 'The ID of the resource.', required=True))
    def getResource(self, id, params):
        return 'resource%s' % id
{%- endif %}
