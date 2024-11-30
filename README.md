# pyoverlapped
Async wrapper for Windows Overlapped API

Allows you to wrap ctypes functions that use Windows Overlapped IO
into Python coroutines.

Requires no external dependencies. Minimal Python version is 3.8

## Installation
```shell
pip install pyoverlapped
```

## Usage
For example, we have ctypes-binded function `WinDivertRecvEx` that supports Overlapepd IO.

To wrap it into coroutine with pyoverlapped, we need 3 things:
1. Handle to object on which we perform overlapped  operation
2. Pointer to a variable that will hold number of transferred bytes
3. Function that accepts Overlapped structure as the only argument. 
Basically, it wraps our target function `WinDivertRecvEx`

With these we can finally await on our function:
```python
from pyoverlapped import perform_overlapped_operation


recv_len = c_uint(0)
f = lambda lpovl: WinDivertRecvEx(..., lpovl)
await perform_overlapped_operation(handle, byref(recv_len), f)
```


## Thanks
Thanks to [ffalcinelli](https://github.com/ffalcinelli) for error-handling decorator for ctypes-bound functions