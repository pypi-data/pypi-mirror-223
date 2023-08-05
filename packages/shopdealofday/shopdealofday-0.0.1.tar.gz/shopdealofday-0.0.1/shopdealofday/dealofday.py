# deal_of_the_day.py

import random

def get_deal_of_the_day(all_products):
    """
    Randomly selects a "Deal of the Day" from the available products.

    Parameters:
        all_products (list): A list of strings representing the names of all available products.

    Returns:
        str: The name of the selected product as the "Deal of the Day."
    """
    if not isinstance(all_products, list) or not all(isinstance(product, str) for product in all_products):
        raise ValueError("all_products must be a list of strings representing the names of available products.")

    if not all_products:
        raise ValueError("all_products list must not be empty.")

    deal_of_the_day = random.choice(all_products)
    return deal_of_the_day
