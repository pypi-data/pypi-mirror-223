# -*- coding:utf-8 -*-

import gdpy
import mock
from gdpy.http import requests
from unittests.common import *
import tempfile
import platform
import json


def makeResponse200():
    status = 200
    headers = {},
    response = requests.Response
    response.text = '"{success}"'
    response.content = '{"items":{}}'
    return MockResponse_base(status, headers, response)


def makeResponse200_4_list():
    status = 200
    headers = {},
    response = requests.Response
    response.text = '{"items":{}}'
    response.content = '{"items":{}}'
    return MockResponse_base(status, headers, response)


def makeResponse200_4_getparam():
    status = 200
    headers = {},
    response = requests.Response
    response.text = '{"parameter":{}}'
    response.content = '{"parameter":{}}'
    return MockResponse_base(status, headers, response)


@mock.patch('gdpy.Session.do_request')
class TestTool(GDTestCase):
    # invalid tool version
    def test_get_tool_failed(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        with self.assertRaises(ValueError) as cm:
            result = tool().get_tool('TestTool', 'version')
        self.assertEquals(str(cm.exception), 'Invalid tool version! Expect interger greater than 0, but got version')

        with self.assertRaises(ValueError) as cm:
            result = tool().get_tool('TestTool', -1)
        self.assertEquals(str(cm.exception), 'Invalid tool version! Expect interger greater than 0, but got -1')

        # invalid tool name
        with self.assertRaises(ValueError) as cm:
            result = tool().get_tool(1, 1)
        self.assertEquals(str(cm.exception),
                          'Invalid tool name! Expect a string started with alphabet and under 128 characters, but got 1!')

        with self.assertRaises(ValueError) as cm:
            result = tool().get_tool(None, 1)

    # get tool without version
    def test_get_tool_success(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = tool().get_tool('TestTool')
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

        # get tool with version
        result = tool().get_tool('TestTool', 1)
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # test list tools
    def test_list_tool(self, do_request):
        req_info = mock_response(do_request, makeResponse200_4_list())
        result = tool().list_tools()
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '{"items":{}}')

    # test delete tool
    def test_delete_tool_success(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = tool().get_tool('TestTool', 1)
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    def test_delete_tool_failed(self, do_request):
        # lack version
        req_info = mock_response(do_request, makeResponse200())
        with self.assertRaises(TypeError) as cm:
            result = tool().delete_tool('TestTool')

        # invalid name
        with self.assertRaises(ValueError) as cm:
            result = tool().delete_tool(1, 1)

        with self.assertRaises(ValueError) as cm:
            result = tool().delete_tool(None, 1)

    # test get tool param
    def test_get_tool_param_success(self, do_request):
        req_info = mock_response(do_request, makeResponse200_4_getparam())
        # without version
        result = tool().get_tool_param('TestTool')
        self.assertEquals(result.status, 200)

        # with version
        result = tool().get_tool_param('TestTool', 1)
        self.assertEquals(result.status, 200)

    def test_get_tool_param_failed(self, do_request):
        req_info = mock_response(do_request, makeResponse200_4_getparam())
        # invalid name
        with self.assertRaises(ValueError) as cm:
            result = tool().get_tool_param(None, 1)
        self.assertEquals(str(cm.exception), 'Expect a name(str) started with alphabet and under 128 characters')

        with self.assertRaises(ValueError) as cm:
            result = tool().get_tool_param(1, 1)
        self.assertEquals(str(cm.exception),
                          'Invalid tool name! Expect a string started with alphabet and under 128 characters, but got 1!')

    # test create tool
    def test_create_tool(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = tool().create_tool('TestTool', 1)
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    # invalid name
    def test_create_tool_failed(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        with self.assertRaises(ValueError) as cm:
            result = tool().create_tool(1, 1)
        self.assertEquals(str(cm.exception),
                          'Invalid tool name! Expect a string started with alphabet and under 128 characters, but got 1!')

        with self.assertRaises(ValueError) as cm:
            result = tool().create_tool(None, 1)
        self.assertEquals(str(cm.exception),
                          'Invalid tool name! Expect a string started with alphabet and under 128 characters, but got None!')

        # invalid version
        with self.assertRaises(ValueError) as cm:
            result = tool().create_tool('TestTool', 'klasjflkj')
        self.assertEquals(str(cm.exception), 'Invalid tool version! Expect interger greater than 0, but got klasjflkj')

    # test put tool
    def test_put_tool(self, do_request):
        req_info = mock_response(do_request, makeResponse200())
        result = tool().put_tool('unittests/resources/hello.yml')
        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '"{success}"')

    def test_create_wdl_tool(self, do_request):
        def makeResponse():
            status = 200
            headers = {}
            response = requests.Response()
            result_data = {"app_id": "app_id"}
            python_version = platform.python_version_tuple()
            if python_version[0] == "2":
                response.text = json.dumps(result_data)
                response.content = json.dumps(result_data)
            else:
                response.text = json.dumps(result_data)
                response.content = bytes(json.dumps(result_data), encoding='utf-8')
            return MockResponse_base(status, headers, response)

        req_info = mock_response(do_request, makeResponse())
        tf = tempfile.NamedTemporaryFile()
        with open(tf.name, "w") as f:
            f.write("""
            task A {
                    command <<<>>>
                }
            """)
        result = wdl_tool().create_tool('test_tool', description='description', attachment={
            "source_file": tf.name})

        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '{"app_id": "app_id"}')
        self.assertEquals(do_request.call_args[0][0].data, {'name': 'test_tool', 'description': 'description'})

    def test_list_wdl_tool(self, do_request):
        def makeResponse():
            status = 200
            headers = {}
            response = requests.Response()
            result_data = {"count": 1, "tool_list": [{"id": "id"}]}
            python_version = platform.python_version_tuple()
            if python_version[0] == "2":
                response.text = json.dumps(result_data)
                response.content = json.dumps(result_data)
            else:
                response.text = json.dumps(result_data)
                response.content = bytes(json.dumps(result_data), encoding='utf-8')
            return MockResponse_base(status, headers, response)

        req_info = mock_response(do_request, makeResponse())
        result = wdl_tool().list_tools()

        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '{"count": 1, "tool_list": [{"id": "id"}]}')
        self.assertEquals(do_request.call_args[0][0].url,
                          "https://cn-beijing-api.genedock.com/accounts/res_account_name/projects/project_name/wdl/tools/")

    def test_get_wdl_tool(self, do_request):
        def makeResponse():
            status = 200
            headers = {}
            response = requests.Response()
            result_data = {"id": "id"}
            python_version = platform.python_version_tuple()
            if python_version[0] == "2":
                response.text = json.dumps(result_data)
                response.content = json.dumps(result_data)
            else:
                response.text = json.dumps(result_data)
                response.content = bytes(json.dumps(result_data), encoding='utf-8')
            return MockResponse_base(status, headers, response)

        req_info = mock_response(do_request, makeResponse())
        result = wdl_tool().get_tool("test_tool", 1)

        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '{"id": "id"}')
        self.assertEquals(do_request.call_args[0][0].url,
                          "https://cn-beijing-api.genedock.com/accounts/res_account_name"
                          "/projects/project_name/wdl/tools/test_tool/?tool_version=1")

    def test_update_wdl_tool(self, do_request):
        def makeResponse():
            status = 200
            headers = {}
            response = requests.Response()
            result_data = {"app_id": "app_id"}
            python_version = platform.python_version_tuple()
            if python_version[0] == "2":
                response.text = json.dumps(result_data)
                response.content = json.dumps(result_data)
            else:
                response.text = json.dumps(result_data)
                response.content = bytes(json.dumps(result_data), encoding='utf-8')
            return MockResponse_base(status, headers, response)

        req_info = mock_response(do_request, makeResponse())
        tf = tempfile.NamedTemporaryFile()
        with open(tf.name, "w") as f:
            f.write("""
            task A {
                    command <<<>>>
                }
            """)
        result = wdl_tool().update_tool('test_tool', 1, description='description', attachment={
            "source_file": tf.name})

        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '{"app_id": "app_id"}')
        self.assertEquals(do_request.call_args[0][0].data,
                          {'description': 'description', 'override': True, 'tool_version': 1})
        self.assertEquals(do_request.call_args[0][0].url,
                          "https://cn-beijing-api.genedock.com/accounts/res_account_name"
                          "/projects/project_name/wdl/tools/test_tool/?")

    def test_delete_wdl_tool(self, do_request):
        def makeResponse():
            status = 200
            headers = {}
            response = requests.Response()
            result_data = {}
            python_version = platform.python_version_tuple()
            if python_version[0] == "2":
                response.text = json.dumps(result_data)
                response.content = json.dumps(result_data)
            else:
                response.text = json.dumps(result_data)
                response.content = bytes(json.dumps(result_data), encoding='utf-8')
            return MockResponse_base(status, headers, response)

        req_info = mock_response(do_request, makeResponse())
        result = wdl_tool().delete_tool("test_tool", 1)

        self.assertEquals(result.status, 200)
        self.assertEquals(result.response.text, '{}')
        self.assertEquals(do_request.call_args[0][0].url,
                          "https://cn-beijing-api.genedock.com/accounts/res_account_name"
                          "/projects/project_name/wdl/tools/test_tool/?tool_version=1")

    def test_get_tool_info_by_name(self, do_request):
        def makeResponse():
            status = 200
            headers = {}
            response = requests.Response
            result_data = {"count": 1, "tool_list": [{"id": "id"}]}
            python_version = platform.python_version_tuple()
            if python_version[0] == "2":
                response.text = json.dumps(result_data)
                response.content = json.dumps(result_data)
            else:
                response.text = json.dumps(result_data)
                response.content = bytes(json.dumps(result_data), encoding='utf-8')
            return MockResponse_base(status, headers, response)

        req_info = mock_response(do_request, makeResponse())
        result = wdl_tool().get_tool_info_by_name("test_tool", 1)

        self.assertEquals(result, [{'id': 'id'}])
        self.assertEquals(do_request.call_args[0][0].url,
                          "https://cn-beijing-api.genedock.com/accounts/res_account_name/projects/project_name/wdl/tools/")


if __name__ == '__main__':
    unittest.main()
