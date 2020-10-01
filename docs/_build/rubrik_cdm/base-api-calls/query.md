# query

Send a GraphQL query to a CDM cluster.

```python
def query(self, query, operation_name=None, variables=None, timeout=15, authentication=True):
```

## Arguments

| Name | Type | Description | Choices |
| :--- | :--- | :--- | :--- |
| query | str | The main GraphQL query body. |  |
| operation\_name | str | A meaningful and explicit name for your GraphQL operation. Think of this just like a function name in your favorite programming language. \(default: {None}\) |  |
| variables | dict | The variables to pass into your query. \(default: {None}\) |  |

## Keyword Arguments

| Name | Type | Description | Choices | Default |
| :--- | :--- | :--- | :--- | :--- |
| timeout | int | The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. |  | 15 |
| authentication | bool | Flag that specifies whether or not to utilize authentication when making the API call. |  | True |

## Returns

| Type | Return Value |
| :--- | :--- |
| dict | The response\["data"\] body of the API call. |

## Example

```python
### Query only

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

query = """
{
  cluster(id: "me") {
    version
  }
}
"""

cluster_details = rubrik.query(query)

### All parameters used

import rubrik_cdm

rubrik = rubrik_cdm.Connect()

operation_name = "ClusterDetails"

query = """
ClusterDetails($clusterID: String!) {
  cluster(id: $clusterID) {
    version
  }
}
"""

variables = {
    "clusterID": "me"
}

cluster_details = rubrik.query(query, operation_name, variables)
```

