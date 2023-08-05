from .secret import Secret

from typing import Dict, Optional

# if no config w/ provider, try to pull in from local

def secret(
    config: Dict,
    name
):


def provider_secret(
    name: str,
    provider: str = None,
    config: Dict = None,
    file_path: Optional[str] = None,
    from_env: bool = None,
):
    # get the provider secret class for the provider
    # instantiate with the provider secret class, passing in the same vars
    

def cluster_secret(
    name: str,
    config: Dict = None,
    file_path: Optional[str] = None,
    from_env: bool = False,
):

def custom_secret(
    config: Dict,
    name: str = None,
    creds_file: str = None,
    file_path: Optional[str] = None,
    from_env: bool = False,
):
