import rtde_control
import rtde_receive
import time
import csv
import math
from datetime import datetime

# ─── CONFIG ────────────────────────────────────────────────────────────────────
ROBOT_IP = "192.168.10.150"

# Where the robot should go when you stop the script (Ctrl+C)
START_POSE = [-0.2604866596529446, -0.36679744543598714, -0.12957999685938806,
              -0.029450542646150164, 2.757024635335865, 1.4293589125080717]

# Your actual “push/contact” pose
APPROACH_POSE = [-0.2420830581542962, -0.12966542109655, -0.22377464882260667,
                 0.032291920989683864, 2.4818711242426796, 1.781441807827078]

PUSH_FORCE       = 10.0
FORCE_PLANE      = "YZ"
TEST_ANGLES_DEG  = [30, 43, 57, 70]

SAMPLES_PER_PUSH = 100
SAMPLE_RATE      = 0.01
TARE_SAMPLES     = 50

OUTPUT_CSV = f"knob_test_results_{datetime.now().strftime('%H%M%S')}.csv"
# ───────────────────────────────────────────────────────────────────────────────

def connect():
    print(f"Connecting to {ROBOT_IP}...")
    rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
    rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)
    return rtde_c, rtde_r

def set_tare(rtde_r):
    """Measures the 'empty' weight of the tool at this pose."""
    print("  [TARE] Measuring tool weight bias...")
    samples = []
    for _ in range(TARE_SAMPLES):
        samples.append(rtde_r.getActualTCPForce())
        time.sleep(SAMPLE_RATE)
    bias = [sum(axis) / len(samples) for axis in zip(*samples)]
    print(f"  [TARE] Bias: Fx={bias[0]:.1f} Fy={bias[1]:.1f} Fz={bias[2]:.1f}")
    return bias

def calculate_wrench(angle_deg, magnitude):
    rad = math.radians(angle_deg)
    # YZ plane: 0° = +Y, 90° = +Z
    return [0.0, magnitude * math.cos(rad), magnitude * math.sin(rad), 0.0, 0.0, 0.0]

def run_test(rtde_c, rtde_r, angle, writer):
    print(f"\n▶ STARTING TEST: {angle}°")

    rtde_c.moveL(APPROACH_POSE, speed=0.05, acceleration=0.2)
    time.sleep(1.0)

    bias = set_tare(rtde_r)

    wrench = calculate_wrench(angle, PUSH_FORCE)
    selection = [0, 1, 1, 0, 0, 0]  # control Fy and Fz
    limits = [0.1, 0.1, 0.1, 0.5, 0.5, 0.5]

    print(f"  Pushing with {PUSH_FORCE}N at {angle}°...")
    rtde_c.forceMode([0, 0, 0, 0, 0, 0], selection, wrench, 2, limits)

    for i in range(SAMPLES_PER_PUSH):
        raw = rtde_r.getActualTCPForce()
        pose = rtde_r.getActualTCPPose()

        writer.writerow([
            angle, i,
            round(raw[0] - bias[0], 3),
            round(raw[1] - bias[1], 3),
            round(raw[2] - bias[2], 3),
            round(pose[0], 5), round(pose[1], 5), round(pose[2], 5)
        ])
        time.sleep(SAMPLE_RATE)

    rtde_c.forceModeStop()
    print("  Done. (stopped force mode)")

def safe_shutdown(ctrl, recv, go_pose=None):
    """Stop force mode, optionally move, then disconnect."""
    if ctrl is not None:
        try:
            ctrl.forceModeStop()
        except:
            pass
        if go_pose is not None:
            try:
                print(f"\n[SAFE EXIT] Moving to START_POSE: {go_pose}")
                ctrl.moveL(go_pose, speed=0.05, acceleration=0.2)
            except Exception as e:
                print(f"[SAFE EXIT] Could not move to START_POSE: {e}")
        try:
            ctrl.disconnect()
        except:
            pass

    if recv is not None:
        try:
            recv.disconnect()
        except:
            pass

    print("[SAFE EXIT] Disconnected from robot.")

def main():
    ctrl = None
    recv = None
    interrupted = False

    try:
        ctrl, recv = connect()

        with open(OUTPUT_CSV, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["angle", "sample", "net_Fx", "net_Fy", "net_Fz", "x", "y", "z"])

            for deg in TEST_ANGLES_DEG:
                run_test(ctrl, recv, deg, w)

        print(f"\n✨ ALL TESTS COMPLETE! File saved as: {OUTPUT_CSV}")

    except KeyboardInterrupt:
        interrupted = True
        print("\n[INTERRUPT] Ctrl+C received. Going to START_POSE then disconnecting...")

    finally:
        # Only go to START_POSE when you kill the run (Ctrl+C)
        safe_shutdown(ctrl, recv, go_pose=START_POSE if interrupted else None)

if __name__ == "__main__":
    main()