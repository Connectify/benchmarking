import unittest
import time
import csv
import os
import sys
import traceback
import spreadsheetReporter
from netem import NetEm
from pageloadexperiment import PageloadExperiment


def reportPageloadResults(reporter, delays, packets, test_params):
    try:
        #print delays
        columns = reporter.SanitizeHeader(delays[0])
        #print columns
        for key in test_params:
            columns.append(reporter.SanitizeHeaderString(key))
            #print key, 'corresponds to', d[key]
        column_str = ",".join(columns)
        #print column_str
        reporter.AppendHeading(column_str)
        delay_row = ''
        for i in range(len(delays[1])):
            delay_row = delay_row + columns[i].strip() + '=' + delays[1][i].strip() + ' '
        for key in test_params:
            delay_row = delay_row + reporter.SanitizeHeaderString(key) + '=' + test_params[key] + ' '
        #print delay_row.strip()
        reporter.AppendResultRow(delay_row.strip())
        #print packets
    except Exception, e:
        print '*** Caught exception: %s: %s' % (e.__class__, e)
        traceback.print_exc()
        sys.exit(1)

class Test(unittest.TestCase):
    netem = NetEm(os.environ['NETEM_IP'])

    def setUp(self):
        self.gdocs_user = os.environ['GDOCS_USER']
        self.gdocs_pw = os.environ['GDOCS_PW']
        pass

    def tearDown(self):
        pass

    def test_reporting(self):
        try:
            reporter = spreadsheetReporter.SpreadsheetReporter(self.gdocs_user,
                                                               self.gdocs_pw)
            reporter.AppendHeading('col1,col2,col3,col4')
            reporter.AppendResultRow('col1=1.0 col2=2.0 col3=3.0 col4=4.0')
        except Exception, e:
            print '*** Caught exception: %s: %s' % (e.__class__, e)
            traceback.print_exc()
            sys.exit(1)

    def run_speedtest(self, reporter, test_params, urls_file):
        print 'Testing ' + test_params['nic1_down_mbps'] + '/' + test_params['nic1_up_mbps']+ ' Mbps'
        # set up netem box with parameters
        print 'Configuring router...'
        self.netem.configure_netem(1, test_params)
        print 'Configured!'

        # run speedtest
        print 'Running speedtest...'

        use_wget = False
        quic_binary_dir = 'bin'
        quic_server_address = os.environ['QUIC_SERVER_IP']
        quic_server_port = '6121'

        try:
            # test QUIC
            exp = PageloadExperiment(False,
                                     quic_binary_dir,
                                     quic_server_address,
                                     quic_server_port)
            delays, packets = exp.RunExperiment(urls_file)
            reportPageloadResults(reporter, delays, packets, test_params)

            # test wget
            exp = PageloadExperiment(True,
                                     quic_binary_dir,
                                     quic_server_address,
                                     quic_server_port)
            delays, packets = exp.RunExperiment(urls_file)
            reportPageloadResults(reporter, delays, packets, test_params)
        except Exception, e:
            print '*** Caught exception: %s: %s' % (e.__class__, e)
            traceback.print_exc()
            sys.exit(1)

    def launch_speedtest(self, params_file, urls_file):
        try:
            reporter = spreadsheetReporter.SpreadsheetReporter(self.gdocs_user,
                                                               self.gdocs_pw)
            csv_file = csv.DictReader(open(params_file,'rb'),
                                      delimiter=',',
                                      quotechar='"')
            for line in csv_file:
                self.run_speedtest(reporter, line, urls_file)
        except Exception, e:
            print '*** Caught exception: %s: %s' % (e.__class__, e)
            traceback.print_exc()
            sys.exit(1)

    def test_10MBIncreasingLatency(self):
        try:
            self.launch_speedtest('test-params-IncreasingLatency.csv',
                                  'test-urls-10MB.json')
        except Exception, e:
            print '*** Caught exception: %s: %s' % (e.__class__, e)
            traceback.print_exc()
            sys.exit(1)

    def test_10MBIncreasingLoss(self):
        try:
            launch_speedtest('test-params-IncreasingLoss.csv',
                             'test-urls-10MB.json')
        except Exception, e:
            print '*** Caught exception: %s: %s' % (e.__class__, e)
            traceback.print_exc()
            sys.exit(1)

    def test_QUIC_vs_HTTP(self):
        test_10MBIncreasingLatency()
        test_10MBIncreasingLoss()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
