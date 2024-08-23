"""A CLI tool for checking disk space."""

import os

from diskspaced import writer

# Example:
# {
#    "root_path": "/Users/dalemyers/Downloads",
#    "contents": [
#        {
#            "path": "foo",
#            "contents": [
#                {"type": "file", "name": "bar", "size": 1234},
#                {"type": "file", "name": "baz", "size": 1243},
#                {"type": "folder", "name": "qux", "contents": []},
#            ],
#        }
#    ],
# }


class JSONWriter(writer.Writer):
    """A write out results as JSON."""

    OPEN_BRACE = "{".encode("utf-8")
    TYPE_FILE = '"type": "file", '.encode("utf-8")
    TYPE_FOLDER = '"type": "folder", '.encode("utf-8")
    FIELD_NAME = '"name": "'.encode("utf-8")
    FIELD_SIZE = '"size": '.encode("utf-8")
    FIELD_ACCESSED = '"accessed": '.encode("utf-8")
    FIELD_MODIFIED = '"modified": '.encode("utf-8")
    FIELD_CREATED = '"created": '.encode("utf-8")
    FIELD_CONTENTS = '"contents": [\n'.encode("utf-8")
    FOLDER_END = "]},\n".encode("utf-8")
    CLOSE_BRACE = "},\n".encode("utf-8")
    STRING_COMMA = '",'.encode("utf-8")
    COMMA = ",".encode("utf-8")

    def write_start(
        self,
        root_path: str,
        disk_usage_total: int,
        disk_usage_used: int,
        disk_usage_free: int,
        block_size: int,
    ) -> None:
        """Write the start of the output file."""

        super().write_start(
            root_path, disk_usage_total, disk_usage_used, disk_usage_free, block_size
        )

        # pylint: disable=consider-using-with
        self.block_size = block_size
        self.file = open(self.output_path, "wb")
        # pylint: enable=consider-using-with

        # This only happens once, so we don't bother caching the encoded values
        self.file.write("{".encode("utf-8"))
        self.file.write(('"root_path": "' + root_path + '", ').encode("utf-8"))
        self.file.write(('"volume_size": ' + str(disk_usage_total) + ", ").encode("utf-8"))
        self.file.write(('"free_space": ' + str(disk_usage_free) + ", ").encode("utf-8"))
        self.file.write(('"used_space": ' + str(disk_usage_used) + ", ").encode("utf-8"))
        self.file.write('"contents": [\n'.encode("utf-8"))

        if os.environ.get("PYTEST_CURRENT_TEST"):
            self.file.flush()

    def write_end(self) -> None:
        """Write the end of the output file."""

        super().write_end()

        self.file.seek(-2, 1)  # Remove the final comma
        self.file.write("\n]}".encode("utf-8"))
        self.file.close()

    def write_folder_start(
        self, folder_name: str, accessed_time: int, modified_time: int, created_time: int
    ) -> None:
        """Write the start of a folder entry."""

        super().write_folder_start(folder_name, accessed_time, modified_time, created_time)

        self.file.write(JSONWriter.OPEN_BRACE)
        self.file.write(JSONWriter.TYPE_FOLDER)

        self.file.write(JSONWriter.FIELD_NAME)
        self.file.write(folder_name.encode("utf-8"))
        self.file.write(JSONWriter.STRING_COMMA)

        self.file.write(JSONWriter.FIELD_ACCESSED)
        self.file.write(str(accessed_time).encode("utf-8"))
        self.file.write(JSONWriter.COMMA)

        self.file.write(JSONWriter.FIELD_MODIFIED)
        self.file.write(str(modified_time).encode("utf-8"))
        self.file.write(JSONWriter.COMMA)

        self.file.write(JSONWriter.FIELD_CREATED)
        self.file.write(str(created_time).encode("utf-8"))
        self.file.write(JSONWriter.COMMA)

        self.file.write(JSONWriter.FIELD_CONTENTS)

        if os.environ.get("PYTEST_CURRENT_TEST"):
            self.file.flush()

    def write_folder_end(self) -> None:
        """Write the end of a folder entry."""

        super().write_folder_end()

        self.file.seek(-2, 1)  # Remove the final comma
        self.file.write(JSONWriter.FOLDER_END)

        if os.environ.get("PYTEST_CURRENT_TEST"):
            self.file.flush()

    def write_file(
        self, file_name: str, size: int, accessed_time: int, modified_time: int, created_time: int
    ) -> None:
        """Write the start of a file entry."""

        super().write_file(file_name, size, accessed_time, modified_time, created_time)

        self.file.write(JSONWriter.OPEN_BRACE)
        self.file.write(JSONWriter.TYPE_FILE)

        self.file.write(JSONWriter.FIELD_NAME)
        self.file.write(file_name.encode("utf-8"))
        self.file.write(JSONWriter.STRING_COMMA)

        self.file.write(JSONWriter.FIELD_SIZE)
        self.file.write(str(max(self.block_size, size)).encode("utf-8"))
        self.file.write(JSONWriter.COMMA)

        self.file.write(JSONWriter.FIELD_ACCESSED)
        self.file.write(str(accessed_time).encode("utf-8"))
        self.file.write(JSONWriter.COMMA)

        self.file.write(JSONWriter.FIELD_MODIFIED)
        self.file.write(str(modified_time).encode("utf-8"))
        self.file.write(JSONWriter.COMMA)

        self.file.write(JSONWriter.FIELD_CREATED)
        self.file.write(str(created_time).encode("utf-8"))
        # No comma here

        self.file.write(JSONWriter.CLOSE_BRACE)

        if os.environ.get("PYTEST_CURRENT_TEST"):
            self.file.flush()
