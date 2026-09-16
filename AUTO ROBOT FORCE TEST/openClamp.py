import time 
from ur_rtde import robotiq_gripper

ROBOT_IP = "192.168.10.150"

print("Connecting to gripper...")
gripper = robotiq_gripper.RobotiqGripper() 
gripper.connect(ROBOT_IP, 63352) 

if not gripper.is_active():
    print("Activating gripper...")
    gripper.activate()
    time.sleep(1)

gripper.set_speed(255)
gripper.set_force(100)

print("Opening clamp...")
gripper.move_and_wait_for_pos(0, 255, 100)

print("Clamp is open.")
gripper.disconnect()