# aws-aurora-db

Example script for connecting to an **Amazon Aurora (MySQL)** database using **AWS IAM Database Authentication** instead of a traditional password.

Instead of storing a database password, the script requests a short-lived access token (valid for 15 minutes) from AWS using your IAM credentials, and uses it to authenticate. That way there's no database password to manage or rotate.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed.
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) configured with an IAM user/role that has `rds-db:connect` permission on the corresponding database user.
- A database user created with IAM authentication enabled (`IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS'`), with the privileges you need.
- The Amazon RDS root certificate (`global-bundle.pem`), required for the TLS connection. Download it with:

  ```bash
  curl -o global-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
  ```

## Installation

Clone the repository and install the dependencies with `uv`:

```bash
git clone https://github.com/jcatanop/aurora-mysql-snipt.git
cd aurora-mysql-snipt
uv sync
```

## Configuration

Connection details and credentials **don't live in the code** — they go in a `.env` file at the root of the project (this file is in `.gitignore` and is never pushed to the repository).

Copy the example template and fill it in with your own values:

```bash
cp .env.example .env
```

Edit `.env` with your Aurora instance's values:

```env
DB_HOST=your-cluster.cluster-xxxxxxxx.us-east-1.rds.amazonaws.com
DB_PORT=3306
DB_NAME=mysql
DB_USER=your_iam_db_user
AWS_REGION=us-east-1
SSL_CA=./global-bundle.pem
```

## Usage

With `.env` and `global-bundle.pem` in place, run:

```bash
uv run main.py
```

If everything is configured correctly (IAM permissions, the database's security group, and a user with IAM authentication enabled), the script connects and prints the database engine version.

## Security notes

- Never commit `.env` or `*.pem` files — both are excluded via `.gitignore`.
- The auth token is generated on the fly on every run and expires after 15 minutes; it is never stored anywhere.
