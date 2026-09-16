def harvest() {
    pArtifacts = readJSON file: pHarvestingConfiguration, returnPojo: false
    pArtifacts.each { source, artifacts ->
        println source
        println artifacts
        prependToFile file: 'cfg.json', content: artifacts.toString()
        env.pUser = ''
        env.pPassword = ''
        if (pProjectSpecificTable[source]['credentials_type'] == 'token') {
            withCredentials([string(credentialsId: pProjectSpecificTable[source]["credentials_id"], variable: 'token')]) {
                env.pUser = pProjectSpecificTable[source]['user']
                env.pPassword = token
            }
        }
        else if (pProjectSpecificTable[source]['credentials_type'] == 'user_and_password') {
            withCredentials([usernamePassword(credentialsId: pProjectSpecificTable[source]["credentials_id"], passwordVariable: 'password', usernameVariable: 'user')]) {
                env.pUser = user
                env.pPassword = password
            }
        }
        else {
            println 'Could not download artifactory because the credential_type is not defined for ' + source
        }
        if(env.OS_Info == "windows") {
            powershell '''
                Set-Item -Path env:PYTHONUNBUFFERED -Value true
                poetry run artifact-harvester --reruns $Env:pReruns --build_name $Env:pBuildInfoName --build_number $Env:pBuildInfoNumber --user $Env:pUser --password $Env:pPassword
            '''
        } else if(env.OS_Info == "linux") {
            sh '''
                set +x
                source /opt/.virtualenvs/mason/bin/activate
                artifact-harvester --reruns ${pReruns} --build_name ${pBuildInfoName} --build_number ${pBuildInfoNumber} --user ${pUser} --password ${pPassword}
            '''
        } else {
            // os = raspi
            sh '''
                set +x
                source /opt/.virtualenvs/mason/bin/activate
                artifact-harvester --reruns ${pReruns} --build_name ${pBuildInfoName} --build_number ${pBuildInfoNumber} --no_cli --user ${pUser} --password ${pPassword}
            '''
        }
    }
}

if (pDevicesUnderTestTable[pDeviceUnderTest]["features"]["artifact_harvesting_tries"] > 0) {
    env.pReruns = pDevicesUnderTestTable[pDeviceUnderTest]["features"]["artifact_harvesting_tries"]
    harvest()
    if(pDevicesUnderTestTable[pDeviceUnderTest]["features"]["sose_handling"] && pBranch == "MASTER") {
        if(env.OS_Info == "windows") {
            powershell '''
                Copy-Item (get-item $Env:pConfigurationSose) -Destination "cfg_sose.json"
                Copy-Item $Env:pConfigurationSupported -Destination "cfg_supported.json"
                poetry run artifact-harvester --sose_conversion_only
            '''
        }
        else if(env.OS_Info == "linux") {
            sh '''
                set +x
                source /opt/.virtualenvs/mason/bin/activate
                cp $Env:pConfigurationSose "cfg_sose.json"
                cp $Env:pConfigurationSupported "cfg_supported.json"
                artifact-harvester --sose_conversion_only
            '''
        } else {
            // os = raspi
            sh '''
                set +x
                source /opt/.virtualenvs/mason/bin/activate
                cp $Env:pConfigurationSose "cfg_sose.json"
                cp $Env:pConfigurationSupported "cfg_supported.json"
                artifact-harvester --sose_conversion_only
            '''
        }
        pHarvestingConfiguration = "cfg_sose_created.json"
        harvest()
    }
}