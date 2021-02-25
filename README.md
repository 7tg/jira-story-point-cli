# Introduction
This project is focused mainly on calculating story points in jira with 
given time periods (optional).
# Getting started
## Setting up the conf
Based on `example-settings.yaml` you need to create a file called `settings.
yaml` in the project folder

## Running the script
### Monthly
```shell
python jira_story_point_calculator.py --month
```
### Weekly
```shell
python jira_story_point_calculator.py --week
```
### All time
```shell
python jira_story_point_calculator.py
```
