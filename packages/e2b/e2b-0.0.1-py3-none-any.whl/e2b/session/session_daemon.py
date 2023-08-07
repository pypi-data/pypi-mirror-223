import asyncio
import json
import logging
from aenum import NamedTuple

from websockets.client import WebSocketClientProtocol, connect
from typing import (
    Callable,
    Optional,
    Any,
    Dict,
    Awaitable,
    List,
    Union,
    Iterable,
    Iterator,
)
from pydantic import BaseModel, PrivateAttr
from jsonrpcclient import request_json, Ok
from jsonrpcclient.id_generators import decimal as decimal_id_generator
from jsonrpcclient.responses import Response, Error, Deserialized
from jsonrpcclient.utils import compose
from websockets.typing import Data

from e2b.utils.future import DeferredFuture

logger = logging.getLogger(__name__)


class Notification(NamedTuple):
    """Nofification"""

    params: Any
    method: str

    def __repr__(self) -> str:
        return f"Notification(params={self.params!r}, method={self.method!r})"


Message = Response | Notification


def to_response_or_notification(response: Dict[str, Any]) -> Message:
    """Create a Response namedtuple from a dict"""
    if "error" in response:
        return Error(
            response["error"]["code"],
            response["error"]["message"],
            response["error"].get("data"),
            response["id"],
        )
    elif "result" in response and "id" in response:
        return Ok(response["result"], response["id"])

    elif "params" in response:
        return Notification(params=response["params"], method=response["method"])

    raise ValueError("Invalid response", response)


def parse(deserialized: Deserialized) -> Union[Message, Iterable[Message]]:
    """Create a Response or list of Responses from a dict or list of dicts"""
    if isinstance(deserialized, str):
        raise TypeError("Use parse_json on strings")
    return (
        map(to_response_or_notification, deserialized)
        if isinstance(deserialized, list)
        else to_response_or_notification(deserialized)
    )


class SessionDaemon(BaseModel):
    url: str
    on_close: Callable[[], Awaitable[None]]
    on_message: Callable[[Notification], None]

    _id_generator: Iterator[int] = PrivateAttr(default_factory=decimal_id_generator)
    _waiting_for_replies: Dict[int, DeferredFuture] = PrivateAttr(default_factory=dict)
    _ws: Optional[WebSocketClientProtocol] = PrivateAttr()

    class Config:
        arbitrary_types_allowed = True

    async def connect(self):
        self._ws = await connect(self.url)

        async def handle_messages():
            if not self._ws:
                raise Exception("Not connected")
            async for message in self._ws:
                await self._receive_message(message)
            await self.on_close()

        asyncio.create_task(handle_messages())

    async def send_message(self, method: str, params: List[Any]) -> Any:
        if not self._ws:
            raise Exception("Not connected")

        id = next(self._id_generator)
        request = request_json(method, params, id)
        future_reply = DeferredFuture()

        try:
            self._waiting_for_replies[id] = future_reply
            logger.info(f"Sending request: {request}")
            await self._ws.send(request)
            r = await future_reply
            logger.info(f"Received reply: {r}")
            return r
        except Exception as e:
            logger.info(f"Error: {request} {e}")
            raise e
        finally:
            del self._waiting_for_replies[id]
            logger.info(f"Removed waiting handler for {id}")

    async def _receive_message(self, data: Data):
        message = to_response_or_notification(json.loads(data))

        logger.info(f"Received message: {message}")

        logger.info(f"Current waiting handlers: {self._waiting_for_replies}")
        if isinstance(message, Ok):
            if (
                message.id in self._waiting_for_replies
                and self._waiting_for_replies[message.id]
            ):
                self._waiting_for_replies[message.id](message.result)
                return
        elif isinstance(message, Error):
            if (
                message.id in self._waiting_for_replies
                and self._waiting_for_replies[message.id]
            ):
                self._waiting_for_replies[message.id].reject(Exception(message))
                return

        elif isinstance(message, Notification):
            self.on_message(message)

    async def close(self):
        if self._ws:
            await self._ws.close()
        if self.on_close:
            await self.on_close()
        for h in self._waiting_for_replies.values():
            h.cancel()
            del h
