import asyncio
import json
import uuid
from typing import TYPE_CHECKING, Dict, Any, Optional

import websockets
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from .session import JanusSession

import logging

logger = logging.getLogger(__name__)


class JanusMessage(BaseModel):
    transaction: str = Field(default_factory=lambda: uuid.uuid4().hex)
    apisecret: Optional[str] = None
    token: Optional[str] = None
    janus: str


"""
Architecture design to handle Janus transactions and events
Assumption 1: All transaction ids are unique, and they will always get
    at least one reply when there are no network errors
So to handle transactions, it will be tracked in JanusConnection only.
To handle events, it will be passed top down to all matching session id
    and plugin handle id.
Each node down the tree with JanusConnection as root, including JanusConnection itself,
shall have:
1. handle_async_response method

E.g.
class JanusSession
    def handle_async_response(self, response):
        pass
"""


class JanusConnection:
    """Janus connection instance, connected through websocket

    Manage Sessions and Transactions
    """

    connected: bool = False

    def __init__(self, uri: str, api_secret: str = None, token: str = None):
        """Create connection instance

        :param uri: Janus server address
        :param api_secret: (optional) API key for shared static secret authentication
        :param token: (optional) Token for shared token based authentication
        """

        self.ws: websockets.WebSocketClientProtocol
        self.uri = uri
        self.transactions: Dict[str, asyncio.Queue] = dict()
        self.sessions: Dict[int, JanusSession] = dict()
        self.api_secret = api_secret
        self.token = token

    async def connect(self, **kwargs: Any) -> None:
        """Connect to server

        All extra keyword arguments will be passed to websockets.connect
        """

        logger.info(f"Connecting to: {self.uri}")

        self.ws = await websockets.connect(
            self.uri, subprotocols=[websockets.Subprotocol("janus-protocol")], **kwargs
        )
        self.receive_message_task = asyncio.create_task(self.receive_message())
        self.receive_message_task.add_done_callback(self.receive_message_done_cb)

        self.connected = True
        logger.info("Connected")

    async def disconnect(self) -> None:
        """Disconnect from server"""

        logger.info("Disconnecting")
        self.receive_message_task.cancel()
        await self.ws.close()
        self.connected = False

    def receive_message_done_cb(self, task: asyncio.Task, context=None) -> None:
        try:
            # Check if any exceptions are raised
            task.exception()
            # traceback.print_tb(exception.__traceback__)
            # logger.info(f"{type(exception)} : {exception}")
        except asyncio.CancelledError:
            logger.info("Receive message task ended")
        except asyncio.InvalidStateError:
            logger.info("receive_message_done_cb called with invalid state")
        # except Exception as e:
        #     traceback.logger.info_tb(e.__traceback__)

    async def receive_message(self) -> None:
        if not self.ws:
            raise Exception("Not connected to server.")

        async for message_raw in self.ws:
            response = json.loads(message_raw)
            logger.info(f"Received: {response}")

            if "transaction" in response:
                transaction_id = response["transaction"]
                await self.transactions[transaction_id].put(response)
            else:
                self.handle_async_response(response)

    async def send(self, message: JanusMessage) -> dict:
        """Send message to server

        :param message: JSON serializable dictionary to send

        :returns: Synchronous response from Janus server

        """
        # # Create transaction
        # transaction_id = uuid.uuid4().hex
        # message["transaction"] = transaction_id

        # Transaction ID must be in the dict to receive response
        self.transactions[message.transaction] = asyncio.Queue()

        # Authentication
        if self.api_secret is not None:
            message.apisecret = self.api_secret
        if self.token is not None:
            message.token = self.token

        # Send the message
        message_json = message.model_dump_json(exclude_none=True)
        logger.info(f"Send: {message_json}")
        await self.ws.send(message_json)

        # Wait for response
        # Assumption: there will be one and only one synchronous reply for a transaction.
        #   Other replies with the same transaction ID are asynchronous.
        response = await self.transactions[message.transaction].get()
        logger.info(f"Transaction response: {response}")

        # Transaction complete, delete it
        del self.transactions[message.transaction]
        return response

    def handle_async_response(self, response: dict) -> None:
        if "session_id" in response:
            # This is response for session or plugin handle
            if response["session_id"] in self.sessions:
                self.sessions[response["session_id"]].handle_async_response(response)
            else:
                logger.warning(
                    f"Got response for session but session not found. Session ID: {response['session_id']}"
                    f"Unhandeled response: {response}"
                )
        else:
            # This is response for self
            logger.info(f"Async event for Janus client core: {response}")

    async def create_session(self, session: "JanusSession") -> int:
        """Create Janus Session"""

        response = await self.send(JanusMessage(janus="create"))

        # Extract session ID
        session_id = int(response["data"]["id"])

        # Register session
        self.sessions[session_id] = session

        return session_id

    # Don't call this from client object, call destroy from session instead
    def destroy_session(self, session: "JanusSession") -> None:
        del self.sessions[session.id]


"""
# Take note to enable admin API with websockets in Janus, for example:
# admin: {
#         admin_ws = true                         # Whether to enable the Admin API WebSockets API
#         admin_ws_port = 7188                    # Admin API WebSockets server port, if enabled
#         #admin_ws_interface = "eth0"            # Whether we should bind this server to a specific interface only
#         #admin_ws_ip = "192.168.0.1"            # Whether we should bind this server to a specific IP address only
#         admin_wss = true                        # Whether to enable the Admin API secure WebSockets
#         admin_wss_port = 7989                   # Admin API WebSockets server secure port, if enabled
#         #admin_wss_interface = "eth0"           # Whether we should bind this server to a specific interface only
#         #admin_wss_ip = "192.168.0.1"           # Whether we should bind this server to a specific IP address only
#         #admin_ws_acl = "127.,192.168.0."       # Only allow requests coming from this comma separated list of addresses
# }
"""


class JanusAdminMonitorClient:
    def __init__(self, uri: str, admin_secret: str):
        self.ws: websockets.WebSocketClientProtocol
        self.uri = uri
        self.admin_secret = admin_secret
        self.transactions: Dict[str, asyncio.Queue] = dict()

    async def connect(self, **kwargs: Any) -> None:
        logger.info(f"Connecting to: {self.uri}")
        # self.ws = await websockets.connect(self.uri, ssl=ssl_context)
        self.ws = await websockets.connect(
            self.uri,
            subprotocols=[websockets.Subprotocol("janus-admin-protocol")],
            **kwargs,
        )
        self.receive_message_task = asyncio.create_task(self.receive_message())
        logger.info("Connected")

    async def disconnect(self):
        logger.info("Disconnecting")
        self.receive_message_task.cancel()
        await self.ws.close()

    async def receive_message(self):
        assert self.ws
        async for message_raw in self.ws:
            response = json.loads(message_raw)
            # WARNING: receive_message task will break with logger.infoing exception
            #   when entering here without a transaction in response.
            #   It happens when the asynchronous event is not recognized in
            #   self.is_async_response()
            # TODO: Find out how to logger.info exceptions in created tasks
            if response["transaction"] in self.transactions:
                await self.transactions[response["transaction"]].put(response)

    async def send(self, message: dict, authenticate: bool = True) -> dict:
        # Create transaction
        transaction_id = uuid.uuid4().hex
        message["transaction"] = transaction_id
        # Transaction ID must be in the dict to receive response
        self.transactions[transaction_id] = asyncio.Queue()

        # Authentication
        if authenticate:
            message["admin_secret"] = self.admin_secret

        # Send the message
        logger.info(json.dumps(message))
        await self.ws.send(json.dumps(message))

        # Wait for response
        # Assumption: there will be one and only one synchronous reply for a transaction.
        #   Other replies with the same transaction ID are asynchronous.
        response = await self.transactions[transaction_id].get()
        logger.info(f"Transaction reply: {response}")

        # Transaction complete, delete it
        del self.transactions[transaction_id]
        return response

    async def info(self):
        # Doesn't require admin secret
        message = {"janus": "info"}
        return await self.send(message, authenticate=False)

    async def ping(self):
        # Doesn't require admin secret
        message = {"janus": "ping"}
        return await self.send(message, authenticate=False)

    async def add_token(self, token: str = uuid.uuid4().hex, plugins: list = []):
        payload: dict = {"janus": "add_token", "token": token}
        if plugins:
            payload["plugins"] = plugins
        return await self.send(payload)

    async def allow_token(self, token: str, plugins: list):
        # if not plugins:
        #     raise Exception("plugins should be non-empty array")
        payload = {
            "janus": "allow_token",
            "token": token,
            "plugins": plugins,
        }
        return await self.send(payload)

    async def disallow_token(self, token: str, plugins: list):
        # if not plugins:
        #     raise Exception("plugins should be non-empty array")
        payload = {
            "janus": "disallow_token",
            "token": token,
            "plugins": plugins,
        }
        return await self.send(payload)

    async def list_tokens(self):
        payload = {"janus": "list_tokens"}
        result = await self.send(payload)
        return result["data"]["tokens"]

    async def remove_token(self, token: str):
        payload = {
            "janus": "remove_token",
            "token": token,
        }
        return await self.send(payload)
