if (isUnix()) {
    sh "git clean -xd --exclude=.venv --force --quiet"
} else {
    bat "git config --local core.longpaths true && git clean -xd --exclude=.venv --force --quiet"
}
