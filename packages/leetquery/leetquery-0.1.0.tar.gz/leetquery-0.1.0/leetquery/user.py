# Copyright (c) 2023 Shu-Yu Huang
#
# Licensed under the MIT License
import requests
import json
from typing import List

__all__  = ["get_submissions"]

def get_submissions(username: str="syhaung", limit: int= 12) -> List[str]:
    url = "https://leetcode.com/graphql?"
    headers = {'Content-Type': 'application/json'}
    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
        recentAcSubmissionList(username: $username, limit: $limit) {
            id
            title
            titleSlug
            timestamp
        }
    }
    """
    variables = {'username': username, 'limit': 50}
    payload = {
            'query': query,
            'operationName': 'recentAcSubmissions',
            'variables': variables
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload)).json()
    return [x["title"] for x in response["data"]["recentAcSubmissionList"]]
