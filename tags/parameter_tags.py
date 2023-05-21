from django import template
register = template.Library()
from lib import parameters

@register.simple_tag
def get_subscription_types():
    return str(parameters.License.subscription_types).replace("'", "\"")