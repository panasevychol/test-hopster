import pprint

from googleapiclient.discovery import build

# from libs import jwt

from constants import WRITINGS_PER_PAGE


def get_page_quantity(writings_quantity):
    page_quantity = writings_quantity / WRITINGS_PER_PAGE
    if writings_quantity % WRITINGS_PER_PAGE:
        page_quantity += 1
    return page_quantity

def request_api(api_name, root_path, method_name, body=None):
    # Build a service object for interacting with the API.
    if not body:
        body = {}
    api_root = '%s/_ah/api' % root_path
    version = 'v1'
    discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (api_root,
                                                         api_name, version)
    service = build(api_name, version, discoveryServiceUrl=discovery_url)

    if api_name == 'wall':
        if method_name == 'list':
            response = service.writings().list(body=body).execute()
        elif method_name == 'create':
            response = service.writings().create(body=body).execute()
        elif method_name == 'delete':
            response = service.writings().delete(body=body).execute()
        else:
            raise RuntimeError('Request method not found')
    else: #elif api_name == 'users':
        # if method_name == 'login':
        response = service.users().login(body=body).execute()
    return response

    # Fetch a single greeting and print it out.
    # response = service.greetings().get(id='9001').execute()
    # pprint.pprint(response)
