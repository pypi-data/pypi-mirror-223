from collections.abc import Sequence
from typing import Optional

from atoti._docs_utils import STANDARD_EXTERNAL_TABLE_OPTIONS_KWARGS
from atoti.directquery._clustering_columns_parameter import CLUSTERING_COLUMNS_PARAMETER
from atoti.directquery._external_table_options import ExternalTableOptions
from atoti_core import doc

from .table import DatabricksTable


class DatabricksTableOptions(ExternalTableOptions[DatabricksTable]):
    @doc(**STANDARD_EXTERNAL_TABLE_OPTIONS_KWARGS)
    def __init__(
        self,
        *,
        clustering_columns: Sequence[str] = (),
        keys: Optional[Sequence[str]] = None,
    ) -> None:
        """Additional options about the external table to create.

        Args:
            {clustering_columns}
            {keys}

        Example:
            .. doctest::
                :hide:

                >>> import os
                >>> from atoti_directquery_databricks import DatabricksConnectionInfo
                >>> connection_info = DatabricksConnectionInfo(
                ...     "jdbc:databricks://"
                ...     + os.environ["DATABRICKS_SERVER_HOSTNAME"]
                ...     + "/default;"
                ...     + "transportMode=http;"
                ...     + "ssl=1;"
                ...     + "httpPath="
                ...     + os.environ["DATABRICKS_HTTP_PATH"]
                ...     + ";"
                ...     + "AuthMech=3;"
                ...     + "UID=token;",
                ...     password=os.environ["DATABRICKS_AUTH_TOKEN"],
                ... )
                >>> external_database = session.connect_to_external_database(
                ...     connection_info
                ... )

            .. doctest::

                >>> from atoti_directquery_databricks import (
                ...     DatabricksTableOptions,
                ... )
                >>> external_table = external_database.tables["tutorial", "sales"]
                >>> table = session.add_external_table(
                ...     external_table,
                ...     table_name="sales_renamed",
                ...     options=DatabricksTableOptions(keys=["SALE_ID"]),
                ... )
        """
        super().__init__(
            keys=keys,
            options={
                CLUSTERING_COLUMNS_PARAMETER: clustering_columns
                if clustering_columns
                else None
            },
        )
