if(env.OS_Info == "windows") {
    powershell "poetry env use python"
    powershell "poetry check"            // Check pyproject.toml
    try {
        powershell "poetry check --lock"     // Check consistency of pyproject.toml and poetry.lock
    } catch (poetry_lock_error) {
        if(pBranch == "PLAYGROUND") {
            println "WARNING: Poetry lockfile problem: ${poetry_lock_error}"
        } else {
            error "Poetry lockfile problem: ${poetry_lock_error}"
        }
    }
    powershell "poetry install --sync --no-ansi"
} else {
    sh """
        set +x
        source /opt/.virtualenvs/mason/bin/activate
        pip3 list
    """
}
