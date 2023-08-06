import os
import click

from zipfile import ZipFile, ZIP_DEFLATED
from estela_cli.utils import (
    get_project_path,
    get_estela_settings,
    _in,
)
from estela_cli.login import login
from estela_cli.templates import (
    OK_EMOJI,
    ESTELA_DIR,
    ESTELA_YAML_NAME,
)
import logging


SHORT_HELP = "Deploy Scrapy project to estela API"


def zip_project(pid, project_path, estela_settings):
    relroot = os.path.abspath(os.path.join(project_path, os.pardir))
    archives_to_ignore = estela_settings["deploy"]["ignore"]
    with ZipFile("{}.zip".format(pid), "w", ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(project_path):
            # ignoring dir with data from jobs
            rel_root = root.replace("{}/".format(project_path), "")
            if _in(rel_root, archives_to_ignore):
                continue
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                arcname = os.path.join(os.path.relpath(root, relroot), file)
                zip.write(filename, arcname)


def verify_requrements(requirements_path):
    project_path = get_project_path()
    requirements_local_path = os.path.join(project_path, requirements_path)
    if not os.path.exists(requirements_local_path):
        raise click.ClickException("The requirements file does not exist.")


@click.command(short_help=SHORT_HELP)
@click.option("--verbose", is_flag=True, help="Show debug logs.")
def estela_command(verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)

    estela_client = login()
    logging.debug(f"Successfully logged in to {estela_client.host}")
    estela_settings = get_estela_settings()
    logging.debug(f"Successfully read estela settings: {estela_settings}")
    project_path = get_project_path()
    p_settings = estela_settings["project"]
    pid = p_settings["pid"]
    logging.debug(f"Project path: {project_path}")

    try:
        logging.debug(f"Verifying project exists...")
        estela_client.get_project(pid)
        logging.debug(f"Verified project exists.")
    except:
        raise click.ClickException(
            "Invalid project at {}/{}.".format(ESTELA_DIR, ESTELA_YAML_NAME)
        )

    logging.debug(f"Verifying requirements...")
    verify_requrements(p_settings["requirements"])
    logging.debug(f"Successfully verified requirements.")

    logging.debug(f"Zipping project for upload to estela...")
    zip_project(pid, project_path, estela_settings)
    logging.debug(f"Successfully zipped the project.")

    response = {}
    try:
        logging.debug(f"Uploading project...")
        response = estela_client.upload_project(pid, open("{}.zip".format(pid), "rb"))
        logging.debug(f"Successfully uploaded the project.")
    except Exception as e:
        os.remove("{}.zip".format(pid))
        logging.debug(str(e))
        raise click.ClickException("A problem occurred while uploading the project.")

    click.echo(
        "{} Project uploaded successfully. Deploy {} underway.".format(
            OK_EMOJI, response.get("did")
        )
    )
    os.remove("{}.zip".format(pid))
