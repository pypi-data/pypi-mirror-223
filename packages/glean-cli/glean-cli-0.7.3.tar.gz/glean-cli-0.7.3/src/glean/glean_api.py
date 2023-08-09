from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import PurePath
from typing import List, Optional, Dict
from urllib.parse import urlparse, parse_qs
import webbrowser

import click
from click import ClickException
from requests import Session
from glean.constants import DEFAULT_CREDENTIALS_FILEPATH, GLEAN_DEBUG

from glean.credentials import CliCredentials
from glean.filesystem import build_spec_from_local
from glean import VERSION
from glean.utils.resource import Resource

GLEAN_BASE_URI = os.environ.get("GLEAN_CLI_BASE_URI", default="https://glean.io")
FILE_SIZE_LIMIT_MB = 50

def create_access_key(credentials_filepath: str, intended_project_id: Optional[str]):
    # If the logged-in user has multiple projects, this indicates that
    # we should request them to disambiguate the project ID they'd like
    # to create an access key for.
    has_multiple_projects = None

    # If project_id was passed but we find that the authenticated Glean user
    # is not a member of that project, this query param will be populated.
    invalid_project_id = None

    # Populated if access key was successfully created.
    project_name = None
    access_key_id = None
    access_key_token = None
    project_id = None
    user_email = None
    user_full_name = None

    # Populated if this is a new user.
    is_new_user = None

    # Populated if we encountered a request error while finishing authentication.
    request_error = False

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal has_multiple_projects
            
            nonlocal invalid_project_id

            nonlocal project_name
            nonlocal access_key_id
            nonlocal access_key_token
            nonlocal project_id
            nonlocal user_email
            nonlocal user_full_name
            nonlocal is_new_user

            nonlocal request_error

            query = urlparse(self.path).query
            parsed_query = parse_qs(query)

            # Utility for grabbing a query param from parsed_query.
            def get_query_param(param: str) -> Optional[str]:
                return parsed_query.get(param, [None])[0]

            has_multiple_projects = get_query_param("has_multiple_projects")

            invalid_project_id = get_query_param("invalid_project_id")

            project_name = get_query_param("project_name")
            access_key_id = get_query_param("access_key_id")
            access_key_token = get_query_param("access_key_token")
            project_id = get_query_param("project_id")
            user_email = get_query_param("user_email")
            user_full_name = get_query_param("user_full_name")

            is_new_user = get_query_param("is_new_user")

            # We expect either all newly created access key info or the project name
            # of the existing access key to be passed. If neither is true, indicate
            # a bad request.
            if not (
                has_multiple_projects or
                invalid_project_id or
                (project_name and access_key_id and access_key_token and project_id and user_email and user_full_name)
            ):
                request_error = True
                self.send_response(302)
                self.send_header('Location', f"{GLEAN_BASE_URI}/cliAuthConfirmation/error")
                self.end_headers()
                return

            self.send_response(302)
            if is_new_user:
                self.send_header('Location', f"{GLEAN_BASE_URI}/cliAuthConfirmation/success/newUser?userFullName={user_full_name}")
            else:
                self.send_header('Location', f"{GLEAN_BASE_URI}/cliAuthConfirmation/success/existingUser?userEmail={user_email}")
            self.end_headers()
            return
        
        # Disables logging in the CLI, which we don't want to expose to the user
        # unless in debug mode.
        def log_message(self, *args):
            if GLEAN_DEBUG:
                super().log_message(*args)
    
    server_address = ("localhost", 0)
    httpd = HTTPServer(server_address, CallbackHandler)

    redirect_url = f"http://localhost:{httpd.server_port}"
    login_url = f"{GLEAN_BASE_URI}/cliAuthConfirmation/entry?cli-auth-server-host={redirect_url}"
    if intended_project_id:
        login_url += f"&cli-auth-project-id={intended_project_id}"

    click.echo("🚀 Launching login page in your browser...")
    click.echo("If this isn't showing up, copy and paste the following URL into your browser:")
    click.echo()
    click.echo(login_url)
    click.echo()

    # Open login URL in browser.
    webbrowser.open_new(login_url)

    # Wait for our server to handle redirect.
    httpd.handle_request()

    # If encountered error while handling request, raise an exception.
    if request_error:
        raise click.ClickException("Unknown error while finishing authentication. Please try again.")
    
    def direct_user_to_project_admin_settings():
        click.echo(f"You can find the ID of any given Glean project in the {click.style('Project Administration', bold=True)} settings section:")
        click.echo()
        click.echo(f"{GLEAN_BASE_URI}/app/p/settings#project_administration")
        click.echo()
    
    if invalid_project_id:
        click.echo(
            f"Your Glean user does not belong to project {intended_project_id}. Please try again with the ID of a project you're a member of."
        )
        direct_user_to_project_admin_settings()
        return
    
    if has_multiple_projects:
        click.echo(f"You belong to multiple Glean projects. Please specify the ID of the project you'd like to create an access key for with the `--project-id` option.")
        direct_user_to_project_admin_settings()
        return

    credentials_filepath = os.path.expanduser(DEFAULT_CREDENTIALS_FILEPATH)
    f = open(credentials_filepath, "w")
    f.write(json.dumps({
        "access_key_id": access_key_id,
        "access_key_token": access_key_token,
        "project_id": project_id
    }))
    click.echo(f"✅ Saved new access key for {click.style(project_name, bold=True)} to {credentials_filepath}")
    click.echo()

    if is_new_user:
        terminal_size = os.get_terminal_size()
        click.echo("─" * terminal_size.columns)
        click.echo()
        click.echo(f"👋 Welcome {user_full_name}! We created a new Glean project for you.")
        click.echo()
        click.echo(f"{click.style('Go to the following link to set up a database connection:', bold=True)} {GLEAN_BASE_URI}/app/mb")
        click.echo()


def login(session: Session, credentials: CliCredentials):
    """Authenticates the session with the provided credentials.

    :return The user's project ID, if successfully logged in.
    :raises ClickException if the login is not successful.
    """
    r = session.post(
        GLEAN_BASE_URI + "/auth/login-cli",
        data={
            "accessKeyId": credentials.access_key_id,
            "accessKeyToken": credentials.access_key_token,
        },
        headers={"Glean-CLI-Version": VERSION},
    )
    # TODO(dse): Show custom error message from server, if present.
    if r.status_code >= 500:
        raise ClickException("Unexpected error initiating your Glean session.")
    elif r.status_code >= 400:
        raise ClickException("Your access key is invalid.")
    if not r.ok:
        raise ClickException("Unexpected error initiating your Glean session.")

    click.echo()
    click.echo("Successfully logged in to " + click.style(r.text, bold=True))
    click.echo("Project id: " + credentials.project_id)
    click.echo("Access key id: " + credentials.access_key_id)

    return credentials.project_id


def create_build_from_git_revision(
    session: Session,
    project_id: str,
    git_revision: Optional[str],
    git_path: Optional[str],
    deploy: bool,
    allow_dangerous_empty_build: bool = False,
    dbt_manifest_path: Optional[PurePath] = None,
):
    """Creates a build based on a git revision and returns the result."""
    build_spec = {
        "configFilesFromGit": {
            "revision": git_revision,
            "path": git_path,
            "dbtManifestPath": dbt_manifest_path,
        }
    }
    return _create_build(
        session, project_id, build_spec, deploy, allow_dangerous_empty_build
    )


def create_build_from_local_files(
    session: Session,
    project_id: str,
    path: str,
    deploy: bool,
    targets: Optional[set],
    allow_dangerous_empty_build: bool = False,
    dbt_manifest_path: Optional[PurePath] = None,
):
    """Creates a build using local files and returns the result."""
    build_spec = build_spec_from_local(path, project_id, targets, dbt_manifest_path)
    return _create_build(
        session, project_id, build_spec, deploy, allow_dangerous_empty_build
    )


def get_datasources(s: Session, project_id: str) -> dict:
    """Queries and formats datasources"""
    query = _get_data_connections(s, project_id)
    data_sources = {d["name"]: d["id"] for d in query["data"]["dataConnections"]}
    return data_sources


def clear_model_cache(s: Session, model_id: str) -> str:
    """Clears the cache for the specified model"""
    return _graphql_query(
        s,
        """
        mutation UpdateModelFreshnessKey($id: String!) {
            updateModelFreshnessKey(id: $id)
        }
        """,
        {"id": model_id},
    )


class PullResourceResponse(dict):
    configs: List[Resource]
    errors: List[str]


def pull_resource(
    s: Session,
    project_id: str,
    resource_type: Optional[str],
    resource_id: Optional[str],
    dataops_only: Optional[bool],
) -> PullResourceResponse:
    """Pulls the DataOps config for the given resource, or all resources in the project if none is specified."""
    res = _graphql_query(
        s,
        """
        query PullResource($projectId: String!, $resourceType: String, $resourceId: String, $dataOpsOnly: Boolean) {
            pullResource(
                projectId: $projectId,
                resourceType: $resourceType,
                resourceId: $resourceId,
                dataOpsOnly: $dataOpsOnly
            ) { configs, errors }
        }
        """,
        {
            "projectId": project_id,
            "resourceType": resource_type,
            "resourceId": resource_id,
            "dataOpsOnly": dataops_only,
        },
    )["data"]["pullResource"]
    res["configs"] = [
        Resource.from_dict(json.loads(string)) for string in res["configs"]
    ]
    return res


def _parse_table_data(table_data: dict) -> Dict[str, Dict[str, str]]:
    """Formats table names for output, and returns tables names and schemas"""
    tables = table_data["data"]["getAvailableGleanDbTables"]
    tables_by_name = {}
    for table in tables:
        name = (
            table["schema"] + "." + table["name"] if table["schema"] else table["name"]
        )
        tables_by_name[name] = {"schema": table["schema"], "name": table["name"]}
    return tables_by_name


def _create_build(
    session, project_id, build_spec, deploy, allow_dangerous_empty_build=False
):
    return _graphql_query(
        session,
        """
        mutation CreateBuild($projectId: String!, $buildSpec: BuildSpecInput!, $deploy: Boolean!, $allowEmptyBuild: Boolean) {
            createBuild( projectId: $projectId, buildSpec: $buildSpec, deploy: $deploy, allowEmptyBuild: $allowEmptyBuild) {
                id,
                resources {
                    added { modelBundles { model { name } }, savedViews { name }, dashboards { name }, colorPalettes { name }, homepageLaunchpads { id } }
                    changed { modelBundles { model { name } }, savedViews { name }, dashboards { name }, colorPalettes { name }, homepageLaunchpads { id } }
                    unchanged { modelBundles { model { name } }, savedViews { name }, dashboards { name }, colorPalettes { name }, homepageLaunchpads { id } }
                    deleted { modelBundles { model { name } }, savedViews { name }, dashboards { name }, colorPalettes { name }, homepageLaunchpads { id } }
                },
                warnings,
                errors
            }
        }
        """,
        {
            "projectId": project_id,
            "buildSpec": build_spec,
            "deploy": deploy,
            "allowEmptyBuild": allow_dangerous_empty_build,
        },
    )


def _get_data_connections(session: Session, project_id: str) -> dict:
    query = _graphql_query(
        session,
        """
        query dataConnections($projectId: String!){
            dataConnections(projectId: $projectId){
                id,
                name
            }
        }
        """,
        {"projectId": project_id},
    )
    return query


def _get_table_data(session: Session, datasource_id: str) -> dict:
    query = _graphql_query(
        session,
        """
        query getAvailableGleanDbTables($datasourceId: String!){
            getAvailableGleanDbTables (datasourceId: $datasourceId){
                name,
                schema
            }
        }
        """,
        {"datasourceId": datasource_id},
    )
    return query


def get_tables(s: Session, datasource_id: str) -> Dict[str, Dict[str, str]]:
    """Queries and formats table from datasource"""
    query = _get_table_data(s, datasource_id)
    tables = _parse_table_data(query)
    return tables


preview_uri = lambda build_results, query_name="createBuild": click.style(
    f"{GLEAN_BASE_URI}/app/?build={build_results['data'][query_name]['id']}",
    underline=True,
)

build_details_uri = lambda build_results, query_name="createBuild": click.style(
    f"{GLEAN_BASE_URI}/app/p/builds/{build_results['data'][query_name]['id']}",
    underline=True,
)

preview_model_uri = (
    lambda model_id, build_results, query_name="modelPreviewBuildFromGleanDb": f"{GLEAN_BASE_URI}/app/m/{model_id}?build={build_results['data'][query_name]['id']}"
)


def _graphql_query(session: Session, query: str, variables: dict):
    r = session.post(
        GLEAN_BASE_URI + "/graphql/",
        json={"query": query, "variables": variables},
        headers={"Glean-CLI-Version": VERSION},
    )
    if r.status_code == 504:
        raise ClickException(
            f"The Glean CLI client has timed out but your request is still running on our server. Please check your project's build page in a few minutes to see build results: {GLEAN_BASE_URI}/app/p/data-ops"
        )
    elif r.status_code != 200:
        raise ClickException("Unexpected error received from the Glean server.")

    results = r.json()
    graphql_exceptions = results.get("errors")
    if (
        graphql_exceptions
        and isinstance(graphql_exceptions[0], dict)
        and graphql_exceptions[0].get("message")
    ):
        error = graphql_exceptions[0]["message"]

        # Must match error message in server code at glean/services/data_ops/build_management.py line #543 (as of 7/5/23).
        if (
            error
            == "No Glean config files were found, and empty builds were not enabled, so the build was aborted."
        ):
            error += "\n\tTo enable empty builds, use the --allow-dangerous-empty-build flag.\n\tWARNING: This will remove all data-ops managed resources, and any resources that depend on them, from your project."
            from glean.cli import _echo_build_errors_and_exit

            _echo_build_errors_and_exit([error])

        raise ClickException(
            f"Unexpected error received from the Glean server:\n  {error}"
        )

    return results


def upload_files_to_glean(
    session: Session, project_id: str, database_name: str, path: str
) -> str:
    datasources = get_datasources(session, project_id)
    db_id = datasources.get(database_name)

    if db_id:
        return _post_file(session, project_id, db_id, path)
    else:
        raise ClickException(
            "Error uploading file\n  Datbase does not exist with name "
            f'"{database_name}"'
            "\n  run glean databases to see valid names "
        )


def _is_over_filesize_limit(file_path: str) -> bool:
    size_in_bytes = os.path.getsize(file_path)
    size_in_mb = size_in_bytes / (1024 * 1024)

    return size_in_mb > FILE_SIZE_LIMIT_MB


def _post_file(session: Session, project_id: str, db_id: str, file_path: str) -> str:
    if _is_over_filesize_limit(file_path):
        raise ClickException(
            f"File exceeds upload limit of {FILE_SIZE_LIMIT_MB} megabytes"
        )

    r = session.post(
        GLEAN_BASE_URI + "/upload/data-file",
        data={
            "projectId": project_id,
            "dataConnectionId": db_id,
        },
        files={"file": open(file_path, "rb")},
        headers={"Glean-CLI-Version": VERSION},
    )

    results = r.json()
    file_errors = results.get("error")
    if file_errors:
        raise ClickException(f"Error uploading file\n  {file_errors}")

    uploaded_filename = results.get("filename")

    if uploaded_filename:
        return uploaded_filename
    else:
        raise ClickException(f"Error uploading file\n  Unexpected result from server")


def export_query(
    session: Session, endpoint: str, data: dict, additional_headers: dict = {}
):
    """POST request to export controllers"""
    r = session.post(
        GLEAN_BASE_URI + f"/export/{endpoint}",
        data=json.dumps(data),
        headers={"Glean-CLI-Version": VERSION, **additional_headers},
    )
    if r.status_code != 200:
        raise ClickException("Unexpected error received from the Glean server.")
    return r.text
