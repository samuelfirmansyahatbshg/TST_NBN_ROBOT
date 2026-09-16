import rtde_control
import rtde_receive
import time
import csv
from datetime import datetime

ROBOT_IP = "192.168.10.150"

# Center of Knob/Axis: [-0.2213792683328537, -0.10876927960020988, -0.21162695758718023, -0.08123428879697865, 2.569427477581583, 1.7249871538099697]


START_POSE = [-0.2604866596529446, -0.36679744543598714, -0.12957999685938806, -0.029450542646150164, 2.757024635335865, 1.4293589125080717]

# CHANGE
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
APPROACH_POSES = [

    # COPY PASTE CO-ORDINATE FROM ARM_POS.PY FILE  
    [-0.22482923851026687, -0.1701012603748267, -0.225693356589459, 0.355174060060583, 2.0767237743511604, 1.8153984024383043]

]

PUSH_FORCE    = 17  # PUSH FORCE - Newtons
MAX_TRAVEL    = 0.003 # PUSH TRAVEL - M
PUSH_DURATION = 2.5   # PUSH DURATION - seconds

#------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---- Data recording settings (added) ----
RECORD_DURING_FORCE = True     # set False if you only want before/after rows
SAMPLE_PERIOD_SEC   = 0.10     # sample every 0.10s during force
run_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
CSV_FILENAME = f"force_test_log_{run_stamp}.csv"
# ----------------------------------------

rtde_c = None
rtde_r = None

def log_row(writer, test_index, phase):
    """Record current TCP pose + TCP force (added)."""
    pose = rtde_r.getActualTCPPose()     # [x,y,z,rx,ry,rz]
    force = rtde_r.getActualTCPForce()   # [Fx,Fy,Fz,Mx,My,Mz]
    writer.writerow({
        "pc_timestamp_iso": datetime.now().isoformat(timespec="milliseconds"),
        "test_index": test_index,
        "phase": phase,
        "tcp_x": pose[0], "tcp_y": pose[1], "tcp_z": pose[2],
        "tcp_rx": pose[3], "tcp_ry": pose[4], "tcp_rz": pose[5],
        "fx": force[0], "fy": force[1], "fz": force[2],
        "mx": force[3], "my": force[4], "mz": force[5],
    })

try:
    rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
    rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

    # Open CSV once for the whole run (added)
    with open(CSV_FILENAME, "w", newline="") as f:
        fieldnames = [
            "pc_timestamp_iso", "test_index", "phase",
            "tcp_x", "tcp_y", "tcp_z", "tcp_rx", "tcp_ry", "tcp_rz",
            "fx", "fy", "fz", "mx", "my", "mz",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        f.flush()

        print("Moving to START_POSE (home)...")
        rtde_c.moveL(START_POSE, speed=0.1, acceleration=0.3)

        for idx, APPROACH_POSE in enumerate(APPROACH_POSES):
            print(f"\n[Test {idx+1}/{len(APPROACH_POSES)}] → Moving to START_POSE...")
            rtde_c.moveL(START_POSE, speed=0.1, acceleration=0.3)

            print(f"  Moving to APPROACH_POSE...")
            rtde_c.moveL(APPROACH_POSE, speed=0.1, acceleration=0.3)
            time.sleep(0.5)

            # Log right before force mode (added)
            log_row(writer, idx, "before_force")
            f.flush()

            print(f"  Pushing with {PUSH_FORCE}N (max {MAX_TRAVEL*1000:.0f}mm) along tool Z...")
            task_frame = [0, 0, 0, 0, 0, 0]
            selection  = [0, 0, 1, 0, 0, 0]
            wrench     = [0, 0, PUSH_FORCE, 0, 0, 0]
            f_type     = 1
            limits     = [0.1, 0.1, MAX_TRAVEL, 0.5, 0.5, 0.5]

            rtde_c.forceMode(task_frame, selection, wrench, f_type, limits)

            if RECORD_DURING_FORCE:
                t0 = time.time()
                while (time.time() - t0) < PUSH_DURATION:
                    log_row(writer, idx, "during_force")
                    f.flush()
                    time.sleep(SAMPLE_PERIOD_SEC)
            else:
                time.sleep(PUSH_DURATION)

            rtde_c.forceModeStop()
            print("  Push complete. Retracting...")

            # Log right after force mode stop (added)
            log_row(writer, idx, "after_force")
            f.flush()

            rtde_c.moveL(APPROACH_POSE, speed=0.1, acceleration=0.3)

        print("\n✅ All tests completed. Returning to START_POSE...")
        rtde_c.moveL(START_POSE, speed=0.1, acceleration=0.3)
        print("✔️ Done.")
        print(f"Data saved to: {CSV_FILENAME}")

except KeyboardInterrupt:
    print("\n🛑 INTERRUPT: Ctrl+C received. Stopping force mode and returning to START_POSE...")
    try:
        rtde_c.forceModeStop()
    except:
        pass
    try:
        rtde_c.moveL(START_POSE, speed=0.1, acceleration=0.3)
        print("🏠 [SAFE EXIT] Returned to START_POSE.")
    except Exception as e:
        print(f"❌ [SAFE EXIT] Could not return to START_POSE: {e}")

finally:
    if rtde_c is not None:
        rtde_c.disconnect()
    if rtde_r is not None:
        rtde_r.disconnect()
    print("🔌 [SAFE EXIT] Disconnected.")