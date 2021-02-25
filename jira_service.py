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

    def _run_jql(self, host, jql, page=1):
        params = {
            "jql": jql
        }

        if page:
            params['startAt'] = (page - 1) * 100

        res = requests.get(
            f"{host}/rest/api/2/search",
            params={
                "jql": jql
            },
            headers=self.headers
        )

        try:
            res.raise_for_status()
        except:
            return []

        res_json = res.json()

        if res_json['total'] > 100 and res_json['startAt'] < res_json['total']:
            if page:
                return res_json['issues'] + self._run_jql(host, jql, page + 1)
            else:
                return res_json['issues'] + self._run_jql(host, jql, 1)

        return res_json['issues']

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
