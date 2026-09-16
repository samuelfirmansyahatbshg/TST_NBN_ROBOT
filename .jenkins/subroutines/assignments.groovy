switch (JOB_NAME) {
    case ~/.*[\\\/]DEVELOP[\\\/].*/:
        pBranch = "DEVELOP"
        break
    case ~/.*[\\\/]MASTER[\\\/].*/:
        pBranch = "MASTER"
        break
    case ~/.*[\\\/]PLAYGROUND[\\\/].*/:
        pBranch = "PLAYGROUND"
        break
    case ~/.*[\\\/]EXPERIMENTAL[\\\/].*/:
        pBranch = "EXPERIMENTAL"
        break
    case ~/.*[\\\/]PULL_REQUEST_CHECKER.*/:
        pBranch = "PULL_REQUEST_CHECKER"
        break
    case ~/.*[\\\/]docker_images[\\\/].*/:
        pBranch = "DOCKER_IMAGES"
        break
    default:
        error("Undefined trigger type!")
        break
}
println "Branch: " + pBranch
env.pBranch = pBranch

pPipelineInfo = readJSON file: '.jenkins/pipeline.json', returnPojo: true
pDevicesUnderTestTable = pPipelineInfo["variant_specific"]
pProjectSpecificTable = pPipelineInfo["project_specific"]
if ("bdc_artifactory" in pProjectSpecificTable) {
    pArtifactoryTable = pProjectSpecificTable["bdc_artifactory"]
}
else {
    pArtifactoryTable = pProjectSpecificTable["brsdd_artifactory"]
}
