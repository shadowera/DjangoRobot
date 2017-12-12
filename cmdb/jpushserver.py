import jpush
from jpush import common

_jpush = jpush.JPush('043317222d3cf4d1f1444b6a', '76da9381aff0b45c6726061b')
_jpush.set_logging("DEBUG")
push = _jpush.create_push()


# if you set the logging level to "DEBUG",it will show the debug logging.


def push_alias_notification(mac, message):
    push.audience = jpush.audience(
        jpush.alias(mac)
    )
    push.notification = jpush.notification(alert=message)
    push.platform = jpush.all_
    print(push.payload)
    push.send()


def push_alias_message(mac, content, **kwargs):
    push.audience = jpush.audience(
        jpush.alias(mac)
    )
    push.message = jpush.message(content, extras=kwargs)
    push.platform = 'android'
    print('payload:...=%s' % push.payload)
    push.send()


if __name__ == '__main__':
    push_alias_message('guishuai', 'hello world', data_from='data_form')
