import subprocess
import os
import time
import re

__author__ = 'Avinash Gaurav'

"""

This module is used to call ansible based commands in a very abstract manner .
Prerequisites:
    - python should be installed on master node
    - Code should be executed on master node only
    - Ansible should be running on the master as well as the client nodes(win or linux).
    - The client machines should be up and pingable.
    - pywinrm package should be installed on the master node  (use command : pip install pywinrm).
    - All the arguments should be passed as a string.
    - For win client nodes, mount and clean up are done by the method itself .
    - In order to call io based methods make sure fio is running on the client nodes(win or linux).

"""

class Ansible:

        @classmethod
        def enable_smb1_win(self, node, path = '/root/win_environment/hosts'):
            win_ping = "ansible {} -i  {} -m win_ping".format(node,path)
            ping_value = subprocess.check_output(win_ping,shell = True)
            ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ping_value )
            out = "Unable to ping ",ip
            if os.system(win_ping) == 0:
                enable_smb1 = subprocess.check_output("ansible {} -i  {}  -m win_command -a 'powershell.exe sc.exe config lanmanworkstation depend= bowser/mrxsmb10/mrxsmb20/nsi ; sc.exe config mrxsmb10 start= auto'".format(node,path),shell=True)
                print enable_smb1
                disable_smb2 = subprocess.check_output("ansible {} -i  {}  -m win_command -a 'powershell.exe sc.exe config lanmanworkstation depend= bowser/mrxsmb10/nsi ; sc.exe config mrxsmb20 start= disabled'".format(node,path),shell=True)
                print disable_smb2
                shutdown_result = subprocess.check_output("ansible {} -i  {}  -m win_command -a 'powershell.exe shutdown /r'".format(node,path), shell=True)
                print shutdown_result
                time.sleep(60)
                ping_value = os.system(win_ping)
                while ping_value != 0:
                    time.sleep(10)
                    ping_value = os.system(win_ping)
                out = 'SMB1 enabled on :',ip
            return out

        @classmethod
        def enable_smb2_3_win(self, node, path = '/root/win_environment/hosts'):
            win_ping = "ansible {} -i  {} -m win_ping".format(node,path)
            ping_value = subprocess.check_output(win_ping,shell = True)
            ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ping_value )
            out = "Unable to ping ",ip
            if os.system(win_ping) == 0:
                enable_smb1 = subprocess.check_output("ansible {} -i  {}  -m win_command -a 'powershell.exe sc.exe config lanmanworkstation depend= bowser/mrxsmb10/mrxsmb20/nsi ; sc.exe config mrxsmb10 start= auto'".format(node,path),shell=True)
                print enable_smb1
                enable_smb2 = subprocess.check_output("ansible {} -i  {}  -m win_command -a 'powershell.exe sc.exe config lanmanworkstation depend= bowser/mrxsmb10/mrxsmb20/nsi ; sc.exe config mrxsmb20 start= auto'".format(node,path),shell=True)
                print enable_smb2
                shutdown_result = subprocess.check_output("ansible {} -i  {}  -m win_command -a 'powershell.exe shutdown /r'".format(node,path), shell=True)
                print shutdown_result
                time.sleep(60)
                ping_value = os.system(win_ping)
                while ping_value != 0:
                    time.sleep(10)
                    ping_value = os.system(win_ping)
                out = 'SMB2 / SMB3 enabled on :',ip
            return out


        @classmethod
        def mount_share_win(self,cifs_server, domain_name, share_name, domain_user, domain_password, node, path = '/root/win_environment/hosts',timeout_in_sec = '100'):
            win_ping = "ansible {} -i  {} -m win_ping".format(node,path)
            ping_value = subprocess.check_output(win_ping,shell = True)
            ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ping_value )
            out = "Unable to ping ",ip
            if os.system(win_ping) == 0:
                x = "ansible {} -i {} -m win_command -a 'powershell.exe net use M: \\\\{}.{}\\{} /user:{} {}; Get-SMBConnection ; sleep(timeout_in_sec) ; net use M: /d'".format(node, path, cifs_server, domain_name, share_name, domain_user, domain_password)
                mount_result = subprocess.check_output(x, shell=True)
                out = "Mounted share {} on the host having  IP: {}".format(share_name,ip)
            return out

        @classmethod
        def create_fio_profile_win(self, node, size, path = '/root/win_environment/hosts', drive_letter = 'T' , runtime_in_sec='605000',folder_name='fio_test'):
            win_ping = "ansible {} -i  {} -m win_ping".format(node,path)
            ping_value = subprocess.check_output(win_ping,shell = True)
            ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ping_value )
            out = "Unable to ping ",ip
            if os.system(win_ping) == 0:
                io_str = "echo -e '[global]\\nioengine=windowsaio\\nexitall_on_error=1\\ninvalidate=1\\ndirect=1\\nrw=randrw\\nrefill_buffers=1\\nbsrange=4k-32k\\ntime_based=1\\nverify=md5\\ndo_verify=1\\nruntime={}\\nsize={}\\ndirectory={}\:\\\{}'".format(runtime_in_sec,size,drive_letter,folder_name).strip()
                profile = io_str+" > /win_profile.fio"
                subprocess.check_output(fio_profile,shell=True)
                create_fio_profile = "ansible {} -i {}  -m win_copy -a 'src=/win_profile.fio dest=C:\\'".format(node,path,fio_profile)
                fio_profile = subprocess.check_output(create_fio_profile,shell=True)
                return fio_profile
            else:
                return out


        @classmethod
        def mount_share_win_initiate_io(self,node,size,cifs_server, domain_name, share_name, domain_user, domain_password, path = '/root/win_environment/hosts',timeout_in_sec = '60500', drive_letter = 'T' , runtime_in_sec='60500',folder_name='fio_test'):
            win_ping = "ansible {} -i  {} -m win_ping".format(node,path)
            ping_value = subprocess.check_output(win_ping,shell = True)
            ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', ping_value )
            out = "Unable to ping ",ip
            if os.system(win_ping) == 0:
                create_fio_profile(self,node=node,size=size,path=path,drive_letter=drive_letter,runtime_in_sec=runtime_in_sec,folder_name=folder_name)
                x = "ansible {} -i {} -m win_command -a 'powershell.exe net use {}: \\\\{}.{}\\{} /user:{} {}; Get-SMBConnection ; fio C:\\win_profile.fio ; sleep(timeout_in_sec) ; net use {}: /d'".format(node, path, drive_letter ,cifs_server, domain_name, share_name, domain_user, domain_password,drive_letter)
                mount_fio_result = subprocess.check_output(x, shell=True)
                out = "Mounted share {} on the host having  IP: {}".format(share_name,ip)
                return out,mount_fio_result
            else:
                return out,": Fio can't be  initiated as the host is down"


        @classmethod
        def mount_share_smb1_linux(self,interface_ip, share_name, username, password, node, mount_dir = 'smb1_test'):
            dirs = "ansible {} -m shell -a 'mkdir /mnt/{}'".format(node,mount_dir)
            create_dirs =  subprocess.check_output(dirs, shell=True)
            mount_linux = "ansible {} -m shell -a ' mount -t cifs //{}/{} /mnt/{} -o sec=ntlm,username={},password={},vers=1.0'".format(node, interface_ip, share_name, mount_dir, username, password)
            mount_linuxs = subprocess.check_output(mount_linux, shell=True)
            print "SMB2 connection Establishing and the mounted dir is :"+"/mnt/"+mount_dir,mount_linuxs

        @classmethod
        def mount_share_smb2_linux(self,interface_ip, share_name, username, password, node, mount_dir = 'smb2_test'):
            dirs = "ansible {} -m shell -a 'mkdir /mnt/{}'".format(node,mount_dir)
            create_dirs =  subprocess.check_output(dirs, shell=True)
            mount_linux = "ansible {} -m shell -a ' mount -t cifs //{}/{} /mnt/{} -o sec=ntlm,username={},password={},vers=2.0'".format(node, interface_ip, share_name, mount_dir, username, password)
            mount_linuxs = subprocess.check_output(mount_linux, shell=True)
            print "SMB2 connection Establishing and the mounted dir is :"+"/mnt/"+mount_dir


        @classmethod
        def mount_share_smb3_linux(self,interface_ip, share_name, username, password, node, mount_dir = 'smb3_test'):
            dirs = "ansible {} -m shell -a 'mkdir /mnt/{}'".format(node,mount_dir)
            create_dirs =  subprocess.check_output(dirs, shell=True)
            mount_linux = "ansible {} -m shell -a ' mount -t cifs //{}/{} /mnt/{} -o sec=ntlm,username={},password={},vers=3.0'".format(node, interface_ip, share_name, mount_dir, username, password)
            mount_linuxs = subprocess.check_output(mount_linux, shell=True)
            print "SMB2 connection Establishing and the mounted dir is :"+"/mnt/"+mount_dir,mount_linuxs

        @classmethod
        def mount_share_smb_linux(self, node, interface_ip, share_name, username, password, vers, mount_dir_name = 'smb_test'):
            mount_dir = mount_dir+'_'+vers
            dirs = "ansible {} -m shell -a 'mkdir /mnt/{}'".format(node,mount_dir)
            create_dirs =  subprocess.check_output(dirs, shell=True)
            mount_linux = "ansible {} -m shell -a ' mount -t cifs //{}/{} /mnt/{} -o sec=ntlm,username={},password={},vers={}'".format(node, interface_ip, share_name, mount_dir, username, password,vers)
            mount_linuxs = subprocess.check_output(mount_linux, shell=True)
            print "SMB2 connection Establishing and the mounted dir is :"+"/mnt/"+mount_dir,mount_linuxs



        @classmethod
        def linux_fio(self, node, size, dirs, runtime_in_sec='605000', block_size='8k',folder_to_be_created='dir-testio'):
            io_str = "echo -e '[global]\\nioengine=libaio\\ndirect=1\\nrefill_buffers=1\\nrw=write\\ndo_verify=1\\nexitall_on_error=1\\nfallocate=none\\ntime_based=1\\nsize={}\\nruntime={} \\n \\n[{}] \\ndirectory={}\\nbs={}'".format(size,runtime_in_sec,folder_to_be_created,dirs,block_size).strip()
            fio_profile = io_str+" > /linux_profile.fio"
            create_fio_profile = "ansible {} -m shell -a \"{}\"".format(node,fio_profile)
            print create_fio_profile
            fio_profile = subprocess.check_output(create_fio_profile,shell=True)
            print fio_profile
            run_fio = "ansible {} -m shell -a 'fio /linux_profile.fio'".format(node)
            run_fio = subprocess.check_output(run_fio,shell =True)
            return "Fio is running",run_fio

        @classmethod
        def mount_nfs_share(self, node, interface_ip,share_name, vers,minorversion='0',mount_dir_name ='test_nfs'):
            mount_dir = mount_dir_name+'_'+vers
            dirs = "ansible {} -m shell -a 'mkdir /mnt/{}'".format(node,mount_dir)
            create_dirs =  subprocess.check_output(dirs, shell=True)
            if vers == '4':
                mount_dir=mount_dir+'_'+minorversion
                mount_linux = "ansible {} -m shell -a ' mount -t nfs {}:/{} /mnt/{} -o vers={},minorversion={},sec=sys'".format(node, interface_ip, share_name, mount_dir, vers, minorversion)
                mount_linuxs = subprocess.check_output(mount_linux, shell=True)
            else:
                mount_linux = "ansible {} -m shell -a ' mount -t nfs {}:/{} /mnt/{} -o vers={},sec=sys'".format(node, interface_ip, share_name, mount_dir, vers)
                mount_linuxs = subprocess.check_output(mount_linux, shell=True)
            return "NFS share mounted and the mounted dir is :"+"/mnt/"+mount_dir,mount_linuxs
