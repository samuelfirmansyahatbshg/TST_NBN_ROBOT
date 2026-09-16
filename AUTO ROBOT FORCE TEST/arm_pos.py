import rtde_receive
import rtde_control

ROBOT_IP = "192.168.10.150"

rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)
rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)

pose = rtde_r.getActualTCPPose()
print(f"KNOB_POSE = {pose}")

APPROACH_POSE = [-0.2604866596529446, -0.36679744543598714, -0.12957999685938806, -0.029450542646150164, 2.757024635335865, 1.4293589125080717] # start pos

# Quick safety test
#rtde_c.moveL(APPROACH_POSE, speed=0.15)

rtde_r.disconnect()
rtde_c.disconnect()
print("Disconnected from robot.")
#  [x, Y, Z, RX, RY, RZ]
# [-248.90, -287.00, -570.40, 0.031, -2.642, -1.812]   <-- starting position
#