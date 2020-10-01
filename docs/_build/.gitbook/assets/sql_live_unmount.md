# sql_live_unmount

Delete a Microsoft SQL Live Mount from the Rubrik cluster.

```py
def sql_live_unmount(self, mounted_db_name, sql_instance=None, sql_host=None, force=False, timeout=30):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| mounted_db_name  | str | The name of the Live Mounted database to be unmounted. |  |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| sql_instance  | str | The name of the MSSQL instance managing the Live Mounted database to be unmounted. |  |  |
| sql_host  | str | The name of the MSSQL host running the Live Mounted database to be unmounted. |  |  |
| force  | bool | Remove all graphql within the Rubrik cluster related to the Live Mount, even if the SQL Server database cannot be contacted.  |  | False |
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 30 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| dict | The full response of `DELETE /mssql/db/mount/{id}?force={bool}`. |



## Example

```py
import rubrik_cdm

rubrik = rubrik_cdm.Connect()

mounted_db_name = "python-sdk-demo"
sql_instance = 'MSSQLSERVER'
sql_host = 'sql.rubrikdemo.com'

live_unmount = rubrik.sql_live_unmount(mounted_db_name, sql_instance, sql_host)

```
