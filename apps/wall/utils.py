from constants import WRITINGS_PER_PAGE

def get_page_quantity(writings_quantity):
    page_quantity = writings_quantity / WRITINGS_PER_PAGE
    if writings_quantity % WRITINGS_PER_PAGE:
        page_quantity += 1
    return page_quantity
