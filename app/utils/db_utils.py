from .common import get_request_host, get_mapped_records
from .constants import Key, Config


def get_connection(self, data_source_key):
    if data_source_key:
        mysql_connections = self.application.mysql_connections
        if data_source_key in mysql_connections:
            return mysql_connections[data_source_key]
        else:
            raise RuntimeError(f"Could not find connection with '{data_source_key}'")
    else:
        raise ValueError("Null data source key received")
