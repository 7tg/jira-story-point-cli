import argparse
import datetime

from jira_service import JiraService
from conf import Conf

CONF = Conf.get_conf()

def _calc_story_points(issues):
    total_points = 0.0
    for issue in issues:
        total_points += issue['fields'][CONF['story-point-key']]
    return total_points

def main():
    parser = argparse.ArgumentParser(description='Get data from jira '
                                                 'calculate story points')
    parser.add_argument('--week', action='store_true',
                        help='calculate this week\'s points')
    parser.add_argument('--month', action='store_true',
                        help='calculate this month\'s points')
    args = parser.parse_args()

    today = datetime.date.today()
    start_date = None
    end_date = None

    if args.week:
        start_date = (today - datetime.timedelta(days=today.weekday())).isoformat()

    if args.month:
        start_date = today.replace(day=1).isoformat()

    jira_service = JiraService()
    issues = jira_service.get_issues(
        start_date=start_date,
        end_date=None
    )

    story_points = _calc_story_points(issues)
    print(story_points)

if __name__ == '__main__':
    main()

