# encoding=utf-8
from fabric.api import *
import os

env.hosts = '47.107.184.22'
env.password = 'Wocao9988'
env.user = 'root'
env.port = '22'

local_work_dir = os.getcwd()
remote_git_dir = '/root/Liam/Projects/MDM/iOS_MDM_Guide'
remote_work_dir = '/root/Liam/Projects/MDM/iOS_MDM_Guide/MDM_Server'
remote_tmp_dir = '/root/Liam/Projects/MDM/tmp'

# replace it with the dir path where csr, key and mdm.cer locate.
cer_dir = '/Users/AstonWorkMac/Desktop/PAFiles/tech_requirements/MDM/Cer/'

# replace strings with real file name
user_submitted_CSR = os.path.join(cer_dir, 'CertificateSigningRequest.certSigningRequest')
mdm_vendor_private_key = os.path.join(cer_dir, 'PAPH_MDM_ZHANGLIANG203_vender.key')
mdm_certificate_from_apple = os.path.join(cer_dir, 'mdm.cer')


def cmt_push(msg):
    with lcd(local_work_dir):
        try:
            local('git add -A .')
            local('git commit -m "{}"'.format(msg))
            local('git push origin master')
        except:
            print('nothing to commit')
        finally:
            print('commit OK')

def up_remote():
    with cd(remote_work_dir):
        run('git pull')
        run('source venv/bin/activate')
        run('sh boot_dev.sh')

def push_up_remote(msg):
    cmt_push(msg)
    up_remote()

def generate_plist_encoded():
    with lcd(local_work_dir):
        local('source venv/bin/activate')
        cmd = 'python mdm_vendor_sign.py  --csr {} --key {} --mdm {}'.format(user_submitted_CSR, mdm_vendor_private_key, mdm_certificate_from_apple)
        local(cmd)
        local('deactivate')


def server_index():
    local('curl -k http://0.0.0.0:8800/')


def client_ssl_call_server():
    pub_key = '../../https/client/client_public_key.pem'
    pri_key = '../../https/client/client_private_key.pem'
    if not os.path.exists(pub_key):
        print('Error: client crt not found !')
        return
    local('curl --cert {} --key {} https://0.0.0.0:8800/'.format(pub_key,pri_key))

def sign_profile():
    with lcd('../../tmp/ali_mdm_cer/'):
        params = {
                "profile" : 'MDM_local_test.mobileconfig',
                "server_crt" : 'mdm_ng.pem',
                "server_key" : 'mdm_ng.key',
                "cert_chain_cert" : 'ca_chain.cer',
                "signed_profile": 'MDM_local_test_signed.mobileconfig'
        }
        local('ls')
        cmd = 'openssl smime -sign -in {profile} -out {signed_profile} -signer {server_crt} -inkey {server_key} -certfile {cert_chain_cert} -outform der -nodetach'.format(**params)
        print cmd
        local(cmd)

def py_sign():
    with lcd('../../tmp/ali_mdm_cer/'):
        params = {
                "profile" : 'MDM_local_test.mobileconfig',
                "signed_profile": 'MDM_local_test_signed.mobileconfig',
                "ph_dev_cer_name": 'iPhone Developer: 海锋 蒲 (Q4DAB6L47P)'
        }
        cmd = 'python ./profile_signer.py -n "{ph_dev_cer_name}" sign {profile} {signed_profile}'.format(**params)
        print cmd
        local(cmd)

def push_files():
    l_path = '../../tmp/ali_mdm_cer/MDM_local_test_signed.mobileconfig'
    s_file_name = 'MDM_local_test_signed.mobileconfig'
    server_path = os.path.join(remote_tmp_dir, s_file_name)
    put(l_path, server_path)
    if s_file_name.endswith('zip'):
        with cd(remote_tmp_dir):
            run('unzip {}'.format(s_file_name))







# params in api.env
# disable_known_hosts
# effective_roles
# tasks
# linewise
# show
# password
# key_filename
# abort_on_prompts
# skip_unknown_tasks
# reject_unknown_hosts
# skip_bad_hosts
# use_ssh_config
# roledefs
# gateway
# gss_auth
# keepalive
# eagerly_disconnect
# rcfile
# path_behavior
# hide
# sudo_prefix
# lcwd
# no_agent
# forward_agent
# remote_interrupt
# port
# shell
# version
# use_exceptions_for
# connection_attempts
# hosts
# gss_deleg
# cwd
# abort_exception
# real_fabfile
# passwords
# sudo_password
# host_string
# shell_env
# always_use_pty
# colorize_errors
# exclude_hosts
# all_hosts
# sudo_prompt
# again_prompt
# echo_stdin
# user
# gss_kex
# command_timeout
# path
# local_user
# combine_stderr
# command_prefixes
# dedupe_hosts
# warn_only
# no_keys
# sudo_passwords
# roles
# fabfile
# use_shell
# host
# pool_size
# system_known_hosts
# prompts
# output_prefix
# command
# timeout
# default_port
# ssh_config_path
# parallel
# sudo_user
# ok_ret_codes