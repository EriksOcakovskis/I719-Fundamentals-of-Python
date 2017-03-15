import unittest
import fluffypaws
import fluffyreq
import fluffylog
from unittest.mock import Mock, patch

MOCK_HOST_IP_RESPONSE_BODY = '192.168.1.10'
MOCK_HOST_IP_RESPONSE_STATUS = 200
MOCK_UNREACHABLE_IP = 'http://127.0.0.1:43842'


class FluffyReqTestCase(unittest.TestCase):
    def test_request_host_ip_response(self):
        mock_response = Mock(text=MOCK_HOST_IP_RESPONSE_BODY,
                             status_code=MOCK_HOST_IP_RESPONSE_STATUS)

        mock_request = Mock()
        mock_request.get = Mock(return_value=mock_response)

        with patch('fluffyreq.requests', mock_request):
            resp_dict = fluffyreq.get_host_ip(MOCK_UNREACHABLE_IP)

        self.assertEqual(resp_dict['ip'], '192.168.1.10')
        self.assertEqual(resp_dict['status code'], 200)


    def test_host_ip_throws_exception_when_offlne(self):
        self.assertRaises(Exception,
                          fluffyreq.get_host_ip,
                          MOCK_UNREACHABLE_IP)


    def test_post_json_returns_negative_one(self):
        resp = fluffyreq.post_json_to_server(MOCK_UNREACHABLE_IP, '')
        self.assertEqual(resp, -1)

class FluffyLogTestCase(unittest.TestCase):
    def test_log_is_correct_format(self):
        log = fluffylog.FluffyLog()
        log.debug('test')
        result = log.flush()
        self.assertRegex(result['data'][0],
                         r'^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d DEBUG .{4}$')
