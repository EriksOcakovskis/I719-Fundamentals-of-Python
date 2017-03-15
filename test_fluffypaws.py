import unittest
import fluffypaws
import fluffyreq
from unittest.mock import Mock, patch

MOCK_HOST_IP_RESPONSE_BODY = '192.168.1.10'
MOCK_HOST_IP_RESPONSE_STATUS = 200
MOCK_UNREACHABLE_IP = '1.1.1.1'


class FluffyReqTestCase(unittest.TestCase):
    def test_request_host_ip_response(self):
        mock_response = Mock(text=MOCK_HOST_IP_RESPONSE_BODY,
                             status_code=MOCK_HOST_IP_RESPONSE_STATUS)

        mock_request = Mock()
        mock_request.get = Mock(return_value=mock_response)

        with patch('fluffyreq.requests', mock_request):
            resp_dict = fluffyreq.get_host_ip('127.0.0.1')

        self.assertEqual(resp_dict['ip'], '192.168.1.10')
        self.assertEqual(resp_dict['status code'], 200)


    def test_host_ip_throws_exception_when_offlne(self):
        self.assertRaises(Exception,
                          fluffyreq.get_host_ip,
                          MOCK_UNREACHABLE_IP)
