
from storops import VNXSystem
from storops.vnx.resource.nfs_share import VNXNfsShare
from storops.vnx.resource.cifs_share import VNXCifsShare
from storops.vnx.resource.cifs_server import VNXCifsServer
from storops.vnx.resource.vdm import VNXVdm
from storops.vnx.resource.nas_pool import VNXNasPool
from storops.vnx.nas_client import VNXNasClient
from storops.vnx.resource.fs import VNXFileSystem
from storops.vnx.nas_client import VNXNasClient
from storops.vnx.resource.fs import VNXFileSystem
from storops.vnx.resource import VNXCliResource
from storops.exception import VNXDiskUsedError, raise_if_err, VNXSetArrayNameError
from storops.lib.common import daemon, instance_cache, clear_instance_cache
from storops.lib.resource import ResourceList, ResourceListCollection
from storops.lib.common import daemon, instance_cache, clear_instance_cache
from storops.lib.resource import ResourceList, ResourceListCollection
from storops.vnx.resource.cifs_server import CifsDomain
from storops.vnx.nas_client import VNXNasConnections
import time
import subprocess
import multiprocessing
import threading
import urllib3
import certifi
import urllib3.contrib.pyopenssl
import os





##SMB1 - node3
def smb1(cifs_server, domain_name, share_name, domain_user, domain_password,interface_ip):
    """
    win_ping = "ansible node3 -i  /root/win_environment/hosts -m win_ping"
    enable_smb1_node3 = subprocess.check_output("ansible node3 -i  /root/win_environment/hosts  -m win_command -a 'powershell.exe sc.exe config lanmanworkstation depend= bowser/mrxsmb10/mrxsmb20/nsi ; sc.exe config mrxsmb10 start= auto'",shell=True)
    print enable_smb1_node3
    disable_smb2_node3 = subprocess.check_output("ansible node3 -i  /root/win_environment/hosts  -m win_command -a 'powershell.exe sc.exe config lanmanworkstation depend= bowser/mrxsmb10/nsi ; sc.exe config mrxsmb20 start= disabled'",shell=True)
    print disable_smb2_node3

    shutdown_result_node3 = subprocess.check_output("ansible node3 -i  /root/win_environment/hosts  -m win_command -a 'powershell.exe shutdown /r'", shell=True)
    print shutdown_result_node3

    time.sleep(60)

    ping_result_node3 = os.system(win_ping)

    while ping_result_node3 != 0:
        time.sleep(10)
        ping_result_node3 = os.system(win_ping)
    """
    create_dir = "ansible nodes -m shell -a 'mkdir /mnt/testsmb1'"
    create_dirs =  subprocess.check_output(create_dir, shell=True)
    mount_linux = "ansible nodes -m shell -a ' mount -t cifs //{}/{} /mnt/testsmb1 -o sec=ntlm,username=cifsuser,pass=cifsuser'".format(interface_ip,share_name)
    mount_linuxs = subprocess.check_output(mount_linux, shell=True)
    io = subprocess.check_output("ansible nodes -m shell -a 'fio /newprofile.fio > /fio_output_smb1 &'",shell=True)
    print "SMB1 connection Establishing"
    ping = subprocess.check_output("ansible node3 -i /root/win_environment/hosts -m win_ping", shell=True)
    print ping

    x = "ansible node3 -i /root/win_environment/hosts -m win_command -a 'powershell.exe net use M: \\\\{}.{}\\{} /user:{} {}; Get-SMBConnection ; sleep(1500) ; net use M: /d'".format(
        cifs_server, domain_name, share_name, domain_user, domain_password)
    mount_result_node3 = subprocess.check_output(x, shell=True)
    print mount_result_node3


##SMB2 - node2
def smb2(cifs_server, domain_name, share_name, domain_user, domain_password,interface_ip):
    create_dir = "ansible nodes -m shell -a 'mkdir /mnt/testsmb2'"
    create_dirs =  subprocess.check_output(create_dir, shell=True)
    mount_linux = "ansible nodes -m shell -a ' mount -t cifs //{}/{} /mnt/testsmb2 -o sec=ntlm,username=cifsuser,pass=cifsuser,vers=2.1'".format(interface_ip,share_name)
    mount_linuxs = subprocess.check_output(mount_linux, shell=True)
    io = subprocess.check_output("ansible nodes -m shell -a 'fio /newprofile.fio  > /fio_output_smb2 &'",shell=True)
    print "SMB2 Connection ESTABLISHING "
    ping = subprocess.check_output("ansible node2 -i /root/win_environment/hosts -m win_ping", shell=True)
    print ping
    x = "ansible node2 -i /root/win_environment/hosts -m win_command -a 'powershell.exe net use M: \\\\{}.{}\\{} /user:{} {}; Get-SMBConnection ; sleep(1500) ; net use M: /d'".format(
        cifs_server, domain_name, share_name, domain_user, domain_password)
    mount_result_node2 = subprocess.check_output(x, shell=True)
    print mount_result_node2


"""
def cifsservice(nas):
    time.sleep(5)
    for i in range(200):
            #print "Restarting cifs service ", i
            time.sleep(10)
            x = nas.ssh_execute('/nas/bin/server_setup server_4 -P cifs -o stop'.split(' '), check_exit_code=False)
            #print x
            if x.find('Error') != -1:
                    time.sleep(5)
                    #print 'Unable to restart cifs service'
                    continue
            #print "Cifs service stop : ",x
            nas.ssh_execute('/nas/bin/server_setup server_4 -P cifs -o start'.split(' '), check_exit_code=False)
            #print "Cifs service started : ",y
            #print "coming out of the cifservice function iteration",i


def failover_failback(nas):
    for i in range(100):
        print "Inside Failover and Failback function ", i
        x = nas.ssh_execute('/nas/bin/server_standby server_4 -a mover'.split(' '), check_exit_code=False)
        if x.find('Error') == -1:
            print 'Insisde error code'
            print x
            time.sleep(10)
            continue
        print "standby ",x
        time.sleep(75)
        y = nas.ssh_execute('/nas/bin/server_standby server_4 -r mover'.split(' '), check_exit_code=False)
        print "restore ",y
        print "Coming out of the failover function iteration",i
        time.sleep(75)
"""



if __name__ == '__main__':
    #Handle http error
    urllib3.disable_warnings();
    urllib3.contrib.pyopenssl.inject_into_urllib3();

    http=urllib3.PoolManager(
          cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where());

    vnx = VNXSystem('10.109.196.42', 'sysadmin', 'sysadmin', file_username='nasadmin', file_password='nasadmin')
    print vnx._get_cs_ip()

    nas = VNXNasConnections('10.109.196.41', 'nasadmin', 'nasadmin')

    vdm_name = 'av_vdm'

    vdm1 = VNXVdm(name=vdm_name, cli=vnx._file_cli)
    mover = vnx.get_mover(name='server_4', mover_id=3)
    mover_id = mover.get_mover_id()
    mover_name = mover._get_name()
    interface = None
    cifsserver = None
    fs = None
    cifsshare = None
    cifsserver_name = 'vdmcifsserver1'
    domain = CifsDomain(name='NCC2K8.USD.LAB.EMC.COM', user='cifsuser', password='cifsuser')
    print "\n" + "Domain object created\n" + "\n"
    print domain
    if vdm1.existed is False:
        print mover
        print 'mover_id', mover_id
        print mover_name
        time.sleep(10)
        vdm = VNXVdm.create(cli=vnx._file_cli, mover_id=mover_id, name=vdm_name, pool_id=83)
        print "\n" + "creating VDM" + "\n"
        print vdm

        time.sleep(3)

        interface = vdm.create_interface(device='cge-1-0', ip='10.109.196.91', net_mask='255.255.255.0',
                                         name='10-109-196-91')
        print "Interface creation" + "\n"
        print interface
        time.sleep(3)
        attaching_interface = vdm.attach_nfs_interface(if_name='10-109-196-91')
        print "\n" + "Attaching interface" + "\n"
        print attaching_interface
        print 'vdm.get_mover_id()', vdm.get_mover_id()
        time.sleep(3)
        time.sleep(3)


        time.sleep(3)

        fs = VNXFileSystem.create(cli=vnx._file_cli, name='vdm_fs', pool=83, size_kb=102400, mover=vdm.get_mover_id(),
                                  is_vdm=True)
        print "\n" + "creating file system" + "\n"
        print fs
        fs_mount_str = '/nas/bin/server_mount ' + vdm_name + ' -o rw,smbca vdm_fs /vdm_fs'
        nas.ssh_execute(fs_mount_str.split(' '))

        cifsserver = VNXCifsServer.create(cli=vnx._file_cli, name='vdmcifsserver1', mover_id=vdm.get_mover_id(),
                                          is_vdm=True, domain=domain, interfaces='10.109.196.91',
                                          alias_name="vdmcifsserver1")

        print "\n" + "creating cifsserver " + "\n"
        print cifsserver
        time.sleep(3)

        print "\n" + "creating cifs share" + "\n"
        cifsshare_str = '/nas/bin/server_export ' + vdm_name + ' -P cifs -o type=CA,netbios=vdmcifsserver1 -name vdm_fs /vdm_fs'
        nas.ssh_execute(cifsshare_str.split(' '))
        cifsshare = VNXCifsShare(name='vdm_fs', mover=vdm, cli=vnx._file_cli)
        print cifsshare
        interface_ip = '10.109.196.91'
        cifs_server = cifsserver_name
        domain_name = domain.name
        domain_user = domain.user
        domain_password = domain.password
        share_name = fs.get_name()

        ##Restricting the DM (server_4) max to SMB2
        p = nas.ssh_execute('/nas/bin/server_setup server_4 -P cifs -o stop'.split(' '))
        q = nas.ssh_execute('/nas/bin/server_cifs server_4 -add security=NT,dialect=SMB2'.split(' '))
        r = nas.ssh_execute('/nas/bin/server_setup server_4 -P cifs -o start'.split(' '))
        print "inside main cifsservice "
        print p,q,r
        print "ending cifs service inside main"

        ping_cifsserver = os.system("ping -c 4 {}.{}".format(cifs_server, domain_name))
        if ping_cifsserver == 0:
                flag = multiprocessing.Value('i', 0)
                smb_1 = multiprocessing.Process(target=smb1,
                                                args=(cifs_server, domain_name, share_name, domain_user, domain_password, interface_ip))
                smb_2 = multiprocessing.Process(target=smb2,
                                                args=(cifs_server, domain_name, share_name, domain_user, domain_password, interface_ip))

                #cifs_service = multiprocessing.Process(target=cifsservice, args=(nas,))
                #mover_failover = multiprocessing.Process(target=failover_failback, args=(nas,))
                #getreason = multiprocessing.Process(target=watch_getreason, args=(nas,))
                smb_1.start()
                smb_2.start()
                #time.sleep(50)
                time.sleep(10)
                #mover_failover.start()
                #time.sleep(8)
                #cifs_service.start()
                #getreason.start()

                smb_1.join()
                smb_2.join()
                #cifs_service.join()
                #mover_failover.join()
                #getreason.join()

                ##CLEAN
                time.sleep(10000)
                print "Clean up started"
        else:
                print "Cifsserver is not pinging"
                print "clean up started "
        cifsshare.delete('vdmcifsserver1')
        print "share deleted" + "\n" + "\n" + "\n"
        fs.delete()
        print "\n" + "\n" + "file deleted" + "\n" + "\n" + "\n"
        cifsserver.delete(mover_id=vdm.get_mover_id(), is_vdm=True)
        print "\n" + "\n" + "cifsserver deleted" + "\n" + "\n"
        vdm.detach_nfs_interface(if_name='10-109-196-91')
        print "\n" + "\n" + "Interface detached" + "\n" + "\n"
        if vdm.existed == True:
            vdm.delete()
            print "\n" + "\n" + "vdm deleted" + "\n" + "\n"
            nas.ssh_execute('/nas/bin/server_ifconfig server_4 -d 10-109-196-91'.split(' '))
            nas.ssh_execute('/nas/bin/server_setup server_4 -P cifs -o stop'.split(' '))
            nas.ssh_execute('/nas/bin/server_setup server_4 -P cifs -o start'.split(' '))
            print "Interface deleted"

    else:
        print('{} {}."already exists"'.format("vdm - > ", vdm_name))
        print "\n"
