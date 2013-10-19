"""/* Copyright(C) 2013, OpenOSEK by Fan Wang(parai). All rights reserved.
 *
 * This file is part of OpenOSEK.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <http://www.gnu.org/licenses/>.
 *
 * Email: parai@foxmail.com
 * Sourrce Open At: https://github.com/parai/OpenOSEK/
 */
"""
from Osek import *

uds_tx_id = 0x731
uds_rx_id = 0x732
UdsAckEvent = DeclareEvent()

def UdsOnCanUsage():
    print "Usage:"
    print "\t python uds.py --port port"
    print "Example: python uds.py --port 8999"

def UdsConfig():
    global uds_tx_id, uds_rx_id
    print 'Welcome to OpenOSEK UDS client cnter!'
    value = raw_input('Please Input the UDS client Tx CAN ID(default = 0x731):')
    if('' != value):
        uds_tx_id = int(value,16)
    value = raw_input('Please Input the UDS client Rx CAN ID(default = 0x732):')
    if('' != value):
        uds_rx_id = int(value,16)
    print 'Tx = %s, Rx = %s.'%(hex(uds_tx_id),hex(uds_rx_id))

def Uds_RxIndication(data):
    cstr = '    Responce: ['
    for i in range(0,len(data)):
        cstr += '0x%-2x,'%(data[i])
    cstr += ']'
    print cstr
    SetEvent(UdsAckEvent)
 
def UdsOnCanClient(port = 8999):
    global uds_tx_id, uds_rx_id
    #UdsConfig()
    Can_Init(None,port,port-port%1000)
    CanTp_Init(Uds_RxIndication,uds_rx_id,uds_tx_id)
    while True:
        data = []
        value = raw_input("uds send [ 3E 00 ]:")
        if(value != ''):
            for chr in value.split(' '):
                try:
                    data.append(int(chr,16))
                except:
                    print 'Error input!'
                    data = [0x3e,00]
                    break
        else:
            data = [0x3e,00]
        CanTp_Transmit(data)
        if(True == WaitEvent(UdsAckEvent,1000)): 
            ClearEvent(UdsAckEvent)
        else:
            print "    No Response, Time-out."
   
def main(argc,argv):
    if(argc != 3):
        UdsOnCanUsage()
        return
    if(argv[1] == '--port'):
        UdsOnCanClient(int(argv[2]))
        
if __name__ == '__main__': 
    import sys 
    main(len(sys.argv),sys.argv);
