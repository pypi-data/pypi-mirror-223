from datetime import datetime, timedelta
import gzip
import logging
import os
import re
import socket
import sys
import time

from typing import Iterator
import urllib.error
import urllib.parse


class Request:
    """Represent the data in a single line of the Apache log file."""

    def __init__(
            self,
            ip_address: str,
            re_match_dict: dict,
            url_prefix: str,
            url: str,
            response_code: int,
            content_length: int,
    ):
        self.ip_address = ip_address
        self.timestamp = time.strptime(
            re_match_dict.get("timestamp")[:20], "%d/%b/%Y:%H:%M:%S"
        )
        self.user_agent = re_match_dict.get("user_agent", "")
        self.referer = re_match_dict.get("referer")
        self.url = self.parse_url(url, url_prefix)
        self.response_code = response_code
        self.content_length = content_length

    def parse_url(self, url: str, url_prefix: str) -> str:
        try:
            if url.startswith("http"):
                return url_prefix + urllib.parse.urlparse(url).path.lower()
            return self.normalise_url(url_prefix + url.lower())
        except ValueError:
            raise ValueError(f"Error parsing: {url}, {sys.stderr}")

    def normalise_url(self, url: str) -> str:
        try:
            return url[:-1] if url[-1] == "/" else url
        except IndexError as err:
            raise IndexError(f"Error parsing: {url}, {err}")

    def fmttime(self) -> str:
        fmt = "%Y-%m-%d %H:%M:%S"
        return datetime(*self.timestamp[:6]).strftime(fmt)

    def __str__(self) -> str:
        return f"Request {self.fmttime()}, {self.ip_address}, {self.url}"

    def __iter__(self):
        for _item in self.as_tuple():
            yield _item

    def as_tuple(self) -> tuple[str, str, str, str]:
        return (self.fmttime(), self.ip_address, self.url, self.user_agent)

    def sanitise_url(self, regexes: str) -> None:
        for regex in regexes:
            matched = re.search(re.compile(regex), self.url)
            if matched is not None:
                self.url = matched.group(0)
                break


class LogStream:
    def __init__(
            self,
            log_dir: str,
            filter_groups: list,
            url_prefix: str,
            start_date: str,
            end_date: str,
    ) -> None:
        self.log_dir = log_dir
        self.filter_groups = filter_groups
        self.url_prefix = url_prefix
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")

        self.access_logs_re = re.compile(
            r"(?P<ip_address>\d+\.\d+\.\d+\.\d+) "
            r"(?P<users>.+ .+) "
            r"\[(?P<timestamp>.+)\] "
            r'"(?P<request>.+)" '
            r"(?P<status_and_size>\d+ \d+) "
            r'(?P<referer>".+") '
            r'"(?P<user_agent>.+)"'
        )

    def regex_match_line(self, line: str) -> Request | None:
        """
        Use regex to convert the line to a dict identifying all
        parts, if not, just log it and skip the line, then, call the
        Request class. Also if the line doesn't match (strict) the
        timestamp requested, ignore it.
        """
        if re_match_dict := self.access_logs_re.search(line):
            re_match_dict = re_match_dict.groupdict()
        else:
            logging.info(f"Skipping invalid request log entry: {line}")
            return
        timestamp = datetime.strptime(
            re_match_dict.get("timestamp"), "%d/%b/%Y:%H:%M:%S %z"
        ).strftime("%Y-%m-%d")
        max_date = self.end_date.strftime("%Y-%m-%d")
        earliest_date = self.start_date.strftime("%Y-%m-%d")
        if timestamp > max_date or timestamp < earliest_date:
            return
        ip_address = re_match_dict.get("ip_address")
        if not self.validate_ip_address(ip_address) or not re_match_dict:
            logging.info(f"Skipping invalid request log entry: {line}")
            return
        status_n_size = re_match_dict.get("status_and_size")
        response_code, content_length = status_n_size.split(" ", 1)
        response_code, content_length = int(response_code), int(content_length)
        url = self.validate_request(re_match_dict)
        if not url:
            logging.info(f"Skipping invalid request log entry: {line}")
            return
        return Request(
            ip_address,
            re_match_dict,
            self.url_prefix,
            url,
            response_code,
            content_length,
        )

    def validate_request(self, re_match_dict):
        """Make sure the request and url are correct.
        Sample: 'GET /test/books/e/10.5334/bbc HTTP/1.0'
        """
        pattern = r"^(GET|POST|PUT)\s+(/\S+)\s+HTTP/1\.\d$"
        request = re_match_dict.get("request")
        if re.match(pattern, request):
            _, url, _ = request.split()
            return url

    def validate_ip_address(self, ip_adrress):
        """Validate the ip_address using socket,
        Better approach than REGEX since would validate
        999.999.999.999"""
        try:
            socket.inet_aton(ip_adrress)
            return True
        except:
            return False

    def logfile_names(self) -> Iterator[str]:
        for path in sorted(os.listdir(self.log_dir)):
            """
            Generate a list of matching logfile names in the directory
            Note - can't assume logs start with 'access.log' - e.g. our log
            names have the format <service>_<code>_access.log-<datestamp>.gz
            Finally allow files whithin the range of a day before and a
            day after of the serch_date requested.
            """
            if "access.log" not in path or not path.endswith(".gz"):
                continue
            match_pattern = re.compile(
                r"(?P<year>\d{4})-?(?P<month>\d{2})-?(?P<day>\d{2})"
            )
            match = match_pattern.search(path)
            if match is None:
                raise AttributeError(
                    "Your file has to have a date at the end of it's name"
                )
            date_dict = match.groupdict()
            timestamp = (
                f"{date_dict['year']}-{date_dict['month']}"
                f"-{date_dict['day']}"
            )
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d")
                if timestamp > self.end_date or timestamp < self.start_date:
                    raise ValueError
            except ValueError:
                continue

            yield os.path.join(self.log_dir, path)

    def lines(self) -> str:
        """Read the logs file and return the lines splitted."""
        for logfile in self.logfile_names():
            with gzip.open(logfile, "r") as f:
                for line in f:
                    yield line.decode("utf-8")

    def relevant_requests(self) -> Iterator[tuple]:
        """Generate a filtered stream of requests; apply the predicate list
        `self.filters' to these requests; if any predicate fails, ignore
        the request and do not generate it for downstream processing."""
        if self.lines():
            for line in self.lines():
                if line_request := self.regex_match_line(line):
                    for filter_group in self.filter_groups:
                        measure_uri, filters, regex = filter_group
                        if not self.filter_in_line_request(
                            filters, line_request
                        ):
                            continue
                        line_request.sanitise_url(regex)
                        yield measure_uri, line_request
        else:
            logging.info("No file was processed")

    def filter_in_line_request(self, filters: list, line_request: str) -> bool:
        """If the filter from make_filters doesn't align with the line_request
        ignore the next iteration in the parent loop."""
        for f in filters:
            if not f(line_request):
                return False
        return True

    def __iter__(self):
        return self.relevant_requests()

    def return_output(self) -> list[tuple]:
        """Return the results from the filters."""
        return list(self)
