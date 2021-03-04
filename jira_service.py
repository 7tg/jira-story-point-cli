from math import ceil

import requests
from conf import Conf


class JiraService:

    def __init__(self, *args, **kwargs):
        self.conf = Conf.get_conf()
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f"Basic {self.conf['api-token']}",
        }



    def _run_jql(self, host, jql):
        params = {
            "jql": jql
        }

        issues = []

        res = requests.get(
            f"{host}/rest/api/2/search",
            params={
                "jql": jql,
                "maxResults": 50,
                "startAt": 0,
            },
            headers=self.headers
        )

        res.raise_for_status()
        res_json = res.json()

        issues += res_json['issues']
        page_count = ceil(res_json['total'] / 50)

        for page in range(1, page_count):
            params = {
                "jql": jql,
                "maxResults": 50,
                "startAt": page * 50
            }
            res = requests.get(
                f"{host}/rest/api/2/search",
                params=params,
                headers=self.headers
            )
            res.raise_for_status()
            res_json = res.json()
            issues += res_json['issues']

        return issues

    def get_issues(self, start_date=None, end_date=None):
        jql = self.conf['issue-jql']
        if start_date:
            jql = jql + f" AND resolved >= {start_date}"
        if end_date:
            jql = jql + f" AND resolved <= {end_date}"

        return self._run_jql(self.conf['host'], jql)


if __name__ == '__main__':
    service = JiraService()
    print(service.get_issues())
