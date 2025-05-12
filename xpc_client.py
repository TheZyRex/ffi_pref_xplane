import xpc

import sys
import struct

import socket



def monitor():

    global counter
    counter = 0
    with xpc.XPlaneConnect() as client:
        print("Starting Receiv")

        message, address = serverSocket.recvfrom(1024)
        print(message)
        while True:


            posi = client.getPOSI();

            #serverSocket.sendto("Loc: (%4f, %4f, %4f) Attitude (P %4f) (R %4f) (Y %4f)\n"\
            # % (posi[0], posi[1], posi[2], posi[3] , posi[4], posi[5], 127.0.0.1, 45682)
            lat = str(posi[0])
            lon = str(posi[1])
            alt = str(posi[2])
            hdg = str(posi[5])
            data = (str(counter) + "," + lat + "," + lon + "," + alt + ","  + hdg)
            serverSocket.sendto( data.encode('utf-8') , ("127.0.0.1",45682))
            counter = counter +1 
            autopilot_state = client.getDREF("sim/cockpit/autopilot/autopilot_state")
            
            print("AP_State: %d", autopilot_state)
            
            byte_conv = hex(int(autopilot_state[0]))
            print("AP state byte conversion:", byte_conv)
            
            nav_steer_deg_mag_read = client.getDREF("sim/cockpit/autopilot/nav_steer_deg_mag")
            print("Nav steer info:", int(nav_steer_deg_mag_read[0]))


if __name__ == "__main__":


    dref1 = "sim/cockpit/autopilot/nav_steer_deg_mag"
    dref2 = "sim/cockpit/autopilot/autopilot_state"

  

    # Setup
    client = xpc.XPlaneConnect()

    # Execute
    # client.sendDREF(dref2, 0x0)
    
    
    # value = 512+16384
    value = 512
    
    client.sendDREF(dref1, 150.0)
    client.sendDREF(dref2, value)
    
    # Cleanup
    client.close()

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(("127.0.0.1", 45683))
    
    monitor()