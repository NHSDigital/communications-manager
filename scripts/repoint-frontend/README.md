# Repoint Frontend

The "Repoint Frontend" script automates the process of reconfiguring the `communications-manager-api` APIs to point to a dynamic backend environment in the `comms-mgr` repository, rather than the default common backend in `internal-dev`.

## Overview

This script is especially useful when engineers are testing changes across both the `communications-manager-api` and `comms-mgr` repositories. By default, the `communications-manager-api` APIs point to a common backend in `internal-dev`, which is convenient when only `communications-manager-api` changes need testing. However, when changes span both `communications-manager-api` and `comms-mgr` and need testing in a specific dynamic environment (e.g. `de-todr3`), manual reconfiguration is required.

The script simplifies this process by automatically:

1. Pointing the APIs to the correct backend environment
2. Disabling mTLS where necessary

## Prerequisites

Before running the "Repoint Frontend" script, ensure the following prerequisites are met:

- You must be logged into a developer AWS account using SSO authentication
- The repository must be named `communications-manager-api` to avoid potential root path issues

## Steps

The script performs the following steps:

1. Remove mTLS if set, ensuring it is disabled if previously configured
2. Create a new branch to contain changes to the proxy
3. Update proxy files with the necessary configuration changes
4. Stage, commit, and push changes to the remote repository

## Post-Script Manual Steps

### Configure Apigee for PR Branch

After successfully running the script, follow these steps to configure Apigee to work with your PR branch. This will allow you to authenticate and send requests to a comms-pr-xxx branch.

- Log in to Apigee
- Navigate to Publish > Apps
- Search for comms-manager-local
- Select Edit
- Choose Add Product
- Search for your PR number and add the internal dev product

### Sending a Request

To send a request:

- Set up an internal-dev request and update "comms" in the URL to point to PR number:

```
https://internal-dev.api.service.nhs.uk/comms-pr-000/
```

For more information, see [How to point APIM to a backend dynamic environment](https://nhsd-confluence.digital.nhs.uk/display/RIS/NHS+Notify+%7C+How+to+point+APIM+to+a+backend+dynamic+environment).

## Usage

```bash
./scripts/repoint-frontend/repoint_frontend.sh <ticket ID> <environment>
```

e.g.
```bash
./scripts/repoint-frontend/repoint_frontend.sh 0000 de-todr3
```

Positional Arguments:

- `ticket ID` Numeric ID of the ticket (e.g., '0000')
- `environment` The environment identifier (e.g., 'de-todr3')

Options:

- `--help` | `-h` Display usage information and exit, outlining all available commands
