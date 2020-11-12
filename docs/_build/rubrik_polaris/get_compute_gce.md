# get_compute_gce

Retrieve all GCE instances from Polaris

```py
def get_compute_gce(self):
```



## Returns

| Type | Return Value                                                                                  |
|------|-----------------------------------------------------------------------------------------------|
| list | List of all GCE instances |



## Example

```py
from rubrik_polaris import PolarisClient


domain = 'my-company'
username = 'john.doe@example.com'
password = 's3cr3tP_a55w0R)'


client = PolarisClient(domain, username, password, insecure=True)

# Search for a set of objects and get their details
for i in client.get_compute_object_ids_gce():
    print(client.get_compute_gce(i))

```
