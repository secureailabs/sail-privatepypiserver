# find a single vm allocates to host the service
import os

from arin_core_azure.compute_helper import ComputeHelper
from arin_core_azure.resource_helper import ResourceHelper
from arin_core_azure.ssh_helper import SshHelper

subscription_name = "Development"
path_file_key = "c:/key/jaap-pipyserver-key.pem"
git_repo_url = "github.com/secureailabs/sail-privatepypiserver"
path_file_git_token = os.environ.get("PATH_FILE_GIT_TOKEN")

if not os.path.isfile(path_file_key):
    print(f"Key file not found at: {path_file_key}")
    exit(0)

if path_file_git_token is None:
    print("Please set environment variable PATH_FILE_GIT_TOKEN")
    exit(0)

with open(path_file_git_token, "r") as f:
    git_token = f.read()

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


hostname = compute_helper.get_vm_public_ip_address(vm_target)
username = compute_helper.get_vm_admin_username(vm_target)


print(f"found server for pipy server at: {hostname}")

ssh_helper = SshHelper(hostname, username, path_file_key)

# print("installing docker.io")
# ssh_helper.install_remote(["docker.io git python3-pip"], do_update=False)
print("cloning repo")

ssh_helper.clone_remote_with_token(git_repo_url, git_token)
