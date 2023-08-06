import aiohttp
import requests
from typing import Optional


class Chat:
    headers: Optional[dict] = {}
    base_url: Optional[str] = "https://test.api.anyask.ai.:8888"
    path_messages: Optional[str] = "/chat/messages"

    def messages(self, data) -> str:
        if data.get('stream'):
            raise Exception("Don't support stream'")
        resp = requests.post(
            url=self.base_url + self.path_messages,
            headers=self.headers,
            json=data
        )
        if resp.status_code >= 200 and resp.status_code < 300:
            resp = resp.json()
            content = resp.get("choices")[0].get("message", {}).get("content", "")
            if content == "":
                content = resp.get("choices")[0].get("delta", {}).get("content", "")
            return content
        else:
            return resp.text

    async def amessages(self, data: dict) -> str:
        if data.get('stream'):
            raise Exception("Don't support stream'")
        async with aiohttp.ClientSession(self.base_url) as session:
            async with session.post(self.path_messages, json=data) as resp:
                chat_msg: dict = await resp.json()
                content = chat_msg.get("choices")[0].get("message", {}).get("content", "")
                if content == "":
                    content = chat_msg.get("choices")[0].get("delta", {}).get("content", "")
                return content
