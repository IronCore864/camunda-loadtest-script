import requests
import configparser
import time


class LoadTest(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.camunda_url = "{host}/engine-rest/process-definition/{process_id}/start".format(
            host=config['DEFAULT']['CamundaHost'],
            process_id=config['DEFAULT']['ProcessID']
        )
        self.total_requests_num = config['DEFAULT'].getint('TotalRequestsToSend')
        self.payload = {
            # if the vars used by the process should be returned
            # default False
            # set to True if you are doing synchronized process start calls
            # 'withVariablesInReturn': True,
            'variables': {
                # some variables passed to the process
                'firstname': {'value': 'Peter', 'typeinfo': ''},
                'surname': {'value': 'Jackson', 'typeinfo': ''},
                'home_house': {'value': '1', 'typeinfo': ''},
                'home_postcode': {'value': 'SE10 9EL', 'typeinfo': ''},
                'mobile': {'value': '9999999999', 'typeinfo': ''},
                'gender': {'value': 'Male', 'typeinfo': ''}
            }
        }
        self.headers = {'Content-type': 'application/json'}
        self.start = None
        self.end = None

    def stats(self, results):
        none_count = 0
        ok_count = 0
        server_err_count = 0

        for res in results:
            if not res:
                none_count += 1
            elif res.status_code == 200:
                ok_count += 1
            elif res.status_code == 500:
                server_err_count += 1
        print('Time used: {}'.format(self.end - self.start))
        print("Total requests: {} OK: {} HTTP 500: {} NULL: {}".format(self.total_requests_num,
                                                                       ok_count,
                                                                       server_err_count,
                                                                       none_count))

    def start_process(self):

        if self.total_requests_num == -1:
            while 1:
                requests.post(
                    self.camunda_url,
                    json=self.payload,
                    headers=self.headers
                )
        else:
            results = []
            self.start = time.time()
            for i in range(self.total_requests_num):
                results.append(
                    requests.post(
                        self.camunda_url,
                        json=self.payload,
                        headers=self.headers
                    )
                )
            self.end = time.time()
            self.stats(results)


load = LoadTest()
load.start_process()
