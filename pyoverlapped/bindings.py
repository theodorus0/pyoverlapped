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

import functools
from ctypes import POINTER, windll, WinError, GetLastError
from ctypes.wintypes import HANDLE, BOOL, LPCSTR, DWORD, LPVOID
from typing import Callable

from pyoverlapped.structures import SecurityAttributes

ERROR_IO_INCOMPLETE = 996
ERROR_IO_PENDING = 997

LPDWORD = POINTER(DWORD)
LPOVERLAPPED = LPVOID


# Many thanks to https://github.com/ffalcinelli/pydivert
def raise_on_error(f):
    """
    This decorator throws a WinError whenever GetLastError() returns an error.
    As as special case, ERROR_IO_PENDING is ignored.
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        retcode = GetLastError()
        if retcode and retcode != ERROR_IO_PENDING:
            err = WinError(code=retcode)
            windll.kernel32.SetLastError(0)
            raise err
        return result

    return wrapper


CreateEventA: Callable[[POINTER(SecurityAttributes), BOOL, BOOL, LPCSTR], HANDLE] = \
    raise_on_error(windll.kernel32.CreateEventA)
CreateEventA.argtypes = [POINTER(SecurityAttributes), BOOL, BOOL, LPCSTR]
CreateEventA.restype = HANDLE

CloseHandle: Callable[[HANDLE], BOOL] = raise_on_error(windll.kernel32.CloseHandle)
CloseHandle.argtypes = [HANDLE]
CloseHandle.restype = BOOL

GetOverlappedResult: Callable[[HANDLE, LPOVERLAPPED, LPDWORD, BOOL], BOOL] = windll.kernel32.GetOverlappedResult
GetOverlappedResult.argtypes = [HANDLE, LPOVERLAPPED, LPDWORD, BOOL]
GetOverlappedResult.restype = BOOL

WaitForSingleObject: Callable[[HANDLE, DWORD], DWORD] = raise_on_error(windll.kernel32.WaitForSingleObject)
WaitForSingleObject.argtypes = [HANDLE, DWORD]
WaitForSingleObject.restype = DWORD

SetEvent: Callable[[HANDLE], BOOL] = raise_on_error(windll.kernel32.SetEvent)
SetEvent.argtypes = [HANDLE]
SetEvent.restype = BOOL
INFINITE = 4294967295
