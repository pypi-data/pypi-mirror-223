import os
import shutil
import tempfile
import time
import zipfile
from datetime import datetime
from enum import Enum

import click
import requests
from rich.console import Console
from rich.progress import Progress
from rich.tree import Tree

SERVICE_URL = "https://oracle.korbit.ai:8012/v1/check"
SCAN_REPORT_URL = "https://oracle.korbit.ai:8002/v3/scans"
FILE_UPLOAD_URL = f"{SERVICE_URL}/korbit-ai/files"
TICK_ROTATION = False
TOP_FOLDER_KORBIT_MENTOR = ".korbitmentor"


class ProgressStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PROGRESS = "PROGRESS"


@click.command()
@click.argument("folder", type=click.Path(exists=True))
def main(folder):
    os.makedirs(TOP_FOLDER_KORBIT_MENTOR, exist_ok=True)
    click.echo(f"Zipping folder: {folder}")

    zip_file_path = zip_folder(folder)
    click.echo(f"Zipping completed successfully {zip_file_path}")

    scan_id = upload_file(zip_file_path)
    click.echo(f"Starting analysis of {zip_file_path}")

    display_scan_status(scan_id)
    report_path = download_report(scan_id)
    click.echo(f"You can access the report at {report_path}")


def generate_zip_file_name(folder_path: str):
    if folder_path in [".", "./"]:
        return "current_dir.zip"
    elif folder_path in ["..", "../"]:
        return "parent_dir.zip"
    folder_path = folder_path.replace("../", "").replace("./", "").replace("/", "-")
    return folder_path + ".zip"


def zip_folder(folder_path: str):
    folder_path = folder_path[:-1] if folder_path.endswith("/") else folder_path
    zip_file_path = generate_zip_file_name(folder_path)
    top_folder_name = os.path.basename(folder_path).replace(".", "-")
    temp_folder_path = tempfile.mkdtemp()

    try:
        temp_top_folder_path = os.path.join(temp_folder_path, top_folder_name)
        shutil.copytree(folder_path, temp_top_folder_path)

        with zipfile.ZipFile(zip_file_path, "w") as zipf:
            zipf.write(temp_top_folder_path, top_folder_name)
            for root, _, files in os.walk(temp_folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_folder_path)
                    zipf.write(file_path, arcname)
    finally:
        shutil.rmtree(temp_folder_path)

    return zip_file_path


def upload_file(zip_file_path) -> str:
    with open(zip_file_path, "rb") as file:
        response = requests.post(FILE_UPLOAD_URL, files={"repository": file})
        if response.status_code == 200:
            return response.json()
        else:
            raise click.ClickException("File upload failed!")


def create_tree_node(name, status):
    if status == "PROGRESS":
        name_with_status = name + (" ⌛️" if TICK_ROTATION else " ⏳")
    elif status == "FAILURE":
        name_with_status = name + " ❌"
    elif status == "SUCCESS":
        name_with_status = name + " ✅"
    else:
        name_with_status = name + " 👀"
    node = Tree(name_with_status)
    return node


def build_file_tree(file_list):
    file_tree = {}
    for file_info in file_list:
        file_name = file_info["name"]
        file_status = file_info.get("status", "Unknown")

        # Extract directory and filename from the file path
        directory, filename = os.path.split(file_name)

        # Traverse the file_tree to the appropriate directory node
        current_node = file_tree
        for folder in directory.split(os.sep):
            if folder not in current_node:
                current_node[folder] = {}
            current_node = current_node[folder]

        current_node[filename] = file_status

    return file_tree


def add_nodes_to_tree(tree_node, current_node):
    for name, value in current_node.items():
        if isinstance(value, dict):
            if name:
                node = tree_node.add(name)
            else:
                node = tree_node
            add_nodes_to_tree(node, value)
        else:
            tree_node.add(create_tree_node(name, value))


def display_scan_status(scan_id: str):
    console = Console()
    global TICK_ROTATION
    while True:
        response = requests.get(f"{SERVICE_URL}/{scan_id}/progress")
        TICK_ROTATION = not TICK_ROTATION
        try:
            data = response.json()
            status = data.get("status")
            if not status:
                console.clear()
                console.print("Analysis requested is in the queue, it will start shortly...")
                time.sleep(1)
                continue
            if status == ProgressStatus.SUCCESS.value:
                console.clear()
                console.print("Analysis completed successfully! Report generation in progress...")
                break
            progress = data.get("progress", 0.0)
            total_progress = data.get("total_progress", 0.0)
            title = data.get("title", "File status")

            file_tree_data = data.get("files", [])
            file_tree = build_file_tree(file_tree_data)

            tree = Tree(title)
            add_nodes_to_tree(tree, file_tree)

            with Progress(console=console, auto_refresh=True) as progress_bar:
                task = progress_bar.add_task(f"Analyzing files ({len(file_tree_data)})...", total=100, spinner="⌛️")
                progress_bar.update(task, completed=progress)

            with Progress(console=console, auto_refresh=True) as progress_bar_total:
                task = progress_bar_total.add_task("Remaining analysis types...", total=100, spinner="⌛️")
                progress_bar_total.update(task, completed=total_progress)

            console.clear()
            console.print(tree)
            console.print(progress_bar)
            console.print(progress_bar_total)

        except Exception as e:
            console.print(f"Error processing response: {e}")
        time.sleep(1)


def download_report(scan_id: str) -> str:
    response = requests.get(f"{SCAN_REPORT_URL}/{scan_id}/issues?format=json&output_concept_embedding=false")
    report_path = f"{TOP_FOLDER_KORBIT_MENTOR}/{scan_id}_{datetime.now().isoformat()}_report.json"
    with open(report_path, "w+") as file:
        file.write(response.content.decode())
    return report_path


if __name__ == "__main__":
    main()
