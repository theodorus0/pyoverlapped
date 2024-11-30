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
from ctypes import c_void_p, c_ulonglong, c_ulong, Structure, sizeof
from ctypes.wintypes import DWORD, LPVOID, HANDLE, BOOL

if sizeof(c_void_p) == 8:
    ULONG_PTR = c_ulonglong
else:
    ULONG_PTR = c_ulong


class Overlapped(Structure):
    _fields_ = [
        ("Internal", ULONG_PTR),
        ("InternalHigh", ULONG_PTR),
        ("Offset", DWORD),
        ("OffsetHigh", DWORD),
        ("Pointer", LPVOID),
        ("HEvent", HANDLE),
    ]


class SecurityAttributes(Structure):
    _fields_ = [
        ("nLength", DWORD),
        ("lpSecurityDescriptor", LPVOID),
        ("bInheritHandle", BOOL)
    ]
