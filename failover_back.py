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

import certifi

import urllib3.contrib.pyopenssl

import os

import subprocess

import time

import multiprocessing

import threading





def cifsservice(nas):

    time.sleep(5)

    for i in range(100):

            #print "Restarting cifs service ", i

            time.sleep(30)

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

    for i in range(50):

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



if __name__ == '__main__':

        vnx = VNXSystem('10.109.196.42', 'sysadmin', 'sysadmin', file_username='nasadmin', file_password='nasadmin')

        print "cs IP",vnx._get_cs_ip()

        nas = VNXNasConnections('10.109.196.41', 'nasadmin', 'nasadmin')

        cifs_service = multiprocessing.Process(target=cifsservice, args=(nas,))

        mover_failover = multiprocessing.Process(target=failover_failback, args=(nas,))

        mover_failover.start()

        cifs_service.start()

        cifs_service.join()

        mover_failover.join()
