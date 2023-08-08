from leetquery.user import get_submissions

def test_init():
    sub_list = get_submissions(
        username="syhaung",
        limit=12
    )

    assert len(sub_list)>0