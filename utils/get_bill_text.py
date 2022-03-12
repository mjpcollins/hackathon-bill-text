from bills import bills


def get_bill(bill_number):
    """
    Load a bill from local to a list

    :param bill_number: The bill we're interested in
    :return: The full text of the bill
    """

    return {'full_text': bills[bill_number]}
