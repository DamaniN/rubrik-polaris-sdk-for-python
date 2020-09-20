# assign_sla

Assign a Rubrik object to an SLA Domain.

```py
def assign_sla(self, object_name, sla_name, object_type, log_backup_frequency_in_seconds=None, log_retention_hours=None, copy_only=None, windows_host=None, nas_host=None, share=None, log_backup_frequency_in_minutes=None, num_channels=4, hostname=None, timeout=30):
```

## Arguments

| Name        | Type | Description                                                                 | Choices |
|-------------|------|-----------------------------------------------------------------------------|---------|
| object_name  | str or list | The name of the Rubrik object you wish to assign to an SLA Domain. When the 'object_type' is 'volume_group', the object_name can be a list of volumes. |  |
| sla_name  | str | The name of the SLA Domain you wish to assign an object to. To exclude the object from all SLA assignments use `do not protect` as the `sla_name`. To assign the selected object to the SLA of the next higher level object use `clear` as the `sla_name`. |  |
| object_type  | str | The Rubrik object type you want to assign to the SLA Domain.  | ahv, mssql_host, oracle_host, vmware, volume_group |

## Keyword Arguments

| Name        | Type | Description                                                                 | Choices | Default |
|-------------|------|-----------------------------------------------------------------------------|---------|---------|
| log_backup_frequency_in_seconds  | int | The MSSQL Log Backup frequency you'd like to specify with the SLA. Required when the `object_type` is `mssql_host`. (default {None}) |  |  |
| log_retention_hours  | int | The MSSQL or Oracle Log Retention frequency you'd like to specify with the SLA. Required when the `object_type` is `mssql_host`, `oracle_db` or 'oracle_host'. (default {None}) |  |  |
| copy_only  | bool | Take Copy Only Backups with MSSQL. Required when the `object_type` is `mssql_host`. (default {None}) |  |  |
| windows_host  | str | The name of the Windows host that contains the relevant volume group. Required when the `object_type` is `volume_group`. (default {None}) |  |  |
| nas_host  | str | The name of the NAS host that contains the relevant share. Required when the `object_type` is `fileset`. (default {None}) |  |  |
| share  | str | The name of the network share a fileset will be created for. Required when the `object_type` is `fileset`. (default {None}) |  |  |
| log_backup_frequency_in_minutes  | int |  - The Oracle Log Backup frequency you'd like to specify with the SLA. Required when the `object_type` is `oracle_db` or `oracle_host`. (default {None}) |  |  |
| num_channels  | int |  - Number of RMAN channels used to backup the Oracle database. Required when the `object_type` is `oracle_host`. (default {"4""}) |  |  |
| hostname  | str | The hostname, or one of the hostnames in a RAC cluster, or the RAC cluster name. Required when the object_type is `oracle_db`. (default {None}) |  |  |
| timeout  | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error.  |  | 30 |

## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| str | No change required. The vSphere VM '`object_name`' is already assigned to the '`sla_name`' SLA Domain. |
| str | No change required. The MSSQL Instance '`object_name`' is already assigned to the '`sla_name`' SLA Domain with the following log settings: log_backup_frequency_in_seconds: `log_backup_frequency_in_seconds`, log_retention_hours: `log_retention_hours` and copy_only: `copy_only` |
| str | No change required. The Oracle Database '`object_name`' is already assigned to the '`sla_name`' SLA Domain with the following log settings: log_backup_frequency_in_minutes: `log_backup_frequency_in_seconds`, log_retention_hours: `log_retention_hours` and num_channels: `num_channels`. |
| str | No change required. The Oracle Host '`object_name`' is already assigned to the '`sla_name`' SLA Domain with the following log settings: log_backup_frequency_in_seconds: `log_backup_frequency_in_seconds`. log_retention_hours: `log_retention_hours`, and num_channels: `num_channels` |
| str | No change required. The '`object_name`' volume_group is already assigned to the '`sla_name`' SLA Domain. |
| dict | The full API response for `POST /internal/sla_domain/{sla_id}/assign`. |
| dict | The full API response for `PATCH /internal/volume_group/{id}`. |
| dict | The full API response for `PATCH /internal/oracle/db/{id}.` |
| dict | The full API response for `PATCH /internal/oracle/host/{id}`. |



## Example

```py
# VMware

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

vm_name = "python-sdk-demo"
sla_name = "Gold"
object_type = "vmware"

assign_sla = rubrik.assign_sla(vm_name, sla_name, object_type)


# MSSQL


rubrik = rubrik_cdm.Connect()

object_name = 'python-sdk.demo.com'
object_type = 'mssql_host'

sla_name = 'Gold'
log_backup_frequency_in_seconds = 600
log_retention_hours = 12
copy_only = False

assignsla = rubrik.assign_sla(
    object_name,
    sla_name,
    object_type,
    logBackupFrequencyInSeconds,
    logRetentionHours,
    copyOnly)


# Oracle Database


import rubrik_cdm

rubrik = rubrik_cdm.Connect()

object_name = 'HRDB50'
object_type = 'oracle_db'
hostname = 'python-sdk.demo.com'

sla_name = 'Gold'
log_backup_frequency_in_minutes = 30
log_retention_hours = 720
num_channels = 4

assignsla = rubrik.assign_sla(
    object_name, 
    sla_name, 
    object_type, 
    log_backup_frequency_in_minutes=log_backup_frequency_in_minutes, 
    log_retention_hours=log_retention_hours, 
    num_channels=num_channels,
    hostname=hostname)


# Oracle Host


import rubrik_cdm

rubrik = rubrik_cdm.Connect()

object_name = 'python-sdk.demo.com'
object_type = 'oracle_host'

sla_name = 'Gold'
log_backup_frequency_in_minutes = 30
log_retention_hours = 720
num_channels = 4

assignsla = rubrik.assign_sla(
    object_name, 
    sla_name, 
    object_type, 
    log_backup_frequency_in_minutes=log_backup_frequency_in_minutes, 
    log_retention_hours=log_retention_hours, 
    num_channels=num_channels)


# Volume Group


rubrik = rubrik_cdm.Connect()

# Note: To escape the "\" character, you need to use an extra "\". In
# other words, the "C:\" volume is shown as "C:\\" in the Python code.
object_name = ["C:\\", "D:\\"]
windows_host = "windows2016.rubrik.com"
sla_name = "Gold"

assign_sla = rubrik.assign_sla(object_name, sla_name, "volume_group", windows_host=windows_host)


# Fileset


rubrik = rubrik_cdm.Connect()

object_name = 'nas_fileset'
object_type = 'fileset'

sla_name = 'Gold'
nas_host = 'nas-server.rubrik.com'
share = '/nas_share'

assign_sla = rubrik.assign_sla(object_name, sla_name, object_type, nas_host=nas_host, share=share)

```
