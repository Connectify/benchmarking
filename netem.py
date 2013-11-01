import os
import sys
import traceback

import paramiko

class NetEm(object):
    '''
    classdocs
    '''

    def __init__(self, address):
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(address, 22,
                                username=os.environ['NETEM_USER'],
                                password=os.environ['NETEM_PW'])
        except Exception, e:
            print '*** Caught exception: %s: %s' % (e.__class__, e)
            traceback.print_exc()
            sys.exit(1)

    def __del__(self):
        print self.id, 'died'
        self.client.close()

    def configure_netem_port(self, port, rate, latency, loss):
        self.client.exec_command('uci set netem.'+port+'.enabled=1')
        self.client.exec_command('uci set netem.'+port+'.ratecontrol=1')
        self.client.exec_command('uci set netem.'+port+'.ratecontrol_rate='+rate)
        self.client.exec_command('uci set netem.'+port+'.delay=1')
        self.client.exec_command('uci set netem.'+port+'.delay_ms='+latency)
        self.client.exec_command('uci set netem.'+port+'.loss=1')
        self.client.exec_command('uci set netem.'+port+'.loss_pct='+loss)

    def configure_netem(self, nic, test_params):
        try:
            download_rate = str(int(1000*float(test_params['nic1_down_mbps'])))
            upload_rate = str(int(1000*float(test_params['nic1_up_mbps'])))
            latency = str(int(float(test_params['nic1_latency'])))
            loss = str(float(test_params['nic1_dropped']))
            #make sure lower number port is plugged into the PC and higher number port is plugged in upstream
            self.configure_netem_port('PORT' + str(2*nic-1), download_rate, latency, loss)
            self.configure_netem_port('PORT' + str(2*nic), upload_rate, latency, loss)

            self.client.exec_command('uci commit')
            self.client.exec_command('/etc/init.d/netem-control restart')

            #self.client.close()

        except Exception, e:
            print '*** Caught exception: %s: %s' % (e.__class__, e)
            traceback.print_exc()
            try:
                self.client.close()
            except:
                pass
            sys.exit(1)
