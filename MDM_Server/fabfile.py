from fabric.api import *
import os

work_dir = os.getcwd()

# replace it with the dir path where csr, key and mdm.cer locate.
cer_dir = '/Users/AstonWorkMac/Desktop/PAFiles/tech_requirements/MDM/Cer/'

# replace strings with real file name
user_submitted_CSR = os.path.join(cer_dir, 'CertificateSigningRequest.certSigningRequest')
mdm_vendor_private_key = os.path.join(cer_dir, 'PAPH_MDM_ZHANGLIANG203_vender.key')
mdm_certificate_from_apple = os.path.join(cer_dir, 'mdm.cer')

def generate_plist_encoded():
    with lcd(work_dir):
        local('source venv/bin/activate')
        cmd = 'python mdm_vendor_sign.py  --csr {} --key {} --mdm {}'.format(user_submitted_CSR, mdm_vendor_private_key, mdm_certificate_from_apple)
        local(cmd)




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