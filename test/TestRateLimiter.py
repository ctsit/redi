import unittest
import datetime

from redi.utils import redcapClient


class TestRateLimiter(unittest.TestCase):

    def test_throttle(self):

        class MockRedcapClient(object):
            def get_data_from_redcap(self, records_to_fetch=None,
                                     events_to_fetch=None,
                                     fields_to_fetch=None,
                                     forms_to_fetch=None,
                                     return_format='xml'):
                return 'Time to make the data'

            def send_data_to_redcap(self, data, overwrite=False):
                return 'Time to send the data'

        client = redcapClient.ThrottledRedcapClient(MockRedcapClient(),
                                                    max_requests_per_minute=3,
                                                    api_calls_already_made=0)

        MINUTE = datetime.timedelta(seconds=3)
        SECONDS = MINUTE.total_seconds()

        client._ThrottledRedcapClient__minute = MINUTE


        started = datetime.datetime.now()
        client.get_data_from_redcap()
        client.get_data_from_redcap()
        client.get_data_from_redcap()
        self.assertTrue(lapsed_time_in_secs(since=started) < SECONDS)
        self.assertEqual(3, len(client.requests))

        client.get_data_from_redcap()
        restarted = datetime.datetime.now()
        self.assertTrue(lapsed_time_in_secs(since=started) > SECONDS)
        self.assertEqual(1, len(client.requests))

        client.get_data_from_redcap()
        self.assertTrue(lapsed_time_in_secs(since=restarted) < SECONDS)
        self.assertEqual(2, len(client.requests))


def lapsed_time_in_secs(since):
    return (datetime.datetime.now() - since).total_seconds()


if __name__ == '__main__':
    unittest.main()
