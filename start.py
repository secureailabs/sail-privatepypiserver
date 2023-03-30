
import json
import os
import subprocess

import bcrypt

container_name = "co_pipyserver"
local_path = os.getcwd()
# stop running container
subprocess.run(f"docker stop {container_name}", shell=True)
subprocess.run(f"docker rm {container_name}", shell=True)

# update htpasswd
path_file_htpasswd = os.path.join(local_path, "data", ".htpasswd")

def encrypt_password(username:str, password:str):
    bcrypted = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")
    return f"{username}:{bcrypted}"

list_line_htpasswd = []
with open("users.json", "r") as file:
    list_user = json.load(file)["list_user"]
    for user in list_user:
        list_line_htpasswd.append(encrypt_password(user["username"], user["password"]))

with open(path_file_htpasswd, "w") as password_file:
    password_file.writelines(list_line_htpasswd)

# start container
path_dir_data = os.path.abspath(os.path.join(local_path, "data"))
path_dir_packages = os.path.abspath(os.path.join(local_path, "packages"))
if not os.path.isdir(path_dir_packages):
    os.mkdir(path_dir_packages)
command = f"docker run -d --name {container_name} -p 80:8080"
command += f" -v {path_dir_data}:/data/"
command += f" -v {path_dir_packages}:/data/packages/"
command += " pypiserver/pypiserver:latest"
command += " -P .htpasswd packages"
subprocess.run(command, shell=True)


# https://pypi.org/project/pypiserver/#nginx
# https://medium.com/geekculture/setting-a-private-pypi-server-with-nginx-acbb73c8516d
# https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/