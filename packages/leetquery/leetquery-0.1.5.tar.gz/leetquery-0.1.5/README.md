# Leetcode Query
A library for retriving Human Resource information from Leetcode.

## Install
``` shell
    pip install leetquery
```
## Usage
### Retriving User Submissions
``` python
from leetquery import get_submissions

submissions = get_submissions(username="syhaung", limits)
```
return value:
```
["question1", "question2", ...]
```