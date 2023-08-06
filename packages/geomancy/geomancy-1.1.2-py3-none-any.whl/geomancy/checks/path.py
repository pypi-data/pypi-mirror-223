"""
Check the existence and, optionally, the type of path.
"""
import typing as t
from pathlib import Path

from .base import Check, Result, CheckException, Executor
from ..config import Parameter

__all__ = ("CheckPath",)


class CheckPath(Check):
    """Check paths for valid files and directories"""

    #: (Optional) the type of path expected
    type: t.Optional[str] = None

    #: The valid values of path types
    type_options = (None, "dir", "file")

    msg = Parameter("CHECK_PATH.MSG", default="Check path '{check.value}'")

    aliases = ("checkPath",)

    def __init__(self, *args, type: t.Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        if type not in self.type_options:
            raise CheckException(
                f"Path type '{type}' must be one of: "
                f"{tuple(opt for opt in self.type_options if opt is not None)}"
            )
        self.type = type

    def check(self, executor: t.Optional[Executor] = None, level: int = 0) -> Result:
        """Check paths"""
        value = self.value
        path = Path(value)

        if not path.exists():
            status = "failed (missing)"
        elif self.type == "dir" and not path.is_dir():
            status = "failed (not dir)"
        elif self.type == "file" and not path.is_file():
            status = "failed (not file)"
        else:
            status = "passed"

        msg = self.msg.format(check=self, status=status)
        return Result(msg=msg, status=status)
