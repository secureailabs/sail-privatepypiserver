# This script is used to deploy the pipy server to a single VM
# it depends on the following packages:
# sail-core-azure==1.0.0

from typing import List

import requests
from arin_core_azure.compute_helper import ComputeHelper
from arin_core_azure.resource_helper import ResourceHelper


def list_pypi_packages(server_ip: str) -> List[str]:
    pypi_url = f"http://{server_ip}/simple"
    response = requests.get(pypi_url)
    if response.status_code == 200:
        return extract_package_names(response.text)
    else:
        raise RuntimeError(f"An error occurred: {response.status_code}")


def extract_package_names(html_content) -> List[str]:
    start_marker = '<a href="'
    end_marker = '/">'
    package_names = []
    while start_marker in html_content:
        start_index = html_content.index(start_marker)
        html_content = html_content[start_index + len(start_marker) :]
        end_index = html_content.index(end_marker)
        package_name = html_content[:end_index]
        package_names.append(package_name)

    return package_names


# # find vm with the pypi server tag
subscription_name = "Development"
compute_helper = ComputeHelper()
resource_helper = ResourceHelper()

subscription_id = resource_helper.get_subscription_id(subscription_name)

list_vm = compute_helper.list_vm_with_tag(subscription_id, "Purpose", "pipyserver")
if len(list_vm) == 0:
    print("No VM found with correct tag, please check again")
    exit(0)
if len(list_vm) > 1:
    print("More than 1 VM found with correct tag, please check again")
    exit(0)
vm_target = list_vm[0]


ip_address = compute_helper.get_vm_private_ip_address(vm_target)
print(f"found server for pipy server at: {ip_address}")
list_package = list_pypi_packages(ip_address)
print(f"{len(list_package)} packages found")
for package in list_package:
    print(package)
