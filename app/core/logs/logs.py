"""Manage and view logs."""

import subprocess
from subprocess import CalledProcessError
from typing import List, Tuple

from app.core.utility.logger_setup import get_logger

log = get_logger()


class Logs:
    """Manage and view logs."""

    def _logs_from_command(self, cmd: str) -> Tuple[List[str], str]:
        """Get the logs from a specified command.

        Args:
            cmd: Command to execte to get logs

        Returns:
            True if successful, else False
            If error, returns error message
        """
        log.info(f"Retrieving system logs: {cmd}")
        try:
            result = subprocess.run(
                cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except CalledProcessError as error:
            error_msg = f"Failed retrieving logs. {error}"
            return [], error_msg
        log_lines = result.stdout.decode().strip().split("\n")
        return log_lines, ""

    def file(
        self,
        filepath: str,
        line_pattern: str,
        start_line_index: int = 0,
        end_line_index: int = 2000,
    ) -> Tuple[List[str], str]:
        """Get the logs within a local file.

        Args:
            filepath: Path to local log file
            line_pattern: Glob pattern to match and filter logs returned
            start_line_index: Line number to start from
            end_line_index: Line number to end at

        Returns:
            Tuple containing a list of log lines and an error message (if any).
        """
        cmd = f"cat {filepath}"
        if line_pattern:
            cmd += f" | grep -i '{line_pattern}'"
        cmd += f" | tail -n +{start_line_index} | head -n {end_line_index - start_line_index + 1}"
        log_lines, error_message = self._logs_from_command(cmd)
        if len(log_lines) < 1:
            return [], f'No matching log lines found within file "{filepath}"'
        return log_lines, error_message

    def service(
        self,
        service_name: str,
        line_pattern: str,
        start_line_index: int = 0,
        end_line_index: int = 2000,
    ) -> Tuple[List[str], str]:
        """Get the logs from a specified command.

        Args:
            service_name: Name of the running service
            line_pattern: Glob pattern to match and filter logs returned
            start_line_index: Line number to start from
            end_line_index: Line number to end at

        Returns:
            True if successful, else False
            If error, returns error message
        """
        cmd = f"journalctl -u {service_name} --no-pager --no-hostname --lines {end_line_index}"
        if line_pattern:
            cmd += f" | grep -i '{line_pattern}'"
        cmd += f" | tail -n +{start_line_index + 1}"
        log_lines, error_message = self._logs_from_command(cmd)
        if len(log_lines) < 1:
            return [], f'No matching log lines found within service "{service_name}"'
        return log_lines, error_message
