from django import template
from datetime import datetime

register = template.Library()


def datetimeformat(datetime_object):

    date = datetime.strftime(datetime_object, "%d.%m.%Y")

    return date


register.filter("datetimeformat", datetimeformat)
