from googleapiclient.discovery import build

from constants import WRITINGS_PER_PAGE


def get_page_quantity(writings_quantity):
    page_quantity = writings_quantity / WRITINGS_PER_PAGE
    if writings_quantity % WRITINGS_PER_PAGE:
        page_quantity += 1
    return page_quantity

def request_api(api_name, method_name, root_path, body=None):
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
            raise RuntimeError('Method %s at %s API not found') % (method_name,
                                                                   api_name)
    elif api_name == 'users':
        if method_name == 'login':
            response = service.users().login(body=body).execute()
        else:
            raise RuntimeError('Method %s at %s API not found') % (method_name,
                                                                   api_name)
    else:
        raise RuntimeError('%s API not found') % api_name

    return response
