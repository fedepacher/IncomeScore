import os
import googleapiclient.discovery
import google.auth
import google.auth.exceptions


def get_project_id():
    """Find the GCP project ID when running on Cloud Run."""
    try:
        _, project_id = google.auth.default()
    except google.auth.exceptions.DefaultCredentialsError:
        # Probably running a local development server.
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT', 'development')

    return project_id


def get_service_url():
    """Return the URL for this service, depending on the environment.

    For local development, this will be http://api:8000/. On Cloud Run
    this is https://{service}-{hash}-{region}.a.run.app.
    """
    # https://cloud.google.com/run/docs/reference/rest/v1/namespaces.services/list
    try:
        service = googleapiclient.discovery.build('run', 'v1')
    except google.auth.exceptions.DefaultCredentialsError:
        # Probably running the local development server.
        port = os.environ.get('PORT', '8000')
        url = f'http://api:{port}'
    else:
        # https://cloud.google.com/run/docs/reference/container-contract
        k_service = os.environ['K_SERVICE']
        project_id = get_project_id()
        parent = f'namespaces/{project_id}'

        # The global end-point only supports list methods, so you can't use
        # namespaces.services/get unless you know what region to use.
        request = service.namespaces().services().list(parent=parent)
        response = request.execute()
        for item in response['items']:
            if item['metadata']['name'] == k_service:
                url = item['status']['url']
                break
        else:
            raise EnvironmentError('Cannot determine service URL')

    return url
