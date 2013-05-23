from django import template


register = template.Library()


@register.simple_tag
def print_flash_messages(messages):
    output = ""
    cls_msg = {}
    types = []
    if len(messages) < 1:
        return ""

    for message in messages:
        if not message.tags in cls_msg:
            cls_msg[message.tags] = []

        cls_msg[message.tags].append(message)

    for type in cls_msg.keys():
        output += "<div id='messages_%s' class='messages %s'>" % (type, type)
        for message in cls_msg[type]:
            output += message.message
        output += "</div>"
    return output
