from bills import bills
from utils.misc import get_json_from_url


def get_bill(bill_number):
    """
    Load a bill from local to a list

    :param bill_number: The bill we're interested in
    :return: The full text of the bill
    """

    return {'full_text': bills[bill_number]}


def get_amendments(bill_number):
    """
    Load a bill's amendments and compare them to the bill text.

    :param bill_number: The bill we're interested in
    :return: Relevant amendments
    """

    dict_content = get_json_from_url(url=f'https://bills-api.parliament.uk/api/v1/Bills/{bill_number}/stages')
    amends = []
    items = dict_content.get('items', [])
    print(f'Checking {len(items)} stages')
    for item in items:
        for sitting in item.get('stageSittings', []):
            stage_id = sitting.get('billStageId')
            print(f'Checking stage: {stage_id}')
            if stage_id:
                amends += get_stage_amendments(
                    bill_number=bill_number,
                    stage_id=stage_id
                )

    return amends


def get_stage_amendments(bill_number, stage_id):
    """
    Queries all information on amendments that occurred at a given stage

    :param bill_number: The bill we're interested in
    :param stage_id: The stage we are interested in
    :return: Relevant amendments
    """
    url = f'https://bills-api.parliament.uk/api/v1/Bills/{bill_number}/Stages/{stage_id}/Amendments/?Take=1000'
    dict_content = get_json_from_url(url)
    return [dict_content]


def split_amendments(all_amendments):
    """
    Work through the amendments and split them in to categories of decision

    :param all_amendments: List of all amendments
    :return: Amendments in categories
    """

    decisions = {}

    for amendment in all_amendments:
        for item in amendment.get('items', []):
            dec = item.get('decision')
            decision = decisions.get(dec, [])
            decision.append(item)
            decisions[dec] = decision

    return decisions


if __name__ == '__main__':

    print()
