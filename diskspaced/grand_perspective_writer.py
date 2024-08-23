"""A CLI tool for checking disk space."""

import datetime
import os

from diskspaced import writer

# Example:
# <?xml version="1.0" encoding="UTF-8"?>
# <GrandPerspectiveScanDump appVersion="4" formatVersion="7">
#    <ScanInfo volumePath="/" volumeSize="994662584320" freeSpace="319055134720" scanTime="2024-08-23T13:58:23Z" fileSizeMeasure="physical">
#        <Folder name="Users/dalemyers/Projects/diskspaced/tests/data/test_scan_downloads_gp" created="2024-08-23T13:56:53Z" modified="2024-08-23T13:56:53Z" accessed="2024-08-23T13:56:53Z">
#            <Folder name="a" created="2024-08-23T13:56:53Z" modified="2024-08-23T13:56:53Z" accessed="2024-08-23T13:56:53Z">
#                <File name="one.txt" size="4096" created="2024-08-23T13:56:53Z" modified="2024-08-23T13:58:13Z" accessed="2024-08-23T13:58:14Z" />
#                <Folder name="b" created="2024-08-23T13:56:53Z" modified="2024-08-23T13:56:53Z" accessed="2024-08-23T13:56:53Z">
#                    <File name="two.txt" size="4096" created="2024-08-23T13:56:53Z" modified="2024-08-23T13:58:15Z" accessed="2024-08-23T13:58:17Z" />
#                    <Folder name="c" created="2024-08-23T13:56:53Z" modified="2024-08-23T13:56:53Z" accessed="2024-08-23T13:56:53Z">
#                        <File name="three.txt" size="4096" created="2024-08-23T13:56:53Z" modified="2024-08-23T13:58:20Z" accessed="2024-08-23T13:58:21Z" />
#                    </Folder>
#                </Folder>
#            </Folder>
#        </Folder>
#    </ScanInfo>
# </GrandPerspectiveScanDump>


class GrandPerspectiveWriter(writer.Writer):
    """A write out results as JSON."""

    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    FOLDER_OPEN = "<Folder ".encode("utf-8")
    FOLDER_CLOSE = "</Folder>\n".encode("utf-8")
    FILE_OPEN = "<File ".encode("utf-8")
    FILE_CLOSE = "/>\n".encode("utf-8")
    CLOSE_TAG = ">\n".encode("utf-8")
    ATTR_CLOSE = '" '.encode("utf-8")
    ATTR_NAME = 'name="'.encode("utf-8")
    ATTR_SIZE = 'size="'.encode("utf-8")
    ATTR_CREATED = 'created="'.encode("utf-8")
    ATTR_MODIFIED = 'modified="'.encode("utf-8")
    ATTR_ACCESSED = 'accessed="'.encode("utf-8")

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

        if not root_path.endswith("/"):
            root_path += "/"

        now = datetime.datetime.now()
        scan_time = now.strftime(GrandPerspectiveWriter.DATE_FORMAT)

        # This only happens once, so we don't bother caching the encoded values
        self.file.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode("utf-8"))
        self.file.write(
            '  <GrandPerspectiveScanDump appVersion="4" formatVersion="7">\n'.encode("utf-8")
        )
        self.file.write(
            f'    <ScanInfo volumePath="{root_path}" volumeSize="{disk_usage_total}" freeSpace="{disk_usage_free}" scanTime="{scan_time}" fileSizeMeasure="physical">\n'.encode(
                "utf-8"
            )
        )

        if os.environ.get("PYTEST_CURRENT_TEST"):
            self.file.flush()

    def write_end(self) -> None:
        """Write the end of the output file."""
        super().write_end()
        self.file.write("  </ScanInfo>\n</GrandPerspectiveScanDump>".encode("utf-8"))
        self.file.close()

    def write_folder_start(
        self, folder_name: str, accessed_time: int, modified_time: int, created_time: int
    ) -> None:
        """Write the start of a folder entry."""

        super().write_folder_start(folder_name, accessed_time, modified_time, created_time)

        self.file.write(GrandPerspectiveWriter.FOLDER_OPEN)

        self.file.write(GrandPerspectiveWriter.ATTR_NAME)
        self.file.write(folder_name.encode("utf-8"))
        self.file.write(GrandPerspectiveWriter.ATTR_CLOSE)

        self.file.write(GrandPerspectiveWriter.ATTR_CREATED)
        self.file.write(
            datetime.datetime.fromtimestamp(created_time)
            .strftime(GrandPerspectiveWriter.DATE_FORMAT)
            .encode("utf-8")
        )
        self.file.write(GrandPerspectiveWriter.ATTR_CLOSE)

        self.file.write(GrandPerspectiveWriter.ATTR_MODIFIED)
        self.file.write(
            datetime.datetime.fromtimestamp(modified_time)
            .strftime(GrandPerspectiveWriter.DATE_FORMAT)
            .encode("utf-8")
        )
        self.file.write(GrandPerspectiveWriter.ATTR_CLOSE)

        self.file.write(GrandPerspectiveWriter.ATTR_ACCESSED)
        self.file.write(
            datetime.datetime.fromtimestamp(accessed_time)
            .strftime(GrandPerspectiveWriter.DATE_FORMAT)
            .encode("utf-8")
        )
        self.file.write(GrandPerspectiveWriter.ATTR_CLOSE)

        self.file.write(GrandPerspectiveWriter.CLOSE_TAG)

        if os.environ.get("PYTEST_CURRENT_TEST"):
            self.file.flush()

    def write_folder_end(self) -> None:
        """Write the end of a folder entry."""

        super().write_folder_end()

        self.file.write(GrandPerspectiveWriter.FOLDER_CLOSE)

        if os.environ.get("PYTEST_CURRENT_TEST"):
            self.file.flush()

    def write_file(
        self, file_name: str, size: int, accessed_time: int, modified_time: int, created_time: int
    ) -> None:
        """Write the start of a file entry."""

        super().write_file(file_name, size, accessed_time, modified_time, created_time)

        self.file.write(GrandPerspectiveWriter.FILE_OPEN)

        self.file.write(GrandPerspectiveWriter.ATTR_NAME)
        self.file.write(file_name.encode("utf-8"))
        self.file.write(GrandPerspectiveWriter.ATTR_CLOSE)

        self.file.write(GrandPerspectiveWriter.ATTR_SIZE)
        self.file.write(str(min(self.block_size, size)).encode("utf-8"))
        self.file.write(GrandPerspectiveWriter.ATTR_CLOSE)

        self.file.write(GrandPerspectiveWriter.ATTR_CREATED)
        self.file.write(
            datetime.datetime.fromtimestamp(created_time)
            .strftime(GrandPerspectiveWriter.DATE_FORMAT)
            .encode("utf-8")
        )
        self.file.write(GrandPerspectiveWriter.ATTR_CLOSE)

        self.file.write(GrandPerspectiveWriter.ATTR_MODIFIED)
        self.file.write(
            datetime.datetime.fromtimestamp(modified_time)
            .strftime(GrandPerspectiveWriter.DATE_FORMAT)
            .encode("utf-8")
        )
        self.file.write(GrandPerspectiveWriter.ATTR_CLOSE)

        self.file.write(GrandPerspectiveWriter.ATTR_ACCESSED)
        self.file.write(
            datetime.datetime.fromtimestamp(accessed_time)
            .strftime(GrandPerspectiveWriter.DATE_FORMAT)
            .encode("utf-8")
        )
        self.file.write(GrandPerspectiveWriter.ATTR_CLOSE)

        self.file.write(GrandPerspectiveWriter.FILE_CLOSE)

        if os.environ.get("PYTEST_CURRENT_TEST"):
            self.file.flush()
