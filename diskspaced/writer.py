"""A CLI tool for checking disk space."""

import abc
from io import IOBase
import logging
import os

from diskspaced.constants import MAX_RECURSION_LIMIT


class Writer(abc.ABC):
    """A base class for writing disk space results."""

    output_path: str
    block_size: int
    file: IOBase
    file_print_count: int
    current_folder_path: str
    depth = 0

    def __init__(self, output_path: str, file_print_count: int) -> None:
        self.output_path = output_path
        self.block_size = 0
        self.file_print_count = file_print_count
        self.file_count = 0
        self.depth = 0
        self.current_folder_path = ""

        if MAX_RECURSION_LIMIT < 100:
            raise ValueError("MAX_RECURSION_LIMIT must be at least 100")

    def write_start(
        self,
        root_path: str,
        disk_usage_total: int,
        disk_usage_used: int,
        disk_usage_free: int,
        block_size: int,
    ) -> None:
        """Write the start of the output file."""
        self.file_count = 0
        self.current_folder_path = root_path

    def write_end(self) -> None:
        """Write the end of the output file."""

    def write_folder_start(
        self, folder_name: str, accessed_time: int, modified_time: int, created_time: int
    ) -> None:
        """Write the start of a folder entry."""
        self.current_folder_path = os.path.join(self.current_folder_path, folder_name)
        self.depth += 1

        if float(self.depth) / MAX_RECURSION_LIMIT > 0.9:
            logging.warning(f"Nearing recursion limit of {MAX_RECURSION_LIMIT}")

        if float(self.depth) > MAX_RECURSION_LIMIT - 100:
            logging.error(
                f"Reached recursion limit of {MAX_RECURSION_LIMIT} at {self.current_folder_path}"
            )
            raise RecursionError(
                f"Reached recursion limit of {MAX_RECURSION_LIMIT} at {self.current_folder_path}"
            )

    def write_folder_end(self) -> None:
        """Write the end of a folder entry."""
        self.current_folder_path = os.path.dirname(self.current_folder_path)
        self.depth -= 1

    def write_file(
        self, file_name: str, size: int, accessed_time: int, modified_time: int, created_time: int
    ) -> None:
        """Write the start of a file entry."""
        self.file_count += 1

        if self.file_print_count != 0 and self.file_count % self.file_print_count == 0:
            logging.info(f"Processing {os.path.join(self.current_folder_path, file_name)}")

    def pretty_print(self) -> None:
        """Pretty print the output."""
