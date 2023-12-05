import os
import socket

from pprint import pprint
from urllib.request import urlopen
from kubernetes import client, config


def main():
    config.load_incluster_config()
    api = client.CustomObjectsApi()

    # Get a comma-separated list of domains from the environment variable
    custom_domains = os.environ.get('ALLOW_LIST_DOMAINS')
    domains = custom_domains.split(',') if custom_domains else []

    current_ips = []
    public_ips = urlopen('https://api.ipify.org').read().decode('utf8')
    current_ips.append(public_ips)

    for domain in domains:
        if domain:
            ip_list = socket.gethostbyname_ex(domain)[2]
            for ip in ip_list:
                current_ips.append(ip)

    patch_body = {
        "spec": {
            "ipWhiteList": {
                "sourceRange": current_ips
            }
        }
    }

    name = os.environ.get('ALLOW_LIST_MIDDLEWARE_NAME', 'ip-allowlist')
    namespace = os.environ.get('ALLOW_LIST_TRAEFIK_NAMESPACE', 'traefik-system')

    patch_resource = api.patch_namespaced_custom_object(
        group="traefik.containo.us",
        version="v1alpha1",
        name=name,
        namespace=namespace,
        plural="middlewares",
        body=patch_body,
    )

    print("Current state of the middleware: ")
    pprint(patch_resource)

if __name__ == '__main__':
    main()
