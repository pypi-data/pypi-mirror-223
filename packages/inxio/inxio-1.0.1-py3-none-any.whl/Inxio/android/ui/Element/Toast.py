from android.widget import Toast


class VToastType:
    # 显示时间2秒
    TYPE_SHORT = 0
    # 显示时间3.5秒
    TYPE_LONG = 1


def toast(central_activity, text, toast_type=VToastType.TYPE_SHORT):
    """
    显示小提示
    :param central_activity:CC
    :param text: 文字
    :param toast_type:类型，TYPE_SHORT为2秒，TYPE_LONG为3.5秒
    :return:
    """
    Toast.makeText(central_activity.java_activity, text, toast_type).show()
