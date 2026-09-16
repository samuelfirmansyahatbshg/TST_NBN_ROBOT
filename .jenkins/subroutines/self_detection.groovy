switch (JOB_NAME) {
    case ~/.*[\\\/]SMOKE[\\\/].*/:
        pIntensity = "SMOKE"
        break
    case ~/.*[\\\/]OVERNIGHT[\\\/].*/:
        pIntensity = "OVERNIGHT"
        break
    case ~/.*[\\\/]WEEKEND[\\\/].*/:
        pIntensity = "WEEKEND"
        break
    case ~/.*[\\\/]COMPLETE[\\\/].*/:
        pIntensity = "COMPLETE"
        break
    case ~/.*[\\\/]PLAYGROUND[\\\/].*/:
        pIntensity = "PLAYGROUND"
        break
    case ~/.*[\\\/]EXPERIMENTAL[\\\/].*/:
        pIntensity = "EXPERIMENTAL"
        break
    case ~/.*[\\\/]MASTER[\\\/].*/:
        pIntensity = "MASTER"
        break
    default:
        pIntensity = "UNASSIGNED"
        break
}
println "Intensity: " + pIntensity
env.pIntensity = pIntensity

switch (JOB_NAME) {
    case ~/.*[\\\/]FUNCTIONAL[\\\/].*/:
        pTestType = "FUNCTIONAL"
        break
    case ~/.*[\\\/]STRESS[\\\/].*/:
        pTestType = "STRESS"
        break
    case ~/.*[\\\/]ROBUSTNESS[\\\/].*/:
        pTestType = "ROBUSTNESS"
        break
    case ~/.*[\\\/]EXPERIMENTAL[\\\/].*/:
        pTestType = "EXPERIMENTAL"
        break
    default:
        pTestType = "UNASSIGNED"
        break
}
println "Test Type: " + pTestType
env.pTestType = pTestType

switch (JOB_NAME) {
    case ~/.*[\\\/]RUNABLE[\\\/].*/:
        pStatus = "RUNABLE"
        break
    case ~/.*[\\\/]BUGS[\\\/].*/:
        pStatus = "BUGS"
        break
    case ~/.*[\\\/]BROKEN[\\\/].*/:
        pStatus = "BROKEN"
        break
    default:
        pStatus = "UNASSIGNED"
        break
}
println "Status: " + pStatus
env.pStatus = pStatus

pDeviceUnderTest = JOB_NAME.split('/').last().trim()
println "Device Under Test: " + pDeviceUnderTest
env.pDeviceUnderTest = pDeviceUnderTest

switch (pBranch) {
    case "DEVELOP":
        switch (pIntensity) {
            case "OVERNIGHT":
                pHarvestingConfiguration = "configurations//artifacts//develop//overnight//" + pDeviceUnderTest + ".json"
                break
            case "WEEKEND":
                pHarvestingConfiguration = "configurations//artifacts//develop//overnight//" + pDeviceUnderTest + ".json"
                break
            case "SMOKE":
                pHarvestingConfiguration = "configurations//artifacts//develop//smoke//" + pDeviceUnderTest + ".json"
                break
            }
        break
    case "MASTER":
        pHarvestingConfiguration = "configurations//artifacts//master//classic//" + pDeviceUnderTest + ".json"
        pConfigurationSose = "firmwares//SOSE//*.json"
        pConfigurationSupported = "configurations//artifacts//master//sose//supported//" + pDeviceUnderTest + ".json"
        break
    case "PLAYGROUND":
        pHarvestingConfiguration = "configurations//artifacts//develop//overnight//" + pDeviceUnderTest + ".json"
        break
    case "EXPERIMENTAL":
        pHarvestingConfiguration = "configurations//artifacts//experimental//" + pDeviceUnderTest + ".json"
        break
    default:
        error("Undefined harvesting configuration!")
        break
}
println "Harvesting Configuration: " + pHarvestingConfiguration
env.pHarvestingConfiguration = pHarvestingConfiguration
if(pDevicesUnderTestTable[pDeviceUnderTest]["features"]["sose_handling"] && pBranch == "MASTER") {
    println "Configuration Sose: " + pConfigurationSose
    env.pConfigurationSose = pConfigurationSose
    println "Configuration Supported: " + pConfigurationSupported
    env.pConfigurationSupported = pConfigurationSupported
}

switch (pBranch) {
    case "DEVELOP":
        pFlashExecution = "y"
        break
    case "MASTER":
        pFlashExecution = "y"
        break
    case "PLAYGROUND":
        pFlashExecution = "${params.FLASH_EXECUTION}"
        break
    case "EXPERIMENTAL":
        pFlashExecution = "${params.FLASH_EXECUTION}"
        break
    default:
        error("Undefined flash execution!")
        break
}
if(env.OS_Info == "windows") {
    powershell """
        "${pFlashExecution}" | Out-File -FilePath flash_flag.txt -Encoding ASCII
    """
}
else {
    sh """
        echo "${pFlashExecution}" | tee flash_flag.txt
    """
}
println "Flashing Execution: " + pFlashExecution
env.pFlashExecution = pFlashExecution

switch (pBranch) {
    case "DEVELOP":
        pTests = "tests"
        break
    case "MASTER":
        pTests = "tests"
        break
    case "PLAYGROUND":
        pTests = "${params.TESTS}"
        break
    case "EXPERIMENTAL":
        pTests = "${params.TESTS}"
        break
    default:
        error("Undefined tests!")
        break
}
println "Tests: " + pTests
env.pTests = pTests

env.pLoggingLevel = pProjectSpecificTable["loglevel_cli"][pIntensity]
env.pLogFileLevel = pProjectSpecificTable["loglevel_file"][pIntensity]
println "Logging Level CLI: " + pLoggingLevel
println "Logging Level File: " + pLogFileLevel

pResource = pDevicesUnderTestTable[pDeviceUnderTest]["resource"] + "_${NODE_NAME}"
println "Resource: " + pResource

pBuildInfoName = env.JOB_NAME
println "Build Info Name: " + pBuildInfoName
env.pBuildInfoName = pBuildInfoName
pBuildInfoNumber = env.BUILD_NUMBER
println "Build Info Number: " + pBuildInfoNumber
env.pBuildInfoNumber = pBuildInfoNumber

pAgent = pDevicesUnderTestTable[pDeviceUnderTest]["agent"]
println pAgent
pAgentMode = false
if (pAgent.containsKey(env.pIntensity)) {
    if ((env.pStatus in pAgent[env.pIntensity]["STATUS"]) && (env.pTestType in pAgent[env.pIntensity]["TEST_TYPE"])) {
        pAgentMode = pAgent[env.pIntensity]["AGENT"]
        env.pTimeBudget = pAgent[env.pIntensity]["TIME_BUDGET"]
        println pTimeBudget
    }
}
println("Agent Mode: " + pAgentMode)

// Basic (Device Under Test)
pTestConfigurationBasicDeviceUnderTestSource = "configurations//basic//devices_under_test//" + pDeviceUnderTest + ".ini"
println "Test Configuration - Basic - Device Under Test - Source: " + pTestConfigurationBasicDeviceUnderTestSource
env.pTestConfigurationBasicDeviceUnderTestSource = pTestConfigurationBasicDeviceUnderTestSource
pTestConfigurationBasicDeviceUnderTestDestination = "BASIC_DEVICE_UNDER_TEST_" + pDeviceUnderTest + ".ini"
println "Test Configuration - Basic - Device Under Test - Destination: " + pTestConfigurationBasicDeviceUnderTestDestination
env.pTestConfigurationBasicDeviceUnderTestDestination = pTestConfigurationBasicDeviceUnderTestDestination
// Basic (Status)
switch (pStatus) {
    case "RUNABLE":
        pTestConfigurationBasicStatusSource = "configurations//basic//status//RUNABLE.ini"
        pTestConfigurationBasicStatusDestination = "BASIC_STATUS_RUNABLE.ini"
        break
    case "BUGS":
        pTestConfigurationBasicStatusSource = "configurations//basic//status//BUGS.ini"
        pTestConfigurationBasicStatusDestination = "BASIC_STATUS_BUGS.ini"
        break
    case "BROKEN":
        pTestConfigurationBasicStatusSource = "configurations//basic//status//BROKEN.ini"
        pTestConfigurationBasicStatusDestination = "BASIC_STATUS_BROKEN.ini"
        break
    default:
        if (pBranch != "MASTER") {
            pTestConfigurationBasicStatusSource = "configurations//basic//status//ALL.ini"
            pTestConfigurationBasicStatusDestination = "BASIC_STATUS_ALL.ini"
        }
        else {
            pTestConfigurationBasicStatusSource = "configurations//basic//status//RUNABLE_BUGS.ini"
            pTestConfigurationBasicStatusDestination = "BASIC_STATUS_RUNABLE_BUGS.ini"
        }
        break
}
println "Test Configuration - Basic - Status - Source: " + pTestConfigurationBasicStatusSource
env.pTestConfigurationBasicStatusSource = pTestConfigurationBasicStatusSource
println "Test Configuration - Basic - Status - Destination: " + pTestConfigurationBasicStatusDestination
env.pTestConfigurationBasicStatusDestination = pTestConfigurationBasicStatusDestination
// Basic (Intensity)
switch (JOB_NAME) {
    case ~/.*[\\\/]COMPLETE[\\\/].*/:
        pTestConfigurationBasicIntensitySource = "configurations//basic//intensity//COMPLETE.ini"
        pTestConfigurationBasicIntensityDestination = "BASIC_INTENSITY_COMPLETE.ini"
        break
    case ~/.*[\\\/]WEEKEND[\\\/].*/:
        pTestConfigurationBasicIntensitySource = "configurations//basic//intensity//WEEKEND.ini"
        pTestConfigurationBasicIntensityDestination = "BASIC_INTENSITY_WEEKEND.ini"
        break
    case ~/.*[\\\/]OVERNIGHT[\\\/].*/:
        pTestConfigurationBasicIntensitySource = "configurations//basic//intensity//OVERNIGHT.ini"
        pTestConfigurationBasicIntensityDestination = "BASIC_INTENSITY_OVERNIGHT.ini"
        break
    case ~/.*[\\\/]SMOKE[\\\/].*/:
        if (pAgentMode) {
            pTestConfigurationBasicIntensitySource = "configurations//basic//intensity//SMOKE_AGENT.ini"
        }
        else {
            pTestConfigurationBasicIntensitySource = "configurations//basic//intensity//SMOKE_CLASSIC.ini"
        }
        pTestConfigurationBasicIntensityDestination = "BASIC_INTENSITY_SMOKE.ini"
        break
    case ~/.*[\\\/]PLAYGROUND[\\\/].*/:
        pTestConfigurationBasicIntensitySource = "configurations//basic//intensity//ALL.ini"
        pTestConfigurationBasicIntensityDestination = "BASIC_INTENSITY_ALL.ini"
        break
    case ~/.*[\\\/]EXPERIMENTAL[\\\/].*/:
        pTestConfigurationBasicIntensitySource = "${params.INTENSITY}"
        pTestConfigurationBasicIntensityDestination = "BASIC_INTENSITY_EXPERIMENTAL.ini"
        break
    case ~/.*[\\\/]MASTER[\\\/].*/:
        pTestConfigurationBasicIntensitySource = "configurations//basic//intensity//ALL.ini"
        pTestConfigurationBasicIntensityDestination = "BASIC_INTENSITY_ALL.ini"
        break
    default:
        error("Undefined test configuration (basic intensity)!")
        break
}
println "Test Configuration - Basic - Intensity - Source: " + pTestConfigurationBasicIntensitySource
env.pTestConfigurationBasicIntensitySource = pTestConfigurationBasicIntensitySource
println "Test Configuration - Basic - Intensity - Destination: " + pTestConfigurationBasicIntensityDestination
env.pTestConfigurationBasicIntensityDestination = pTestConfigurationBasicIntensityDestination
// Basic (Test Type)
switch (pTestType) {
    case "FUNCTIONAL":
        pTestConfigurationBasicTestTypeSource = "configurations//basic//test_type//FUNCTIONAL.ini"
        pTestConfigurationBasicTestTypeDestination = "BASIC_TEST_TYPE_FUNCTIONAL.ini"
        break
    case "STRESS":
        pTestConfigurationBasicTestTypeSource = "configurations//basic//test_type//STRESS.ini"
        pTestConfigurationBasicTestTypeDestination = "BASIC_TEST_TYPE_STRESS.ini"
        break
    case "ROBUSTNESS":
        pTestConfigurationBasicTestTypeSource = "configurations//basic//test_type//ROBUSTNESS.ini"
        pTestConfigurationBasicTestTypeDestination = "BASIC_TEST_TYPE_ROBUSTNESS.ini"
        break
    case "EXPERIMENTAL":
        pTestConfigurationBasicTestTypeSource = "${params.TEST_TYPE}"
        pTestConfigurationBasicTestTypeDestination = "BASIC_TEST_TYPE_EXPERIMENTAL.ini"
        break
    default:
        pTestConfigurationBasicTestTypeSource = "configurations//basic//test_type//ALL.ini"
        pTestConfigurationBasicTestTypeDestination = "BASIC_TEST_TYPE_ALL.ini"
        break
}
println "Test Configuration - Basic - Test Type - Source: " + pTestConfigurationBasicTestTypeSource
env.pTestConfigurationBasicTestTypeSource = pTestConfigurationBasicTestTypeSource
println "Test Configuration - Basic - Test Type - Destination: " + pTestConfigurationBasicTestTypeDestination
env.pTestConfigurationBasicTestTypeDestination = pTestConfigurationBasicTestTypeDestination
// Basic (Requirement Source)
pTestConfigurationBasicRequirementSourceSource = "configurations//basic//requirement_source//ALL.ini"
println "Test Configuration - Basic - Requirement Source - Source: " + pTestConfigurationBasicRequirementSourceSource
env.pTestConfigurationBasicRequirementSourceSource = pTestConfigurationBasicRequirementSourceSource
pTestConfigurationBasicRequirementSourceDestination = "BASIC_REQUIREMENT_SOURCE_ALL.ini"
println "Test Configuration - Basic - Requirement Source - Destination: " + pTestConfigurationBasicRequirementSourceDestination
env.pTestConfigurationBasicRequirementSourceDestination = pTestConfigurationBasicRequirementSourceDestination
// Equipment
pTestConfigurationEquipmentSource = "configurations//equipment//" + pDeviceUnderTest + ".ini"
println "Test Configuration Equipment Source: " + pTestConfigurationEquipmentSource
env.pTestConfigurationEquipmentSource = pTestConfigurationEquipmentSource
pTestConfigurationEquipmentDestination = "EQUIPMENT_" + pDeviceUnderTest + ".ini"
println "Test Configuration Equipment Destination: " + pTestConfigurationEquipmentDestination
env.pTestConfigurationEquipmentDestination = pTestConfigurationEquipmentDestination