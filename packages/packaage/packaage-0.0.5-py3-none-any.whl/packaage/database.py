from __future__ import absolute_import

import json
import logging

import boto3
import psycopg2


logger = logging.getLogger(__name__)


def connect_rds(secret_id: str, db_name: str) -> psycopg2.extensions.connection:
    """Create a connector to an AWS RDS database.

    It will search the secret into Secret Manager to retreive all the connection information.
    The only parameter not retreive is the database in the server it will connect.
    Because this project use only one database, this parameter is hardcoded in the script but a
    block can be added to check the secret id passed as argument and dynamicly change it.

    Args:
        secret_id (str): The name of the secret for the database in Secret Manager
        db_name (str): The name of the db to connect to.

    Raises:
        secret_unknown: The secret entered as parameter is not known in Secret Manager

    Returns:
        psycopg2.extensions.connection: The connector to the database
    """
    secrets = boto3.client("secretsmanager", "eu-west-1")

    try:
        credentials = json.loads(secrets.get_secret_value(SecretId=secret_id).get("SecretString"))
    except secrets.exceptions.ResourceNotFoundException as secret_unknown:
        logger.error('Secret: %s not found !', secret_id)
        raise secret_unknown

    connector = psycopg2.connect(
        user=credentials.get("username"),
        password=credentials.get("password"),
        port=credentials.get("port"),
        database=db_name,
        host=credentials.get("host"),
    )

    connector.set_session(autocommit=True)

    return connector
