from django import template
from django.db.models.query import QuerySet
from django.contrib.auth import get_user_model

from cmdb.models import Code, Cabinet

register = template.Library()

User = get_user_model()


@register.simple_tag
def get_con(context, arg, field):
    if isinstance(context, QuerySet):
        context = context.values()
        instance = [con for con in context if con['id'] == arg]
        if instance:
            return instance[0][field]
        return ''


@register.filter(name='compare_result')
def get_change_compare(changes):
    change_compare = []
    for key, value in changes.items():
        if key in ['network_type', 'service_type', 'operation_type']:
            log = replace_log(key, value, Code, 'value')
        elif key == 'dev_cabinet':
            log = replace_log(key, value, Cabinet, 'number')
        else:
            log = '字段："%(field)s"，由："%(old)s"，变更为："%(new)s"。' % {
                'field': key,
                'old': value[0],
                'new': value[1]
            }
        change_compare.append(log)
    return '，'.join(str(i) for i in change_compare)


def replace_log(key, value, model, field):
    old = value[0]
    new = value[1]
    log_format = '字段："%(field)s"，由："%(old)s"，变更为："%(new)s"。'
    try:
        data = model.objects.filter(id=old).values()[0]
        old_data = data[field]
    except Exception:
        old_data = old
    try:
        data = model.objects.filter(id=new).values()[0]
        new_data = data[field]
    except Exception:
        new_data = new
    return log_format % {
        'field': key,
        'old': old_data,
        'new': new_data
    }