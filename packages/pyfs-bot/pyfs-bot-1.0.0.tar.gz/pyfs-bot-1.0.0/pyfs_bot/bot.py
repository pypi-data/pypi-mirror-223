import base64
import hashlib
import hmac
import time
from typing import Any, Dict

from pyfs_base import BaseFeishu


class Bot(BaseFeishu):
    def __init__(self, hook_id: str = None, key_word: str = None, secret: str = None) -> None:
        super(Bot, self).__init__()
        self.hook_id = hook_id
        self.key_word = key_word
        self.secret = secret
        # https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot
        # curl -X POST -H "Content-Type: application/json" \
        #     -d '{"msg_type":"text","content":{"text":"request example"}}' \
        #     https://open.feishu.cn/open-apis/bot/v2/hook/****
        self.WEBHOOK_URL = self.OPEN_DOMAIN + '/open-apis/bot/v2/hook/{hook_id}'

    def __gen_sign(self, timestamp: int, secret: str) -> str:
        # 拼接timestamp和secret
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        hmac_code = hmac.new(string_to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign

    def send_hook_message(self, data: Dict[str, Any], hook_id: str = None, secret: str = None) -> Dict[str, Any]:
        hook_id = hook_id or self.hook_id
        secret = secret or self.secret
        if secret:
            timestamp = int(time.time())
            data['timestamp'] = timestamp
            data['sign'] = self.__gen_sign(timestamp, secret)
        return self.post(self.WEBHOOK_URL.format(hook_id=hook_id), data=data)

    # 发送文本消息
    def send_hook_text_message(self, message: str, hook_id: str = None, key_word: str = None, secret: str = None) -> Dict[str, Any]:
        key_word = key_word or self.key_word
        if key_word:
            message = '【{0}】{1}'.format(key_word, message)
        data = {
            'msg_type': 'text',
            'content': {
                'text': message,
            }
        }
        return self.send_hook_message(data, hook_id=hook_id, secret=secret)

    # 发送富文本消息
    def send_hook_post_message(self, post: Dict[str, Any], hook_id: str = None, key_word: str = None, secret: str = None) -> Dict[str, Any]:
        key_word = key_word or self.key_word
        if key_word:
            for lang in post:
                post[lang]['title'] = '【{0}】{1}'.format(key_word, post[lang]['title'])
        data = {
            'msg_type': 'post',
            'content': {
                'post': post,
            }
        }
        return self.send_hook_message(data, hook_id=hook_id, secret=secret)

    # 发送群名片
    def send_hook_share_chat_message(self, share_chat_id: str, hook_id: str = None, secret: str = None) -> Dict[str, Any]:
        # 群 ID 说明: https://open.feishu.cn/document/server-docs/group/chat/chat-id-description
        data = {
            'msg_type': 'share_chat',
            'content': {
                'share_chat_id': share_chat_id,
            }
        }
        return self.send_hook_message(data, hook_id=hook_id, secret=secret)

    # 发送图片
    def send_hook_image_message(self, image_key: str, hook_id: str = None, secret: str = None) -> Dict[str, Any]:
        # 群 ID 说明: https://open.feishu.cn/document/server-docs/group/chat/chat-id-description
        data = {
            'msg_type': 'image',
            'content': {
                'image_key': image_key,
            }
        }
        return self.send_hook_message(data, hook_id=hook_id, secret=secret)

    # 发送消息卡片
    def send_hook_interactive_message(self, interactive: Dict[str, Any], hook_id: str = None, secret: str = None) -> Dict[str, Any]:
        # 卡片结构介绍: https://open.feishu.cn/document/common-capabilities/message-card/message-cards-content/card-structure/card-content
        # 消息卡片搭建工具: https://open.feishu.cn/document/common-capabilities/message-card/message-card-builder
        data = {
            'msg_type': 'interactive',
            'card': interactive,
        }
        return self.send_hook_message(data, hook_id=hook_id, secret=secret)


bot = Bot()
send_hook_message = bot.send_hook_message
send_hook_text_message = bot.send_hook_text_message
send_hook_post_message = bot.send_hook_post_message
send_hook_share_chat_message = bot.send_hook_share_chat_message
send_hook_image_message = bot.send_hook_image_message
send_hook_interactive_message = bot.send_hook_interactive_message
