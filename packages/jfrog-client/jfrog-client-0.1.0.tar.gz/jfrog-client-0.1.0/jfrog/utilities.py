""" shared functions to manage Jfrog Platform """
import logging

# The different levels of logging, from highest urgency to lowest urgency, are:
# CRITICAL | ERROR | WARNING | INFO | DEBUG
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)


def __validate_url(url):
    updateurl = 'You should update the base url.'
    url = url.strip()
    if url.lower().endswith('/'):
        logging.warning(
            "Found a / at the end of the URL this has been removed.")
        logging.warning(updateurl)
        url = url.strip("/")
    if url.lower().endswith('/artifactory'):
        logging.warning(
            "Found /artifactory at the end of the URL this has been removed.")
        logging.warning(updateurl)
        url = url.strip("/artifactory")
    if url.lower().endswith('/xray'):
        logging.warning(
            "Found /xray at the end of the URL this has been removed.")
        logging.warning(updateurl)
        url = url.strip("/xray")
    if url.lower().endswith('/mc'):
        logging.warning(
            "Found /mc at the end of the URL this has been removed.")
        logging.warning(updateurl)
        url = url.strip("/mc")
    return url


def setlayout(ptype):
    ''' Choose the correct default layout based on the repository type '''
    specialtypes = ['bower', 'cargo', 'composer', 'conan', 'go', 'ivy',
                    'npm', 'nuget', 'puppet', 'sbt', 'swift', 'vcs']
    if ptype.lower() in ['maven', 'gradle']:
        return 'maven-2-default'
    if ptype.lower() in specialtypes:
        return ptype.lower() + '-default'
    return 'simple-default'
