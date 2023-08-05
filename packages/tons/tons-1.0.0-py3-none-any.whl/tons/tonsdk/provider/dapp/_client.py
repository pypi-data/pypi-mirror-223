import asyncio
import ssl
import time
from typing import Any, List, AsyncGenerator, Optional

import aiohttp
import certifi
from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError
from gql.transport.websockets import WebsocketsTransport
from graphql import DocumentNode
from pydantic import BaseModel

from tons.config import TonNetworkEnum


class ErrorMsg(BaseModel):
    message: Optional[str] = None
    code: Optional[int] = None


class DAppWrongResult(Exception):
    def __init__(self, errors):
        self.errors = errors

    def __str__(self):
        return ". ".join([f"{error.message}, Code: {error.code}" for
                          error in self.errors])


class BroadcastQuery(BaseModel):
    boc: str
    timeout: int


class Limiter:
    def __init__(self, calls: int = 10, period: float = 1):
        self.calls = calls
        self.period = period
        self.clock = time.monotonic
        self.last_reset = 0
        self.num_calls = 0

    async def __aenter__(self):
        if self.num_calls >= self.calls:
            await asyncio.sleep(self.__period_remaining())
        if self.__period_remaining() <= 0:
            self.num_calls = 0
            self.last_reset = self.clock()
        self.num_calls += 1
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def __period_remaining(self):
        return self.period - (self.clock() - self.last_reset)


class DAppClient:
    def __init__(self, graphql_url: str, broadcast_url: str, websocket_url: str, api_key: str, network: TonNetworkEnum):
        self.api_key = api_key
        self.broadcast_url = broadcast_url
        self.websocket_url = websocket_url
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.http_transport = AIOHTTPTransport(
            url=graphql_url, headers=self.__headers(is_json=False), ssl=self.ssl_context)
        self.limit_rps = Limiter(calls=1, period=0.2 if network == TonNetworkEnum.mainnet else 0.2)

    async def query(self, queries: List[DocumentNode], ignore_errors=False) -> List[Any]:
        results = []

        async with Client(
                transport=self.http_transport,
                fetch_schema_from_transport=False,
        ) as session:
            for query in queries:
                try:
                    async with self.limit_rps:
                        result = await session.execute(query)

                    results.append(result)
                except TransportQueryError as e:
                    self.__handle_errors(e.errors, ignore_errors)

        return results

    async def broadcast(self, queries: List[BroadcastQuery], timeout=31, ignore_errors=False) -> List[Any]:
        results = []
        timeout = aiohttp.ClientTimeout(total=timeout)

        async with aiohttp.ClientSession(timeout=timeout) as session:
            for query in queries:
                try:
                    async with self.limit_rps:
                        async with session.post(self.broadcast_url, json=query.dict(),
                                                headers=self.__headers(is_json=True), ssl=self.ssl_context
                                                ) as resp:
                            results.append(await self.__parse_broadcast_response(resp, ignore_errors))
                except TransportQueryError as e:
                    self.__handle_errors(e.errors, ignore_errors)

        return results

    async def subscription(self, query: DocumentNode, timeout=31) -> AsyncGenerator:
        websockets_transport = WebsocketsTransport(url=self.websocket_url, headers=self.__headers(is_json=False),
                                                   close_timeout=0, keep_alive_timeout=timeout)
        async with Client(transport=websockets_transport, fetch_schema_from_transport=True) as session:
            async for result in session.subscribe(query):
                yield result

    def __headers(self, is_json):
        headers = {}

        if is_json:
            headers = {
                'Content-Type': 'application/json',
            }

        if self.api_key:
            headers['API-KEY'] = self.api_key

        return headers

    async def __parse_broadcast_response(self, resp, ignore_errors):
        try:
            resp = await resp.json()
        except Exception:  # TODO: catch correct exceptions
            self.__handle_errors([{"message": resp.reason, "code": resp.status}], ignore_errors)
            return None

        if "errors" in resp and resp['errors']:
            if len(resp['errors']) == 1 and 'message' in resp['errors'][0] \
                    and resp['errors'][0]['message'] == 'timeout':
                # transaction may have been sent and may be committed later
                resp['data']['status'] = 0
                return resp['data']

            else:
                return self.__handle_errors(resp['errors'], ignore_errors)

        return resp['data']

    def __handle_errors(self, errors, ignore_errors):
        if not ignore_errors:
            errors = [ErrorMsg.parse_obj(error)
                      for error in errors]
            raise DAppWrongResult(errors)

        return
