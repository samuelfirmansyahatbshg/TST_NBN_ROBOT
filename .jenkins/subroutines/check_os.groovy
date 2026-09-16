if (isUnix()) {
    os_map = ['x86_64':'linux', 'aarch64':'raspi']
    uname  = sh(returnStdout: true, script: 'uname -p').trim().toLowerCase()
    println "Architecture: " + uname
    env.OS_Info = os_map[uname]
}
else {
    env.OS_Info = "windows"
}