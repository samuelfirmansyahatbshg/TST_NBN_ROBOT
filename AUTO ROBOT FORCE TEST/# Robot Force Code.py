# Robot Force Code
import rtde_control
import rtde_receive
import time
import math

#--------------------------------------------------------------------
# ROBOT CONNECTION
#--------------------------------------------------------------------

ROBOT_IP = "192.168.10.150" #Robot IP ADDRESS Need

rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)

#--------------------------------------------------------------------
# USER SETTINGS
#--------------------------------------------------------------------

# Knob position [x, y, z, Rx, Ry, Rz] in meters & radians
KNOB_POSE = [.300, -.200, 0.150, 2.221, -2.221, 0.0]

# How far above/behind the knob to start the approach (in meters)
APPROACH_OFFSET = 0.08 #8 cm back from knob along push direction

# Push force in Newtons (increase/decrease as needed)
PUSH_FORCE = 10.0 

# How far to push in (meters)
PUSH_DISTANCE = 0.03 # 3 cm push

# Speed and acceleration
SPEED   = 0.05          # m/s
ACCEL   = 0.3           # m/s^2

# Force control task frame & settings
# Push direction: 45 Degrees from top (z) and 45 Degrees from side (Y)
# Direction vector [Fx, Fy, Fz, TRx, TRy, TRz]
angle_rad = math.radians(45)
PUSH_DIRECTION = [
    0.0,            # No force in X
    round(math.sin(angle_rad), 4),      # Y component (side 45 degrees)
    -round(math.cos(angle_rad), 4),     # Z component (downward 45 degrees)
    0.0,
    0.0,
    0.0 
]

#--------------------------------------------------------------------
# Home / Ready Position (joint angles in radians)
# These are safe upright positions - adjust if needed
#--------------------------------------------------------------------

HOME_JOINTS= [
    math.radians(0),    # Base
    math.radians(-90),  # Shoulder
    math.radians(90),   # Elbow
    math.radians(-90),  # Wrist 1
    math.radians(-90),  # Wrist 2
    math.radians(0)     # Wrist 3
]

#--------------------------------------------------------------------
# HELPER: Calculate approach pose offset
# Offsets the knob pose backwards along push direction
#--------------------------------------------------------------------

def get_approach_pose(knob_pose, offset, direction):
    approach = list(knob_pose)
    approach[0] -= direction[0] * offset # X
    approach[1] -= direction[1] * offset # Y
    approach[2] -= direction[2] * offset # Z (negative = move up/back)
    return approach

#--------------------------------------------------------------------
# MAIN SEQUENCE
#--------------------------------------------------------------------

def main():
    print("=== UR10e Oven Knob Push Sequence ===")

    # --- Step 1: Move to Home Position ---
    print("[1/5] Moving to home position...")
    rtde_c.moveJ(HOME_JOINTS, speed=0.5, acceleration=0.5)
    time.sleep(1)

    # --- Step 2: Move to Approach Position ---
    print("[2/5] Moving to approach position...")
    approach_pose = get_approach_pose(KNOB_POSE, APPROACH_OFFSET, PUSH_DIRECTION)
    rtde_c.moveL(approach_pose, speed=SPEED, acceleration=ACCEL)
    time.sleep(0.5)

    # --- Step 3: Force-Controlled Push ---
    print("[3/5] Pushing nob with {PUSH_FORCE}N force at 45/45 degree angle...")

    # Task frame: identity (world frame)
    task_frame = [0, 0, 0, 0, 0, 0]

    # Which axes are force-controlled (1) vs position-controlled (0)
    # [x,Y, Z, Rx, Ry, Rz] - control force on Y and Z (push direction)
    selection_vector = [0, 1, 1, 0, 0, 0]

    # Wrench: desired force along push direction
    wrench = [
        0.0,                                    # Fx
        PUSH_FORCE * math.sin(angle_rad),       # Fy
        -PUSH_FORCE * math.cos(angle_rad),      # Fz
        0.0,                                    # Tx
        0.0,                                    # Ty 
        0.0                                     # Tz
    ]

    # Type 2 = force control in tool frame
    force_type = 2
    limits = [0.1, 0.1, 0.1, 0.5, 0.5, 0.5]     # Max speed limits during force control

    rtde_c.forceMode(task_frame, selection_vector, wrench, force_type, limits)

    # Let it push for a set duration (seconds)
    PUSH_DIRECTION = 2.0    # Adjust how long it pushes
    time.sleep(PUSH_DIRECTION)

    #stop force mode
    rtde_c.forceModeStop()
    print("[3/5] Push comlete.")
    time.sleep(0.5)

    # --- Step 4: Retract back to approach position ---
    print("[4/5] Retracting...")
    rtde_c.moveL(approach_pose, speed=SPEED, acceleration=ACCEL)
    time.sleep(0.5)

    # --- Step 5: Return to Home ---
    print("[5/5] Returning to home position...")
    rtde_c.moveJ(HOME_JOINTS, speed=0.5, acceleration=0.5)

    print("=== Sequence Complete ===")

#--------------------------------------------------------------------
# RUN
#--------------------------------------------------------------------
if name == "_main_":
    try:
        main()
    except KeyboardInterrupt:
        print("|n[!] Interrupted by user")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        rtde_c.stopScript()
        rtde_c.disconnect()
        print("Robot script stopped safely.")

