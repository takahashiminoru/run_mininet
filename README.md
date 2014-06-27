This repository is for advanced run_mininet.py (https://github.com/osrg/ryu/blob/master/ryu/tests/switch/run_mininet.py) .

- Enable using two different switches
- Add support for LINC Switch

Mininet that supports LINC Switch is here:

  https://github.com/FlowForwarding/mininet

usage)

  to use Open vSwitch as tester_sw and use LINC Switch as target_sw:

    sudo ryu/tests/switch/run_mininet.py --tester ovs --target linc

"switch" option is overwritten by "tester" and "target".
