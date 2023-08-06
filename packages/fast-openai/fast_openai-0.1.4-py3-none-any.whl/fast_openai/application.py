from functools import wraps
import itertools
from typing import Any, Callable, Coroutine, Dict, List, Optional, ParamSpecKwargs, Tuple, Type, Union
from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from typing_extensions import ParamSpec
from fastapi.templating import Jinja2Templates
from .client import APIClient
from .json import to_json
from .llm import LLMStack
from .odm import FaunaModel

class FastOpenAI(FastAPI):
    """OpenAI Backend for FastAPI"""
    def __init__(self, *args, **kwargs):
        super().__init__(title="FastOpenAI", description="OpenAI Backend for FastAPI", debug=True, *args, **kwargs)
        self.llm = LLMStack()
        
        @self.on_event("startup")
        async def startup():
            await FaunaModel.create_all()
            
        @self.on_event("shutdown")
        async def shutdown():
            await APIClient.cleanup()
    
    def ws(self, path:str):
        def decorator(func:Callable[[Any], Any]) -> Callable[[Any], Coroutine[Any, Any, None]]:
            @wraps(func)
            async def wrapper(websocket:WebSocket,**kwargs:ParamSpecKwargs):
                await websocket.accept()
                await func(websocket,**kwargs)
            self.add_api_websocket_route(path, wrapper)
            return wrapper
        return decorator

    def sse(self, path:str, **kwargs:Any):
        def decorator(func:Callable[[Any], Any]) -> Callable[[Any, Callable[[Any], Any]], Coroutine[Any, Any, StreamingResponse]]:
            @wraps(func)
            async def wrapper(*args,**kwargs) -> StreamingResponse:
                async def generator():
                    async for item in func(*args,**kwargs):
                        yield to_json(item) + "\n\n"
                return StreamingResponse(content=generator(), status_code=200, headers={"Content-Type": "text/event-stream", "Cache-Control": "no-cache", "Connection": "keep-alive", "Transfer-Encoding": "chunked"})
            self.add_api_route(path, wrapper,response_class=StreamingResponse, **kwargs)
            return wrapper
        return decorator