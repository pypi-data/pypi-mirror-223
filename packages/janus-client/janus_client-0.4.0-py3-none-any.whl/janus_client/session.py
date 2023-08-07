import asyncio
from typing import Dict, TYPE_CHECKING
import logging

from .transport import JanusTransport, ResponseHandlerType

if TYPE_CHECKING:
    from .plugin_base import JanusPlugin


logger = logging.getLogger(__name__)


class JanusSession:
    """Janus session instance"""

    __id: int = None
    transport: JanusTransport
    created: bool = False

    def __init__(
        self,
        base_url: str = "",
        api_secret: str = None,
        token: str = None,
        transport: JanusTransport = None,
    ):
        self.plugin_handles: Dict[int, JanusPlugin] = dict()

        if transport:
            self.transport = transport
        else:
            self.transport = JanusTransport.create_transport(
                base_url=base_url,
                api_secret=api_secret,
                token=token,
            )

    def __str__(self):
        return f"Session ({self.__id}) {self}"

    async def __connect(self) -> None:
        if not self.transport.connected:
            await self.transport.connect()

        if not self.__id:
            self.__id = await self.transport.create_session(self)

        self.keepalive_task = asyncio.create_task(self.keepalive())
        self.created = True

    async def destroy(self) -> None:
        """Release resources

        | Should be called when you don't need the session anymore.
        | Plugins from this session should be destroyed before this.
        """

        await self.send(
            {"janus": "destroy"},
            response_handler=lambda res: res if res["janus"] == "success" else None,
        )
        self.keepalive_task.cancel()
        await self.transport.destroy_session(self.__id)
        self.__id = None
        self.created = False

    def __sanitize_message(self, message: dict) -> None:
        if "session_id" in message:
            logger.warn(
                f"Should not set session_id ({message['session_id']}). Overriding."
            )
            del message["session_id"]

    async def send(
        self,
        message: dict,
        handle_id: int = None,
        response_handler: ResponseHandlerType = lambda response: response,
    ) -> dict:
        self.__sanitize_message(message=message)

        if not self.created:
            await self.__connect()

        return await self.transport.send(
            message,
            session_id=self.__id,
            handle_id=handle_id,
            response_handler=response_handler,
        )

    async def keepalive(self) -> None:
        # Reference: https://janus.conf.meetecho.com/docs/rest.html
        # A Janus session is kept alive as long as there's no inactivity for 60 seconds
        while True:
            await asyncio.sleep(30)
            await self.send({"janus": "keepalive"})

    def handle_async_response(self, response: dict):
        if "sender" in response:
            # This is response for plugin handle
            if response["sender"] in self.plugin_handles:
                self.plugin_handles[response["sender"]].handle_async_response(response)
            else:
                logger.info(
                    f"Got response for plugin handle but handle not found. Handle ID: {response['sender']}"
                )
                logger.info(f"Unhandeled response: {response}")
        else:
            # This is response for self
            logger.info(f"Async event for session: {response}")

    async def attach_plugin(self, plugin: "JanusPlugin") -> int:
        """Create plugin handle for the given plugin type

        :param plugin: Plugin instance with janus_client.JanusPlugin as base class
        """

        response = await self.send({"janus": "attach", "plugin": plugin.name})

        # Extract plugin handle id
        handle_id = int(response["data"]["id"])

        # Register plugin
        self.plugin_handles[handle_id] = plugin

        return handle_id

    def detach_plugin(self, plugin_handle: "JanusPlugin"):
        del self.plugin_handles[plugin_handle.id]
