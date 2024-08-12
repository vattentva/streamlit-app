from enum import Enum

class LangchainConfig(Enum):
    SYSTEM_MESSAGE = 'You are a helpful assistant.'

class RequestType(Enum):
    CHAT = 2
    SUMMARY = 3
