import json

from mstrio.connection import Connection
from mstrio.helpers import IServerError
from mstrio.utils.api_helpers import (
    FuturesSessionWithRenewal,
    changeset_manager,
    unpack_information,
)
from mstrio.utils.datasources import (
    alter_conn_list_resp,
    alter_conn_resp,
    alter_instance_list_resp,
    alter_instance_resp,
    alter_patch_req_body,
)
from mstrio.utils.error_handlers import ErrorHandler
from mstrio.utils.helper import exception_handler, response_handler


@ErrorHandler(err_msg='Error getting available DBMSs.')
def get_available_dbms(connection, error_msg=None):
    """Get information for all available database management systems (DBMSs).

    Args:
        connection: MicroStrategy REST API connection object
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 200/400
    """
    url = f"{connection.base_url}/api/dbobjects/dbmss"
    return connection.get(url=url)


@ErrorHandler(err_msg='Error getting available database drivers.')
def get_available_db_drivers(connection, error_msg=None):
    """Get information for all available database drivers.

    Args:
        connection: MicroStrategy REST API connection object
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 200/400
    """
    url = f"{connection.base_url}/api/dbobjects/drivers"
    return connection.get(url=url)


def get_datasource_instance(connection, id, error_msg=None):
    """Get information for a specific database source.

    Args:
        connection: MicroStrategy REST API connection object
        id (string): ID
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 200/400
    """
    url = f"{connection.base_url}/api/datasources/{id}"
    response = connection.get(url=url)
    if not response.ok:
        if error_msg is None:
            error_msg = f"Error getting Datasource Instance with ID: {id}"
        response_handler(response, error_msg)
    response = alter_instance_resp(response)
    return response


@ErrorHandler(err_msg='Error deleting Datasource Instance with ID {id}')
def delete_datasource_instance(connection, id, error_msg=None):
    """Delete a specific database source based on id.

    Args:
        connection: MicroStrategy REST API connection object
        id (string): ID
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 204/400
    """
    url = f"{connection.base_url}/api/datasources/{id}"
    return connection.delete(url=url)


def update_datasource_instance(connection, id, body, error_msg=None):
    """Update a specific database source based on id.

    Args:
        connection: MicroStrategy REST API connection object
        id (string): ID
        body: update operation info
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 200/400
    """
    url = f"{connection.base_url}/api/datasources/{id}"
    for op_dict in body["operationList"]:
        op_dict = alter_patch_req_body(
            op_dict, "/datasourceConnection", "/databaseConnectionId"
        )
        op_dict = alter_patch_req_body(
            op_dict, "/primaryDatasource", "/databasePrimaryDatasourceId"
        )
        op_dict = alter_patch_req_body(
            op_dict, "/dataMartDatasource", "/databaseDataMartDatasourceId"
        )
        alter_patch_req_body(op_dict, "/dbms", "/dbmsId")
    response = connection.patch(url=url, json=body)
    if not response.ok:
        if error_msg is None:
            error_msg = f"Error updating Datasource Instance with ID: {id}"
        response_handler(response, error_msg)
    return response


def create_datasource_instance(connection, body, error_msg=None):
    """Create a specific database source.

    Args:
        connection: MicroStrategy REST API connection object
        id (string): ID
        body: Datasource info
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 201/400
    """
    url = f"{connection.base_url}/api/datasources"
    response = connection.post(url=url, json=body)
    if not response.ok:
        if error_msg is None:
            name = body.get("name", "NA")
            error_msg = f"Error creating Datasource Instance: {name}"
        response_handler(response, error_msg)
    response = alter_instance_resp(response)
    return response


@ErrorHandler(err_msg='Error getting the namespaces for datasource with ID: {id}.')
def get_datasource_namespaces(
    connection: "Connection",
    id: str,
    project_id: str | None = None,
    refresh: bool | None = None,
    fields: str | None = None,
    error_msg: str | None = None,
):
    """Get namespaces for a specific datasource.

    Args:
        connection: MicroStrategy REST API connection object
        id (str): Database ID
        project_id (str, optional): Project ID
        refresh (bool, optional): Force refresh
        fields (str, optional): A whitelist of top-level fields separated by
            commas. Allow the client to selectively retrieve fields in the
            response.
        error_msg (str, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 200.
    """
    if project_id is None:
        connection._validate_project_selected()
        project_id = connection.project_id

    return connection.get(
        url=f"{connection.base_url}/api/datasources/{id}/catalog/namespaces",
        headers={
            'X-MSTR-ProjectID': project_id,
        },
        params={
            'refresh': refresh,
            'fields': fields,
        },
    )


def get_datasource_namespaces_async(
    session: FuturesSessionWithRenewal,
    connection: "Connection",
    id: str,
    project_id: str | None = None,
    refresh: bool | None = None,
    fields: str | None = None,
):
    return session.get(
        url=f"{connection.base_url}/api/datasources/{id}/catalog/namespaces",
        headers={
            'X-MSTR-ProjectID': project_id,
        },
        params={
            'refresh': refresh,
            'fields': fields,
        },
    )


def get_datasource_instances(
    connection, ids=None, database_type=None, project=None, error_msg=None
):
    """Get information for all database sources.

    Args:
        connection: MicroStrategy REST API connection object
        ids: list of datasources ids
        database_type: list of types (names) of databases
        project: id (str) of a project or instance of an Project class
            to search for the datasource instances in. When provided, both
            `ids` and `database_types` are ignored. By default `None`.
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 200/400
    """
    if project:
        url = f"{connection.base_url}/api/projects/{project}/datasources"
        response = connection.get(url=url)
    else:
        database_type = None if database_type is None else database_type.join(",")
        ids = None if ids is None else ids.join(",")
        url = f"{connection.base_url}/api/datasources"
        response = connection.get(
            url=url, params={'id': ids, 'database.type': database_type}
        )
    if not response.ok:
        res = response.json()
        if project and res.get("message") == "HTTP 404 Not Found":
            # aka project based endpoint not supported
            # try without filtering
            warning_msg = (
                "get_datasource_instances() warning: filtering by Project "
                "is not yet supported on this version of the I-Server. "
                "Returning all values."
            )
            exception_handler(warning_msg, Warning)
            return get_datasource_instances(
                connection=connection,
                ids=ids,
                database_type=database_type,
                error_msg=error_msg,
            )
        if not error_msg:
            if (
                project
                and res.get('code') == "ERR006"
                and "not a valid value for Project ID" in res.get('message')
            ):
                error_msg = f"{project} is not a valid Project class instance or ID"
                raise ValueError(error_msg)
            error_msg = "Error getting Datasource Instances"
            if project:
                error_msg += f" within `{project}` Project"
        response_handler(response, error_msg)
    response = alter_instance_list_resp(response)
    return response


def get_datasource_connections(connection, error_msg=None):
    """Get information for all datasource connections.

    Args:
        connection: MicroStrategy REST API connection object
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 200/400
    """
    url = f"{connection.base_url}/api/datasources/connections"

    response = connection.get(url=url)
    if not response.ok:
        if error_msg is None:
            error_msg = "Error getting Datasource Connections"
        response_handler(response, error_msg)
    response = alter_conn_list_resp(response)
    return response


def get_datasource_connection(connection, id, error_msg=None):
    """Get a datasource connection for given id.

    Args:
        connection: MicroStrategy REST API connection object
        id (string): ID
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 200/400
    """
    url = f"{connection.base_url}/api/datasources/connections/{id}"
    response = connection.get(url=url)
    if not response.ok:
        if error_msg is None:
            error_msg = (
                f"Error getting Datasource Connection with ID: {id}. "
                f"Check if it is not embedded Datasource Connection."
            )
        response_handler(response, error_msg)
    response = alter_conn_resp(response)
    return response


def update_datasource_connection(connection, id, body, error_msg=None):
    """Update a datasource connection based on id.

    Args:
        connection: MicroStrategy REST API connection object
        id (string): ID
        body: update operation info
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 200/400
    """
    url = f"{connection.base_url}/api/datasources/connections/{id}"
    for op_dict in body["operationList"]:
        alter_patch_req_body(op_dict, "/datasourceLogin", "/databaseLoginId")
    response = connection.patch(url=url, json=body)
    if not response.ok:
        if error_msg is None:
            error_msg = f"Error updating Datasource Connection with ID: {id}"
        response_handler(response, error_msg)
    return response


@ErrorHandler(err_msg='Error deleting Datasource Connection with ID {id}')
def delete_datasource_connection(connection, id):
    """Delete a datasource connection based on id.

    Args:
        connection: MicroStrategy REST API connection object
        id (string): ID
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 204/400
    """
    url = f"{connection.base_url}/api/datasources/connections/{id}"
    return connection.delete(url=url)


def create_datasource_connection(connection, body, error_msg=None):
    """Create a specific database connection.

    Args:
        connection: MicroStrategy REST API connection object
        body: Datasource Connection info
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 201/400
    """
    url = f"{connection.base_url}/api/datasources/connections"
    response = connection.post(url=url, json=body)
    if not response.ok:
        if error_msg is None:
            name = body.get("name", "NA")
            error_msg = f"Error creating Datasource connection: {name}"
        response_handler(response, error_msg)
    response = alter_conn_resp(response)
    return response


@ErrorHandler(err_msg='Error testing Datasource connection.')
def test_datasource_connection(connection, body, error_msg=None):
    """Test a datasource connection. Either provide a connection id, or the
    connection parameters within connection object.

    Args:
        connection: MicroStrategy REST API connection object.
        body: Datasource Connection info.
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. HTTP STATUS 204/400
    """
    url = f"{connection.base_url}/api/datasources/connections/test"
    return connection.post(url=url, json=body)


@ErrorHandler(err_msg='Error fetching connection mappings.')
def get_datasource_mappings(
    connection: Connection,
    default_connection_map: bool | None = False,
    project_id: str | None = None,
    error_msg: str | None = None,
):
    """Get information for all connection mappings.

    Args:
        connection: MicroStrategy REST API connection object
        default_connection_map (bool, optional): If True will get the default
            connection mappings for a project. Requires `project_id`
            parameter. Default False.
        project_id: The project_id, required only for default connection
            mappings.
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 200.
    """
    response = connection.get(
        url=f"{connection.base_url}/api/datasources/mappings",
        params={
            "defaultConnectionMap": default_connection_map,
            "projectId": project_id,
        },
    )

    if default_connection_map and not response.ok and response.status_code == 404:
        response.status_code = 200
        response._content = json.dumps({'mappings': []}).encode('utf-8')

    return response


@ErrorHandler(err_msg='Error fetching connection mapping with ID {id}.')
def get_datasource_mapping(
    connection: Connection,
    id=str,
    default_connection_map: bool | None = False,
    project_id: str | None = None,
    error_msg: str | None = None,
):
    """Get information about specific connection mapping.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the mapping
        default_connection_map (bool, optional): If True will get the default
            connection mappings for a project. Requires `project_id`
            parameter. Default False.
        project_id: The project_id, required only for default connection
            mappings.
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 200.
    """

    response = get_datasource_mappings(
        connection=connection,
        default_connection_map=default_connection_map,
        project_id=project_id,
        error_msg=error_msg,
    )

    # Faking get single resource endpoint. Only 'list all' available on REST
    if response.ok:
        response_json = response.json()

        try:
            mappings = [
                mapping for mapping in response_json['mappings'] if mapping["id"] == id
            ]

            mapping_data = mappings[0]
            mapping_data['ds_connection'] = mapping_data.pop('connection')
        except LookupError:
            raise IServerError(message="Connection Mapping not found", http_code=None)

        response.encoding, response._content = 'utf-8', json.dumps(mapping_data).encode(
            'utf-8'
        )
    return response


@ErrorHandler(err_msg='Error creating connection mapping.')
def create_datasource_mapping(
    connection: Connection, body, error_msg: str | None = None
):
    """Create a new connection mapping.

    Args:
        connection: MicroStrategy REST API connection object
        body: Datasource Connection Map creation info.
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 201.
    """
    url = f"{connection.base_url}/api/datasources/mappings"
    return connection.post(url=url, json=body)


@ErrorHandler(err_msg='Error deleting connection mapping with ID {id}')
def delete_datasource_mapping(
    connection: Connection, id: str, error_msg: str | None = None
):
    """Delete a connection mapping based on id.

    Args:
        connection: MicroStrategy REST API connection object
        id (string): ID of the mapping meant to be deleted.
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 204.
    """
    url = f"{connection.base_url}/api/datasources/mappings/{id}"
    return connection.delete(url=url)


@ErrorHandler(err_msg="Error getting Datasource logins.")
def get_datasource_logins(connection: Connection, error_msg: str | None = None):
    """Get information for all datasource logins.

    Args:
        connection: MicroStrategy REST API connection object
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 200.
    """
    url = f"{connection.base_url}/api/datasources/logins"
    return connection.get(url=url)


@ErrorHandler(err_msg='Error creating Datasource login.')
def create_datasource_login(connection: Connection, body, error_msg: str | None = None):
    """Create a new datasource login.

    Args:
        connection: MicroStrategy REST API connection object
        body: Datasource login creation info.
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 201.
    """
    url = f"{connection.base_url}/api/datasources/logins"
    return connection.post(url=url, json=body)


@ErrorHandler(err_msg='Error getting Datasource login with ID {id}')
def get_datasource_login(connection: Connection, id: str, error_msg: str | None = None):
    """Get datasource login for a specific id.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the login
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 200.
    """
    url = f"{connection.base_url}/api/datasources/logins/{id}"
    return connection.get(url=url)


@ErrorHandler(err_msg='Error deleting Datasource login with ID {id}')
def delete_datasource_login(
    connection: Connection, id: str, error_msg: str | None = None
):
    """Delete a datasource login.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the login
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 204.
    """
    url = f"{connection.base_url}/api/datasources/logins/{id}"
    return connection.delete(url=url)


@ErrorHandler(err_msg='Error updating Datasource login with ID {id}')
def update_datasource_login(
    connection: Connection, id: str, body, error_msg: str | None = None
):
    """Update a datasource login.

    Args:
        connection: MicroStrategy REST API connection object
        id: ID of the login
        body: Datasource Connection Map creation info.
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object. Expected status is 200.
    """
    url = f"{connection.base_url}/api/datasources/logins/{id}"
    return connection.patch(url=url, json=body)


@ErrorHandler(err_msg="Error getting table columns for table: {table_id}")
def get_table_columns(
    connection: Connection,
    datasource_id: str,
    namespace_id: str,
    table_id: str,
    error_msg: str | None = None,
):
    url = (
        f"{connection.base_url}/api/datasources/{datasource_id}/catalog/namespaces/"
        f"{namespace_id}/tables/{table_id}"
    )
    return connection.get(url, headers={"X-MSTR-ProjectID": connection.project_id})


@unpack_information
@ErrorHandler(
    err_msg='Error converting Datasource embedded connection from DSN to DSN-less'
)
def convert_ds_dsn(
    connection: Connection, datasource_id: str, error_msg: str | None = None
):
    """Convert datasource embedded connection from DSN to DSN-less format
    connection string and update the object to metadata.

    Args:
        connection: MicroStrategy REST API connection object
        datasource_id (string) : Datasource id
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        HTTP response object with updated embedded connection data.
        Expected status is 200.
    """
    url = f"{connection.base_url}/api/datasources/{datasource_id}/conversion"
    return connection.post(url=url)


@unpack_information
@ErrorHandler(
    err_msg='Error converting Datasource connection object from DSN to DSN-less'
)
def convert_connection_dsn(
    connection: Connection, ds_connection_id: str, error_msg: str | None = None
):
    """Convert datasource connection from DSN to DSN-less format connection
    string and update the object to metadata.

    Args:
        connection: MicroStrategy REST API connection object
        ds_connection_id (string) : Datasource connection object id
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        HTTP response object with updated object data. Expected status is 200.
    """
    url = (
        f"{connection.base_url}/api/datasources/connections/{ds_connection_id}"
        f"/conversion"
    )
    return connection.post(url=url)


@ErrorHandler(err_msg='Error getting VLDB settings for datasource with ID: {id}')
def get_vldb_settings(connection: 'Connection', id: str, error_msg: str = None):
    """Get advanced VLDB settings for a datasource.

    Args:
        connection (Connection): MicroStrategy REST API connection object
        id (string): Datasource ID
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object.
    """

    return connection.get(
        url=f'{connection.base_url}/api/model/datasources/{id}'
        '?showAdvancedProperties=true'
    )


@ErrorHandler(err_msg='Error updating VLDB settings for datasource with ID {id}')
def update_vldb_settings(
    connection: 'Connection', id: str, body: dict, error_msg: str = None
):
    """Update metadata of advanced VLDB settings for a datasource.

    Args:
        connection (Connection): MicroStrategy REST API connection object
        id (string): Datasource ID
        body (dict): JSON-formatted data used to update VLDB settings
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object.
    """

    with changeset_manager(connection) as changeset_id:
        return connection.put(
            url=f'{connection.base_url}/api/model/datasources/{id}',
            json=body,
            headers={'X-MSTR-MS-Changeset': changeset_id},
        )


@ErrorHandler(
    err_msg='Error getting metadata of VLDB settings for datasource with ID {id}'
)
def get_applicable_vldb_settings(
    connection: 'Connection', id: str, error_msg: str = None
):
    """Get metadata of advanced VLDB settings for a datasource.

    Args:
        connection (Connection): MicroStrategy REST API connection object
        id (string): Datasource ID
        error_msg (string, optional): Custom Error Message for Error Handling

    Returns:
        Complete HTTP response object.
    """

    return connection.get(
        url=f'{connection.base_url}/api/model/datasources/{id}'
        '/applicableAdvancedProperties'
    )
