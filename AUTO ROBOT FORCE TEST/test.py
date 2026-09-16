import rtde_receive

rtde_r = rtde_receive.RTDEReceiveInterface("192.168.10.150")

print(rtde_r.getDigitalOutState())