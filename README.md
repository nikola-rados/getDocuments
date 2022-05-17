[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Lifecycle:Stable](https://img.shields.io/badge/Lifecycle-Stable-97ca00)](https://github.com/bcgov/repomountie/blob/master/doc/lifecycle-badges.md)

# Testing platform for `getDocument` service through JC-Interface and SCV

This repository provides scripts to test the `getDocument` service through a number of interfaces.

## Understanding the Output

The scripts print out three groups of messages, **Error Messages**, **Management Commands**, and an **Error Summary**.

The **Error Messages** list the details of each of the discrepancies detected by the scripts.

The **Management Commands** list the [orgbook-configurations](https://github.com/bcgov/orgbook-configurations) and/or [von-bc-registries-agent-configurations](https://github.com/bcgov/von-bc-registries-agent-configurations) management commands needed to fix the detected issues.

The **Error Summary** provides a summary of the audit run and is produced whether or not there are any issues detected.

### Management Commands

These can include commands to delete the existing OrgBook data and re-queue the data from the BC Reg issuer.  Commands will look like the following example:

```
./manage -e prod queueOrganization CP0009876
./manage -e prod queueOrganization 3456543
./manage -e prod queueOrganization 3456789
./manage -p bc -e prod deleteTopic BC1234567
./manage -e prod requeueOrganization 1234567
./manage -p bc -e prod deleteTopic BC1234589
./manage -e prod requeueOrganization 1234589
```

In this example, the first 3 lines represent companies missing in OrgBook, and must be queued from BC Reg.

The last 4 lines represent 2 companies in OrgBook that are incorrect and must be deleted and re-processed.

The commands should be run in the order listed, however, if, for some reason, you need to run the commands in a batch, the `orgbook-configurations` scripts should always be run first.

Commands in the following forms should be run using the openshift `./manage` scripts from [orgbook-configurations](https://github.com/bcgov/orgbook-configurations):
- `./manage -p bc -e <env> deleteTopic <business_number>`

Commands in the following forms should be run using the openshift `./manage` scripts from [von-bc-registries-agent-configurations](https://github.com/bcgov/von-bc-registries-agent-configurations):
- `./manage -e <env> queueOrganization <business_number>`
- `./manage -e <env> requeueOrganization <business_number>`

## Running on Docker

The [./manage](./manage) script can be used to build and start a container for running the scripts.  The container was designed for use in OpenShift and by default starts the scripts using a cron tab [audit.conf](./docker/audit.conf).  Once the container is running you can shell into the container and run the scripts manually.  When running in docker add all of your environment variables to the `./env/.env` file.  This file will be created for you the first time you start the container.

When running locally the various databases will have to be port forwarded to your machine.  In order for the container to be able to connect with the databases you will need to specify the host names as `host.docker.internal` and forward the databases to separate ports.

Example:

From the command line (after updating your .env file):
```
./manage build
./manage start
./manage shell audit
```

From the shell inside the container:
```
(app-root) bash-4.4$ cd scripts/
(app-root) bash-4.4$ python ./detail_audit_report.py 
Get corp stats from OrgBook DB 2021-11-22 08:29:49.528329
Get corp stats from BC Registries DB 2021-11-22 08:29:52.320647
...
```

Type `exit` when complete, and then `./manage stop` to stop the container.

## Running in OpenShift

The audit container was designed to be run in OpenShift.  Once configured it runs the scripts on a schedule and posts the results to the `von-notifications` channel in the BCGov rocket.chat instance.

The [openshift-developer-tools](https://github.com/BCDevOps/openshift-developer-tools/tree/master/bin) compatible OpenShift configurations are contained in the [openshift](./openshift) folder.

The [openshift](./openshift) folder also contains a [./manage](./openshift/manage) script that can be used to build and deploy container images from your local source code.

Example (run from the `openshift` folder) - Build and deploy the `dev` and `test`:
```
./manage -e tools buildAndTag dev
./manage -e tools -e tools tag dev test
```