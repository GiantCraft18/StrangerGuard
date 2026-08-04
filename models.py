from dataclasses import dataclass, field
from typing import Optional, Set
from enum import Enum


class ActionType(Enum):
    BLOCK = "block"
    BAN = "ban"
    NONE = "none"


@dataclass
class CheckResult:
    is_stranger: bool
    user_id: int
    reason: str = ""
    in_contacts: bool = False
    in_dialogs: bool = False
    in_whitelist: bool = False


@dataclass
class ActionResult:
    success: bool
    action: ActionType
    user_id: int
    message: str = ""
    error: Optional[Exception] = None


@dataclass
class Config:
    auto_block: bool = False
    auto_ban: bool = False
    respect_whitelist: bool = True
    cache_ttl: int = 90
    only_private: bool = True
    log_actions: bool = True