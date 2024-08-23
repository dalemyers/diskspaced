"""A CLI tool for checking disk space."""

import enum
import os
import platform
import shutil

from diskspaced.writer import Writer
from diskspaced.json_writer import JSONWriter
from diskspaced.grand_perspective_writer import GrandPerspectiveWriter


if platform.system() == "Windows":
    raise NotImplementedError("Windows is not supported by this tool.")


class OutputFormat(enum.Enum):
    """Represents the output format for the scan results."""

    JSON = "json"
    GRAND_PERSPECTIVE = "grandperspective"


def _get_block_size(path: str) -> int:
    """Get the block size for the given path.

    :param path: The path to get the block size for
    :returns: The block size
    """

    statvfs = os.statvfs(path)

    if platform.system() == "Darwin":
        return statvfs.f_frsize

    if platform.system() == "Linux":
        return statvfs.f_bsize

    raise NotImplementedError(f"Unsupported platform: {platform.system()}")


def _scan(folder_path: str, writer: Writer, process_in_order: bool) -> None:

    if os.path.islink(folder_path):
        return

    if os.path.isdir(folder_path):

        try:
            folder_details = os.stat(folder_path)
        except FileNotFoundError:
            return
        except OSError as e:
            if e.errno == 13:  # Permission denied
                return

        writer.write_folder_start(
            os.path.basename(folder_path),
            int(folder_details.st_atime),
            int(folder_details.st_mtime),
            int(folder_details.st_ctime),
        )

    files = []
    folders = []

    for item in os.listdir(folder_path):
        full_path = os.path.join(folder_path, item)

        if os.path.isdir(full_path):
            folders.append(full_path)
        else:
            files.append((full_path, item))

    if process_in_order:
        folders.sort()
        files.sort(key=lambda x: x[1])

    for folder in folders:
        _scan(folder, writer, process_in_order)

    for file_path, file_name in files:

        if os.path.islink(file_path):
            continue

        try:
            file_details = os.stat(file_path)
        except FileNotFoundError:
            # It could have been deleted in between scanning and processing
            continue
        except OSError as e:
            if e.errno == 13:  # Permission denied
                continue
            raise

        writer.write_file(
            file_name,
            file_details.st_size,
            int(file_details.st_atime),
            int(file_details.st_mtime),
            int(file_details.st_ctime),
        )

    writer.write_folder_end()


def scan(
    folder_path: str,
    output_path: str,
    output_format: OutputFormat,
    file_print_count: int,
    alphabetical: bool,
) -> None:
    """Scan the folder and write the results to the output path.

    :param folder_path: The path to scan
    :param output_path: The path to write the results to
    :param output_format: The format to write the results in
    :param file_print_count: The number of files to print after. Zero disables printing.
    :param alphabetical: Whether to process the files in alphabetical order
    """

    writer: Writer

    if output_format == OutputFormat.JSON:
        writer = JSONWriter(output_path, file_print_count)
    elif output_format == OutputFormat.GRAND_PERSPECTIVE:
        writer = GrandPerspectiveWriter(output_path, file_print_count)
    else:
        raise ValueError(f"Unknown output format: {output_format}")

    disk_usage = shutil.disk_usage(folder_path)
    block_size = _get_block_size(folder_path)

    writer.write_start(folder_path, disk_usage.total, disk_usage.used, disk_usage.free, block_size)

    _scan(folder_path, writer, alphabetical)

    writer.write_end()
