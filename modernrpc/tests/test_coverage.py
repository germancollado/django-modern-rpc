# coding: utf-8
import datetime

import pytest

from modernrpc.exceptions import RPCException
from modernrpc.handlers.base import RPCHandler
from modernrpc.modernrpc_settings import MODERNRPC_DEFAULT_ENTRYPOINT_NAME
from testsite.rpc_methods_stub.not_decorated import full_documented_method, func_a, func_b, func_c


class MyBadHandler(RPCHandler):
    pass


def test_not_called_functions():
    # These functions are used only to test registering, but they are never called.
    # We call them now, so coverage doesn't report error
    func_a()
    func_b()
    func_c()
    full_documented_method('john', datetime.datetime.now(), 'Male')


def test_bad_handler_definition(rf):

    request = rf.get('/rpc')

    h = MyBadHandler(request, MODERNRPC_DEFAULT_ENTRYPOINT_NAME)
    with pytest.raises(NotImplementedError):
        h.loads("")
    with pytest.raises(NotImplementedError):
        h.dumps({"x": "y"})
    with pytest.raises(NotImplementedError):
        MyBadHandler.valid_content_types()
    with pytest.raises(NotImplementedError):
        h.parse_request()
    with pytest.raises(NotImplementedError):
        h.result_success(42)
    with pytest.raises(NotImplementedError):
        h.result_error(RPCException(1, ''))
