from runhouse.rns.resource import Resource

from runhouse.rh_config import rns_client
from runhouse.rns.api_utils.utils import load_resp_content, read_resp_data

from typing import Dict, Optional, List, Union

import json
import logging
import requests


# secret.save() --> rns if account, local if no account
# secret.write()/put() --> write into local file system

# rh.cluster_secret()  (e.g. ssh config, kube config)
# - ssh config: json.dump or load the config into vault/file or pass in file+host name idk
# - secret scoped to one cluster that can be shared and reused by teammate

# .to(), .share()
# - .to uses updated put_resource rpc
# .get(), .put(), .update()
# .delete(), .remove()

# .from_config --> save it to proper place in filesystem/env so as not to save in python memory

# runhouse login behavior..

# look into generic parent class that can handle a dict mapping or something?

# Q: in memory secret but we don't want it in python memory right or..

# steps
# - skeleton code for base secret class
# - add a provider secret (aws)
# - add factory function for said provider secret
# - testing 
# - repeat with ssh cluster secret
# - repeat with custom secret
# - repeat with remaining provider secrets
# - runhouse login behavior
# - rh.env(secrets=List[Secrets])


class Secret(Resource):
    RESOURCE_TYPE = "secret"

    PROVIDER_NAME = None
    CREDENTIALS_FILE = None

    USER_ENDPOINT = "user/secret"
    GROUP_ENDPOINT = "group/secret"

    def __init__(
        self,
        name: str,
        secrets: Dict,
        save_to_file: bool = True,
        save_to_env: bool = False,
    ):
        self.name = name
        if save_to_file:
            self._save_to_file(secrets)
        if save_to_env:
            self._save_to_env(secrets)
    
    @classmethod
    def load_secrets(
        cls,
        names: List[str] = None,
        local_file: bool = True,
        environ: bool = False,
    ):
        """Load secrets from Vault or local environment. Optionally save to local file or environment, either to local file, environ, or both."""
        resp = requests.get(
            f"{rns_client.api_server_url}/{cls.USER_ENDPOINT}",
            headers=rns_client.request_headers,
        )
        if resp.status_code != 200:
            raise Exception("Failed to download secrets from Vault")

        secrets = read_resp_data(resp)
        if local_file:

    
    @classmethod
    def save_secrets(
        cls,
        names: Union[str, List[str]],
    ):
        """Save secrets into Vault, if user is logged in. Otherwise, save to local config files."""



    @classmethod
    def get_enabled():
        """
        Returns a list of secrets (names) that are enabled in Vault (if user is logged in), or locally if not.
        To save secrets from Vault to local, Secrets.save_secrets(Secrets.get_enabled()).
        """
    
    @classmethod
    def from_name(cls, name):
        """Load existing Secret via its name."""
        # pulls from vault and not rns client
    
    @classmethod
    def from_config(cls, config, file=True, environ=False):
        """"""
    
    def delete_configs(self):
        """Delete the Secret's config from local and Vault"""
    
    def is_local(self):
        """If the Secret exists locally."""
        # check if file or environ vars exist

    def save(
        self,
        name: str = None,
        overwrite: bool = True,
        file: bool = True,
        environ: bool = False,
    ):
        """Register the secret, saving it to local config and Vault."""
        # TODO: how to check if the user has an account to save
        resp = requests.put(
            f"{rns_client.api_server_url}/{self.USER_ENDPOINT}",
            data=json.dumps(self.get_secrets()),
            headers=rns_client.request_headers,
        )

        if resp.status_code != 200:
            raise Exception(
                f"Failed to update secrets in Vault: {load_resp_content(resp)}"
            )
        logging.info(f"Uploaded secrets for to Vault")

        if file:
            self._save_to_file()
        if environ:
            self._save_to_environ()
    
    def get(
        self,
        key: Optional[str] = None,
    ):
        """
        If key is provided, return the value associated with that key for the secret.
        Otherwise, get the secret from local. 
        """
        secrets = Secret.load_secrets(names=[self.name])
        if key:
            return secrets[key]
        return secrets
        

    def put(
        self,
        entry: Dict = None,
    ):
        """
        If key is provided, update the secret config. Write the secret to local.
        """
        if entry:
            self.secrets.update(entry)
        
    
    def is_enabled(self):
        raise NotImplementedError
    
    def share(self, user):
        raise NotImplementedError
    
    def to(self, system):
        # TODO: use put_resource rpc
        raise NotImplementedError

    def _save_to_file(self):
        # TODO: implement generic version for custom secrets
        raise NotImplementedError

    def _save_to_environ(self):
        # TODO: implement generic version for custom secrets
        raise NotImplementedError

    def _load_from_file(self):
        raise NotImplementedError
    
    def _load_from_environ(self):
        raise NotImplementedError