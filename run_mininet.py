#!/usr/bin/env python

import sys

from mininet.cli import CLI
from mininet.link import Link
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import OVSSwitch
from mininet.node import UserSwitch
from mininet.term import makeTerm

try:
    from mininet.node import LincSwitch
    ENABLE_LINC = True
except Exception:
    ENABLE_LINC = False

from oslo.config import cfg
from ryu import version

if '__main__' == __name__:

    switch_type = {'ovs': OVSSwitch, 'ovsk': OVSSwitch, 'cpqd': UserSwitch}
    linc_str = ''
    if ENABLE_LINC == True:
        linc_str = '|linc'
        switch_type['linc'] = LincSwitch
    opts = [
        cfg.StrOpt('tester', default='ovs',
            help='tester switch [ovs|ovsk|cpqd%s] (default: ovs)' % linc_str),
        cfg.StrOpt('target', default='ovs',
            help='target switch [ovs|ovsk|cpqd%s] (default: ovs)' % linc_str)
    ]
    conf = cfg.ConfigOpts()
    conf.register_cli_opts(opts)
    conf(project='ryu', version='run_mininet.py %s' % version)
    conf(sys.argv[1:])
    tester = switch_type.get(conf.tester)
    if tester is None:
        print "Invalid tester switch type. [%s]" % conf.tester
        sys.exit(-1)
    target = switch_type.get(conf.target)
    if target is None:
        print "Invalid target switch type. [%s]" % conf.target
        sys.exit(-1)

    net = Mininet(controller=RemoteController)

    c0 = net.addController('c0')

    kwargs = {}
    if conf.target == 'ovs':
        kwargs['datapath'] = 'user'
    s1 = net.addSwitch('s1', cls=target, listenPort=6634, dpopts='', **kwargs)
    kwargs = {}
    if conf.tester == 'ovs':
        kwargs['datapath'] = 'user'
    s2 = net.addSwitch('s2', cls=tester, listenPort=6635, dpopts='', **kwargs)

    Link(s1, s2)
    Link(s1, s2)
    Link(s1, s2)

    net.build()
    c0.start()
    s1.start([c0])
    s2.start([c0])

    if conf.target.startswith('ovs'):
        s1.cmd('ovs-vsctl set Bridge s1 protocols=OpenFlow13')
    if conf.tester.startswith('ovs'):
        s2.cmd('ovs-vsctl set Bridge s2 protocols=OpenFlow13')

    s1.cmd('ifconfig s1-eth1 -multicast')
    s1.cmd('ifconfig s1-eth2 -multicast')
    s1.cmd('ifconfig s1-eth2 -multicast')
    s2.cmd('ifconfig s2-eth1 -multicast')
    s2.cmd('ifconfig s2-eth2 -multicast')
    s2.cmd('ifconfig s2-eth3 -multicast')

    CLI(net)

    net.stop()
