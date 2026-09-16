if(env.OS_Info == "windows") {
    println("Pipeline Json Analysis")
    powershell "poetry run req-val validate-pipeline-json"

    println("Configuration Analysis")
    powershell "poetry run req-val validate-alternative-configuration-files configurations"

    println("Static Code Analysis")
    powershell "poetry run flake8 tests"
    powershell "poetry run isort tests --check-only --diff"
} else {
    println("Pipeline Json Analysis")
    sh """
        set +x
        source /opt/.virtualenvs/mason/bin/activate
        req-val validate-pipeline-json
    """

    println("Configuration Analysis")
    sh """
        set +x
        source /opt/.virtualenvs/mason/bin/activate
        req-val validate-alternative-configuration-files configurations
    """

    println("Static Code Analysis")
    sh """
        set +x
        source /opt/.virtualenvs/mason/bin/activate
        flake8 tests
        isort tests --check-only --diff
    """
}
