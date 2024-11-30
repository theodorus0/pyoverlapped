"""
This file is part of pyoverlapped.

pyoverlapped is free software: you can redistribute it and/or modify it under the terms of
the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

Foobar is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with pyoverlapped.
If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
from ctypes import windll, POINTER, GetLastError, c_ulong, byref, cast
from ctypes.wintypes import HANDLE, BOOL, LPWORD, LPCSTR
from typing import Callable, TypeVar

from pyoverlapped.bindings import GetOverlappedResult, LPOVERLAPPED, CreateEventA, CloseHandle, ERROR_IO_INCOMPLETE
from pyoverlapped.structures import Overlapped

T = TypeVar('T')


async def wait_for_overlapped_result(handle: HANDLE, p_overlapped: LPOVERLAPPED, p_bytes_sent: LPWORD):
    success = False
    while not success:
        success = GetOverlappedResult(handle,
                                      p_overlapped,
                                      p_bytes_sent,
                                      BOOL(False))
        if not success:
            err_code = GetLastError()
            if err_code == ERROR_IO_INCOMPLETE:
                windll.kernel32.SetLastError(0)
            else:
                raise OSError(err_code)
        else:
            # TODO:
            #  for some reason asyncronous sleep sets last error to 258
            #  if everything went good, so we have to exit the loop here
            continue
        # TODO: check
        await asyncio.sleep(0.001)


async def perform_overlapped_operation(handle: HANDLE, p_transferred_bytes: POINTER(c_ulong),
                                       func: Callable[[LPOVERLAPPED], T]) -> None:
    """
    Perform operation that supports Overlapped I/O
    :param handle: object handle
    :param p_transferred_bytes: pointer to var holding transferred bytes number
    :param func: function that accepts LPOVERLAPPED as the only parameter
    """
    event = CreateEventA(None, BOOL(False), BOOL(False), LPCSTR())
    ovl = Overlapped(HEvent=event)
    func(cast(byref(ovl), LPOVERLAPPED))

    await wait_for_overlapped_result(handle, cast(byref(ovl), LPOVERLAPPED), p_transferred_bytes)
    CloseHandle(event)

