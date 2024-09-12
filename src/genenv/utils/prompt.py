from __future__ import annotations
import importlib
import logging
import os
from typing import Iterable

tkinter = importlib.util.find_spec("tkinter")
if tkinter:
    try:
        import tkinter
        from tkinter import filedialog
    except ModuleNotFoundError:
        tkinter = None

log = logging.getLogger(__name__)


# User input echo logging level
echo_log = log.debug


class InvalidInputException(BaseException):
    pass


class InputAbortionException(BaseException):
    pass


def ask_file(
    title: str | None = None,
    filters: Iterable[tuple[str, str | list[str] | tuple[str]]] | None = (),
) -> str:
    """
    Asks for a file by opening a file selection dialog, if tkinter is available,
    or by asking for a path in the console.
    """
    if tkinter:
        log.info("Choose file...")
        root = tkinter.Tk()
        root.wm_withdraw()  # hide tkinter root window
        out = filedialog.askopenfilename(title=title, filetypes=filters)
        echo_log(out)
        root.destroy()
    else:
        log.info("Enter path to file...")
        out = input()
        echo_log(out)
        if not os.path.exists(out):
            log.warning(f"File {out} not found")
            raise InvalidInputException()
        elif not os.path.isfile(out):
            log.warning(f"{out} is not a file")
            raise InvalidInputException()
    if not out:
        raise InputAbortionException
    return out
