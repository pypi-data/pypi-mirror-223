from android.app import Notification
from android.graphics import BitmapFactory
from android.net import Uri
from android.app import NotificationChannel

from Inxio.android.core_components.Intent import VIntent
from Inxio.android.core_components.PendingIntent import VPendingIntent


class VNotificationManager:
    def __init__(self, java_nm):
        self.java_nm = java_nm

    def notify(self, id, notification):
        """
        发起一个通知
        :param id:通知的ID
        :param notification:NBuilder对象
        :return: None
        """
        if self.java_nm:
            self.java_nm.notify(id, notification)

    def cancel(self, id):
        """
        取消名为ID的通知，即删除消失此通知
        :param id: ID，int
        :return: None
        """
        if self.java_nm:
            self.java_nm.cancel(id)

    def cancel_all(self):
        """
        清除所有由此NM发出的通知，无视优先级
        :return: None
        """
        if self.java_nm:
            self.java_nm.cancelALL()


class VNotification:
    DEFAULT_ALL = ~0
    DEFAULT_SOUND = 1
    DEFAULT_VIBRATE = 2
    DEFAULT_LIGHTS = 4
    MAX_CHARSEQUENCE_LENGTH = 1024
    MAX_REPLY_HISTORY = 5
    MAX_LARGE_ICON_ASPECT_RATIO = 16 / 9
    MAX_ACTION_BUTTONS = 3
    EXTRA_REMOTE_INPUT_DRAFT = "android.remoteInputDraft"
    EXTRA_NOTIFICATION_ID = "android.intent.extra.NOTIFICATION_ID"
    EXTRA_NOTIFICATION_TAG = "android.intent.extra.NOTIFICATION_TAG"
    EXTRA_CHANNEL_GROUP_ID = "android.intent.extra.CHANNEL_GROUP_ID"
    EXTRA_CHANNEL_ID = "android.intent.extra.CHANNEL_ID"

    PRIORITY_DEFAULT = 0
    PRIORITY_LOW = -1
    PRIORITY_MIN = -2
    PRIORITY_HIGH = 1
    PRIORITY_MAX = 2

    def __init__(self):
        ...


class NBuilder:
    def __init__(self, control_activity):
        java_activity = control_activity.java_activity
        self.builder = Notification.Builder(java_activity)

    def set_auto_cancel(self, if_set: bool):
        """
        是否设置打开此通知，则通知自动消失
        :param if_set: bool
        :return: self
        """
        self.builder.setAutoCancel(if_set)
        return self

    def set_small_icon(self, source_int=-123456789, source_name="AUTO", v_activity=None):
        """
        设置小图标（即通知栏上显示的）,采用source_int获取或source_name+v_activity获取
        :param v_activity: 当采用source_name方式获取时，必须赋值此参数；如果采用source_int的方式则无需填写此参数
        :param source_name: 如果比较懒，可以直接输入资源名获取
        :param source_int: 可通过Activity().R.drawable["name"]获取
        :return:self
        """
        if source_int != -123456789:
            self.builder.setSmallIcon(source_int)
            return self
        elif source_name != "AUTO" and v_activity:
            self.builder.setSmallIcon(v_activity.R.drawable[f"{source_name}"])
            return self

    def set_text(self, text):
        """
        为通知对象设置内容
        :param text: str
        :return: self
        """
        self.builder.setContentText(text)
        return self

    def set_title(self, title_str):
        """
        为通知对象设置
        :param title_str: str
        :return: self
        """
        self.builder.setContentTitle(title_str)
        return self

    def set_defaults(self, defaults):
        """
        设置震动，LED，音乐等
        :param defaults: 可通过VNotification.*sth*获取
        :return:self
        """
        self.builder.setDefaults(defaults)
        return self

    def set_when(self, when):
        """
        设置显示时间！
        :param when:emm,你可以传入time.time()来表示为立刻显示
        :return: self
        """
        self.builder.setWhen(when)
        return self

    def set_sub_text(self, text):
        """
        设置附加文本
        :param text: str
        :return: self
        """
        self.builder.setSubText(text)
        return self

    def set_large_icon(self, source_name="AUTO", v_activity=None):
        """
        设置大图标（即下拉布局上显示的），采用source_name+v_activity获取
        :param v_activity: 当采用source_name方式获取时，必须赋值此参数；如果采用source_int的方式则无需填写此参数
        :param source_name: 资源名
        :return:self
        """
        if source_name != "AUTO" and v_activity:
            self.builder.setLargeIcon(
                BitmapFactory.decodeResource(
                    v_activity.get_resources(), v_activity.R.drawable[f"{source_name}"]
                )
            )
            return self

    def set_vibrate(self, type_list):
        """
        神奇的方法，自定义震动的方式（6）
        :param type_list: 震动方式列表,参数含义：[0,200,500,700]:延迟0ms，震动200ms；再延迟500ms，再震动700ms
        :return: self
        """
        self.builder.setVibrate(type_list)

    def set_sound(self, sound):
        """
        设置声音
        :param sound:你可以用VNotification.DEFAULT_SOUND即可
        :return:self
        """
        self.builder.setSound(sound)
        return self

    def set_sound_by_url(self, sound_url):
        """
        通过URL设置提示音
        :param sound_url:URL
        :return: self
        """
        sound = Uri.parse(sound_url)
        self.builder.setSound(sound)
        return self

    def set_ongoing(self, if_ongoing):
        """
        设置是否正在执行,设置为ture，表示它为一个正在进行的通知。
        他们通常是用来表示 一个后台任务,用户积极参与(如播放音乐)或以某种方式正在等待,
        因此占用设备(如一个文件下载, 同步操作,主动网络连接)
        :param if_ongoing:是否正在执行
        :return: self
        """
        self.builder.setOngoing(if_ongoing)
        return self

    def set_progress(self, max: int, now: int, if_clear: bool):
        """
        如果为确定的进度条：调用setProgress(max, progress, false)来设置通知，
        在更新进度的时候在此发起通知更新progress，并且在下载完成后要移除进度条 ，
        通过调用setProgress(0, 0, false)既可。

        如果为不确定（持续活动）的进度条， 这是在处理进度无法准确获知时显示活动正在持续，
        所以调用setProgress(0, 0, true) ，操作结束时，
        调用setProgress(0, 0, false)并更新通知以移除指示条

        :param max:最大值
        :param now:当前进度
        :param if_clear:是否清楚进度
        :return:self
        """
        self.builder.setProgress(max, now, if_clear)
        return self

    def set_priority(self, priority):
        """
        设置优先级
        VNotification.PRIORITY_MAX	重要而紧急的通知，通知用户这个事件是时间上紧迫的或者需要立即处理的。
        VNotification.PRIORITY_HIGH	高优先级用于重要的通信内容，例如短消息或者聊天，这些都是对用户来说比较有兴趣的。
        VNotification.PRIORITY_DEFAULT	默认优先级用于没有特殊优先级分类的通知。
        VNotification.PRIORITY_LOW	低优先级可以通知用户但又不是很紧急的事件。
        VNotification.PRIORITY_MIN	用于后台消息 (例如天气或者位置信息)。最低优先级通知将只在状态栏显示图标，只有用户下拉通知抽屉才能看到内容。
        :param priority: 优先级int,可通过VNotification.PRIORITY_*获取
        :return: self
        """
        self.builder.setPriority(priority)
        return self

    def set_intent(self, pending_intent):
        """
        设置Intent
        :param pending_intent: 可通过VPendingIntent.get_activity(....)获取
        :return: self
        """
        self.builder.setContentIntent(pending_intent)
        return self

    def build(self):
        """
        开始构建
        :return:self.builder.build()
        """
        return self.builder.build()


def integration_start_notification(activity,
                                   noti_id: int,
                                   intent: VPendingIntent,
                                   small_icon_name: str,
                                   text: str,
                                   title: str,
                                   auto_cancel=None,
                                   defaults=None,
                                   when=None,
                                   sub_text=None,
                                   large_icon_tuple=None,
                                   vibrate=None,
                                   sound=None,
                                   sound_url=None,
                                   ongoing=None,
                                   progress_tuple=None,
                                   priority=None,
                                   ):
    """
    为了方便大家使用消息通知这个函数！所以我将其整合为自选参数型函数（就和自助餐一样，你要什么功能自己填参数~）
    :param noti_id: 必填，通知ID int
    :param activity: 必填参数！当前Activity对象
    :param small_icon_name: 小图标资源名称
    :param text: 文字
    :param title: 题目

    :param auto_cancel: 是否点击后自动消失？(bool)
    :param defaults: 多感官控制，如震动、闪光灯
    :param when: 时间（ms）
    :param sub_text: 副标题文字
    :param large_icon_tuple: 大图标参数元组，参数含义：（source_name, v_activity）
    :param vibrate: 神奇的方法，自定义震动的方式
    :param sound: 声音，你可以用VNotification.DEFAULT_SOUND即可
    :param sound_url: 声音URL，但注意，此参数不得与参数sound共存！
    :param ongoing:是否正运行？
    :param progress_tuple:设置进度条参数元组，参数含义（max,now,if_clear）
    :param priority:优先级
    :param intent:PendingIntent
    :return:None
    """
    n_builder = NBuilder(activity)
    n_builder.set_title(title)
    n_builder.set_text(text)
    n_builder.set_small_icon(source_name=small_icon_name)
    # 设置附加参数
    if auto_cancel:
        n_builder.set_auto_cancel(auto_cancel)
    if defaults:
        n_builder.set_defaults(defaults)
    if when:
        n_builder.set_when(when)
    if sub_text:
        n_builder.set_sub_text(sub_text)
    if large_icon_tuple:
        n_builder.set_large_icon(large_icon_tuple[0], large_icon_tuple[1])
    if vibrate:
        n_builder.set_vibrate(vibrate)
    if sound:
        n_builder.set_sound(sound)
    if sound_url:
        n_builder.set_sound_by_url(sound_url)
    if ongoing:
        n_builder.set_ongoing(ongoing)
    if progress_tuple:
        n_builder.set_progress(max=progress_tuple[0], now=progress_tuple[1], if_clear=progress_tuple[2])
    if priority:
        n_builder.set_priority(priority=priority)
    # 附加参数设置完毕
    n_builder.set_intent(intent)

    activity.get_notification_manager().notify(id=noti_id, notification=n_builder)


def start_notification_jump(activity,
                            noti_id: int,
                            new_activity_name: str,
                            small_icon_name: str,
                            text: str,
                            title: str,
                            auto_cancel=None,
                            defaults=None,
                            when=None,
                            sub_text=None,
                            large_icon_tuple=None,
                            vibrate=None,
                            sound=None,
                            sound_url=None,
                            ongoing=None,
                            progress_tuple=None,
                            priority=None):
    """
    参数同integration_start_notification
    此函数封装成程度更高
    更改的参数：new_activity_class：请填入目标Activity类的字符串名称！
    """
    intent = VIntent(activity, new_activity_name)
    pending_intent = VPendingIntent().get_activity(activity, 0, intent, 0)
    integration_start_notification(activity, noti_id, pending_intent, small_icon_name, text, title, auto_cancel,
                                   defaults, when,
                                   sub_text, large_icon_tuple, vibrate, sound, sound_url, ongoing, progress_tuple,
                                   priority)
