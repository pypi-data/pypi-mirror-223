# dealfortheday/mydealfortheday.py

import random
import datetime

def getDealForTheDay(allProducts, request):
    """
    Randomly selects a "Deal of the Day" from the available products.

    Parameters:
        allProducts (list): A list of strings representing the names of all available products.
        request: The Django request object.

    Returns:
        str: The name of the selected product as the "Deal of the Day."
    """
    if not isinstance(allProducts, list) or not all(isinstance(product, str) for product in allProducts):
        raise ValueError("allProducts must be a list of strings representing the names of available products.")

    if not allProducts:
        raise ValueError("allProducts list must not be empty.")

    deal_of_the_day_key = 'deal_of_the_day'
    current_date = datetime.date.today()

    if deal_of_the_day_key not in request.session or request.session.get('deal_date') != current_date:
        deal_of_the_day = random.choice(allProducts)
        request.session[deal_of_the_day_key] = deal_of_the_day
        request.session['deal_date'] = current_date
    else:
        deal_of_the_day = request.session[deal_of_the_day_key]

    return deal_of_the_day
