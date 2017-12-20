# ez-repo

A **python** command line client which interacts with storage endpoints (for now only S3) and makes the user store files as if in artefact repository server.
This tool is useful for projects which technologies does not provide an easy way to publish their artefacts and they want a simple and cheap way to do it.
Repo helps keeping artefacts organized as it stores them in a normalized way (repository/organization/name/version/name-version-classifiers.extension).

With repo, you typically write an INI file describing your artefacts and how you want to publish them then you add this line to your CI pipeline and your artefacts will be uploaded in a formalized way.
The code is pretty simple as it uses Boto3 but it can be improved by adding multiple storage drivers later to enable repo to push on other storage while providing the same interface to users.

# Build status
   [![Build Status](https://travis-ci.org/EasyMile/ez-repo.svg?branch=master)](https://travis-ci.org/EasyMile/ez-repo)

## Installation

- With pip

```bash
pip install --user https://github.com/easymile/ez-repo/archive/master.zip
```

- Enjoy :)

## Initialisation

# S3
To use ez-repo with S3 you must authenticate to AWS with IAM.

- Retrieve/create your AWS IAM credentials (http://console.aws.amazon.com/iam/home?#users)

- Initialize credentials to access AWS (http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html)

## Usage

- Upload an artefact (complete description)

```bash
ez-repo upload --storage-endpoint example-bucket --repository release --society "easymile" --name "repo" --artefactversion "1.0.0" --classifiers "python" --extension ".tar.gz" --file "./repo-1.0.0-python.tar.gz"
```

- Upload an artefact (interactive mode). Only the **--file** is mandatory to upload. Repo use the file name to fill defaults values if matching standard **name-version-classifiers.extension**.

```bash
ez-repo upload --storage-endpoint example-bucket --repository release --file "./repo-1.0.0-python.tar.gz"
```

- ez-repo also supports reading INI file listing artefacts properties and their respective path in order to upload them in one command.

```bash
cat artefacts.ini
[repo]
local_path = ./repo-1.0.0-python.tar.gz
name = repo
classifiers = python
extension = .tar.gz

ez-repo upload --storage-endpoint example-bucket --config ./artefacts.ini
```

- Search for an artefact matching an expression

```bash
ez-repo search --storage-endpoint example-bucket --expression ".*"

release/easymile/repo/repo-1.0.0-python.tar.gz
```

- Download works with expressions (user will be prompted before downloading)

```bash
ez-repo download --storage-endpoint example-bucket --expression ".*repo-1.0.0-python.tar.gz"
```

- Delete also works like download and search (user will be prompted before deletion)

```bash
ez-repo delete --storage-endpoint example-bucket --expression ".*repo-1.0.0.tar.gz"
```

## Developers

To develop on repo, it is useful to use virtualenvs in order to sandbox the dev environment. It is also recommended to check the tool via installation before merging to master.
