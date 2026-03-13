import json
import re
import os
from typing import Any, Callable, Coroutine
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = "claude-sonnet-4-6"


class HumanInputRequired(Exception):
    def __init__(self, prompt: str):
        self.prompt = prompt
        super().__init__(prompt)


class BaseAgent:
    name: str = "BaseAgent"
    step_index: int = 0

    def __init__(
        self,
        ws_send: Callable[[str], Coroutine],
        context: dict,
    ):
        self.ws_send = ws_send
        self.context = context
        self._resume_reply: str | None = None
        self._client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

    async def send(self, message: dict):
        await self.ws_send(json.dumps(message))

    async def stream_to_client(self, text: str):
        await self.send({
            "type": "AGENT_CHUNK",
            "agent": self.name,
            "step_index": self.step_index,
            "text": text,
        })

    async def require_human_input(self, prompt: str) -> str:
        raise HumanInputRequired(prompt)

    def inject_reply(self, reply: str):
        self._resume_reply = reply

    async def call_claude_streaming(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 4096,
    ) -> str:
        full_text = ""
        async with self._client.messages.stream(
            model=MODEL,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        ) as stream:
            async for text in stream.text_stream:
                await self.stream_to_client(text)
                full_text += text
        return full_text

    @staticmethod
    def extract_json_block(text: str) -> dict | list | None:
        pattern = r"```json\s*([\s\S]*?)\s*```"
        match = re.search(pattern, text)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        # Try to find raw JSON object/array
        json_pattern = r"\{[\s\S]*\}|\[[\s\S]*\]"
        matches = re.findall(json_pattern, text)
        for m in reversed(matches):
            try:
                return json.loads(m)
            except json.JSONDecodeError:
                continue
        return None

    async def run(self) -> dict:
        raise NotImplementedError
