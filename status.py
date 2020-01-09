"""
ノードの状態を表すクラス
"""
__author__ = "Takahiro55555"
__version__ = "0.0.1"
__date__ = "2020-01-09"

from enum import IntEnum, auto

class Status(IntEnum):
    """
    ノードの状態を表すクラス
    """
    NONE = auto()
    OPEN = auto()
    CLOSED = auto()