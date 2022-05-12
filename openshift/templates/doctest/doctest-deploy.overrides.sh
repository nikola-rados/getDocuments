#! /bin/bash
_includeFile=$(type -p overrides.inc)
if [ ! -z ${_includeFile} ]; then
  . ${_includeFile}
else
  _red='\033[0;31m'; _yellow='\033[1;33m'; _nc='\033[0m'; echo -e \\n"${_red}overrides.inc could not be found on the path.${_nc}\n${_yellow}Please ensure the openshift-developer-tools are installed on and registered on your path.${_nc}\n${_yellow}https://github.com/BCDevOps/openshift-developer-tools${_nc}"; exit 1;
fi

# ========================================================================
# Special Deployment Parameters needed for the backup instance.
# ------------------------------------------------------------------------
# The generated config map is used to update the Backup configuration.
# ========================================================================
CONFIG_MAP_NAME=doctest-conf
SOURCE_FILE=$( dirname "$0" )/../../../docker/doctest.conf

OUTPUT_FORMAT=json
OUTPUT_FILE=${CONFIG_MAP_NAME}-configmap_DeploymentConfig.json

printStatusMsg "Generating ConfigMap; ${CONFIG_MAP_NAME} ..."
generateConfigMap "${CONFIG_MAP_NAME}" "${SOURCE_FILE}" "${OUTPUT_FORMAT}" "${OUTPUT_FILE}"


if createOperation; then
  readParameter "JC_INTERFACE_USERNAME - Please provide the JC-Interface username:" JC_INTERFACE_USERNAME "" "false"
  readParameter "JC_INTERFACE_PROD_PASSWORD - Please provide the JC-Interface PROD password:" JC_INTERFACE_PROD_PASSWORD "" "false"
  readParameter "JC_INTERFACE_TEST_PASSWORD - Please provide the JC-Interface TEST password:" JC_INTERFACE_TEST_PASSWORD "" "false"
  readParameter "JC_INTERFACE_DEV_PASSWORD - Please provide the JC-Interface DEV password:" JC_INTERFACE_DEV_PASSWORD "" "false"

  readParameter "WSGW_URL_PROD - Please provide the getDocument URL for WSGW on PROD:" WSGW_URL_PROD "" "false"
  readParameter "WSGW_URL_TEST - Please provide the getDocument URL for WSGW on TEST:" WSGW_URL_TEST "" "false"
  readParameter "WSGW_URL_DEV - Please provide the getDocument URL for WSGW on DEV:" WSGW_URL_DEV "" "false"
  readParameter "CATS_URL_PROD - Please provide the getDocument URL for CATS on PROD:" CATS_URL_PROD "" "false"
  readParameter "CATS_URL_TEST - Please provide the getDocument URL for CATS on TEST:" CATS_URL_TEST "" "false"
  readParameter "CATS_URL_DEV - Please provide the getDocument URL for CATS on DEV:" CATS_URL_DEV "" "false"

  readParameter "REQUEST_AGENCY_IDENTIFIER_ID_PROD - Please provide the request agency identifier ID for PROD:" REQUEST_AGENCY_IDENTIFIER_ID_PROD "" "false"
  readParameter "REQUEST_AGENCY_IDENTIFIER_ID_TEST - Please provide the request agency identifier ID for TEST:" REQUEST_AGENCY_IDENTIFIER_ID_TEST "" "false"
  readParameter "REQUEST_AGENCY_IDENTIFIER_ID_DEV - Please provide the request agency identifier ID for DEV:" REQUEST_AGENCY_IDENTIFIER_ID_DEV "" "false"
  readParameter "REQUEST_PART_ID_PROD - Please provide the request participant ID for PROD:" REQUEST_PART_ID_PROD "" "false"
  readParameter "REQUEST_PART_ID_TEST - Please provide the request participant ID for TEST:" REQUEST_PART_ID_TEST "" "false"
  readParameter "REQUEST_PART_ID_DEV - Please provide the request participant ID for DEV:" REQUEST_PART_ID_DEV "" "false"
  readParameter "PCSS_APPLICATION_CODE - Please provide the PCSS application code:" PCSS_APPLICATION_CODE "" "false"
  readParameter "SCV_APPLICATION_CODE - Please provide the SCV application code:" SCV_APPLICATION_CODE "" "false"

  readParameter "TARGET_URL - Please provide the Justice target URL:" TARGET_URL "" "false"
  readParameter "COOKIE - Please provide a valid cookie:" COOKIE "" "false"

else
  printStatusMsg "Update operation detected ...\nSkipping the prompts for the all the secrets ...\n"

  writeParameter "JC_INTERFACE_USERNAME" "prompt_skipped" "false"
  writeParameter "JC_INTERFACE_PROD_PASSWORD" "prompt_skipped" "false"
  writeParameter "JC_INTERFACE_TEST_PASSWORD" "prompt_skipped" "false"
  writeParameter "JC_INTERFACE_DEV_PASSWORD" "prompt_skipped" "false"

  writeParameter "WSGW_URL_PROD" "prompt_skipped" "false"
  writeParameter "WSGW_URL_TEST" "prompt_skipped" "false"
  writeParameter "WSGW_URL_DEV" "prompt_skipped" "false"
  writeParameter "CATS_URL_PROD" "prompt_skipped" "false"
  writeParameter "CATS_URL_TEST" "prompt_skipped" "false"
  writeParameter "CATS_URL_DEV" "prompt_skipped" "false"

  writeParameter "REQUEST_AGENCY_IDENTIFIER_ID_PROD" "prompt_skipped" "false"
  writeParameter "REQUEST_AGENCY_IDENTIFIER_ID_TEST" "prompt_skipped" "false"
  writeParameter "REQUEST_AGENCY_IDENTIFIER_ID_DEV" "prompt_skipped" "false"
  writeParameter "REQUEST_PART_ID_PROD" "prompt_skipped" "false"
  writeParameter "REQUEST_PART_ID_TEST" "prompt_skipped" "false"
  writeParameter "REQUEST_PART_ID_DEV" "prompt_skipped" "false"
  writeParameter "PCSS_APPLICATION_CODE" "prompt_skipped" "false"
  writeParameter "SCV_APPLICATION_CODE" "prompt_skipped" "false"

  writeParameter "TARGET_URL" "prompt_skipped" "false"
  writeParameter "COOKIE" "prompt_skipped" "false"
fi

SPECIALDEPLOYPARMS="--param-file=${_overrideParamFile}"
echo ${SPECIALDEPLOYPARMS}