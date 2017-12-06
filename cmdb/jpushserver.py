import jpush
from jpush import common

_jpush = jpush.JPush('043317222d3cf4d1f1444b6a', '76da9381aff0b45c6726061b')
_jpush.set_logging("DEBUG")
push = _jpush.create_push()


# if you set the logging level to "DEBUG",it will show the debug logging.


def alias_notification(mac, message):
    push.audience = jpush.audience(
        jpush.alias(mac)
    )
    push.notification = jpush.notification(alert=message)
    push.platform = jpush.all_
    print(push.payload)
    push.send()


def alias_message(mac, message):
    push.audience = jpush.audience(
        jpush.alias(mac)
    )


alias_notification('guishuai', 'hello guishuai')
