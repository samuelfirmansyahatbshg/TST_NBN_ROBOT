"""
COPYRIGHT © BSH HOME APPLIANCES GROUP 2022

ALL RIGHTS RESERVED.

The reproduction, transmission or use of this document or its contents is not permitted without express
written authority. Offenders will be liable for damages. All rights, including rights created by patent
grant or registration of a utility model or design, are reserved.
"""

if __name__ == "__main__":
    import os
    import subprocess
    import sys

    ############################
    # CONFIGURE THE HOOK HERE: #
    ############################
    POSSIBLE_CHECKS = (
        FLAKE8 := "FLAKE8",
        ISORT := "ISORT",
        REQVAL_ALTERNATIVE_CONFIGURATIONS := "REQVAL_ALTERNATIVE_CONFIGURATIONS",
        REQVAL_PIPELINE_JSON := "REQVAL_PIPELINE_JSON",
    )
    ENABLED = (
        FLAKE8,
        ISORT,
        REQVAL_ALTERNATIVE_CONFIGURATIONS,
        # REQVAL_PIPELINE_JSON,
    )

    #############
    # HOOK VARS #
    #############
    cwd = os.getcwd()
    run_silent = {"cwd": cwd, "stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
    run_captured = {"cwd": cwd, "capture_output": True, "encoding": "utf-8"}

    def get_diff():
        """
        Git provides a list of changed files via the git diff command, cf. https://git-scm.com/docs/git-diff for details
        For the hook, currently only Python files are relevant
        """
        try:
            sp = subprocess.run(
                ["git", "diff", "--diff-filter=d", "--staged", "--name-only", "-z"],
                check=True,
                encoding="utf-8",
                **run_silent,
            )  # >>> stdout of this command is NUL separated (\x00) relative paths to staged files.
            files = [
                f
                for f in sp.stdout.split("\x00")
                if f and (f.endswith(".py") or f.endswith(".pyi"))  # 'f' is not empty and ends with .pyi or .py
            ]
            for i in range(len(files)):
                if sys.platform == "win32":
                    files[i] = files[i].replace("/", "\\")
            return files
        except subprocess.CalledProcessError:
            print("Problem running pre-commit hook: Could not read git diff")

    def run_checks(files):
        """
        - Run checks that are in the ENABLED tuple (formatters before linters and checks)
        - Print user-friendly message(s)
        - Exit with the correct code
            - 0 if formatters changed nothing and checks successful -> Commit successful
            - 1 if formatters changed files and checks successful -> User simply has to commit again
            - 2 if checks unsuccessful -> User has to do manual work
        """
        did_autoformat = False
        need_manual_fix = False
        ################
        # PYTHON FILES #
        ################
        files_isort = []
        for file in files:
            if not file.endswith("conftest.py"):
                files_isort.append(file)
        if files:
            print("Python files changed, running checks.")
            # Formatting:
            if ISORT in ENABLED and files_isort:
                sp_isort = subprocess.run(["isort", *files_isort, "--check-only"], **run_silent)
                if sp_isort.returncode:
                    did_autoformat = True
                    print("Auto-correcting import order...")
                    subprocess.run(["isort", *files_isort], **run_silent)
            # Linting:
            if FLAKE8 in ENABLED:
                sp_flake8 = subprocess.run(["flake8", *files], **run_captured)
                if sp_flake8.returncode:
                    need_manual_fix = True
                    print("[ERROR]: flake8 style")
                    print(sp_flake8.stdout)
                    if sp_flake8.stderr:
                        print(sp_flake8.stderr)
        ##################
        # REQ-VAL CHECKS #
        ##################
        if REQVAL_ALTERNATIVE_CONFIGURATIONS in ENABLED:
            sp_req_val = subprocess.run(
                ["req-val", "validate-alternative-configuration-files", "configurations"], **run_captured)
            if sp_req_val.returncode:
                need_manual_fix = True
                print("[ERROR]: alternative configurations")
                print(sp_req_val.stdout)
        if REQVAL_PIPELINE_JSON in ENABLED:
            sp_req_val = subprocess.run(["req-val", "validate-pipeline-json"], **run_captured)
            if sp_req_val.returncode:
                need_manual_fix = True
                print("[ERROR]: .jenkins/pipeline.json")
                print(sp_req_val.stdout)
        #################
        # EXIT HANDLING #
        #################
        if need_manual_fix:
            print("Please resolve the errors above manually.")
            sys.exit(2)
        else:
            if did_autoformat:
                print("Looks good! Please try committing again.")
                sys.exit(1)
            else:
                print("Looks good!")
                sys.exit(0)

    staged = get_diff()
    run_checks(staged)
