# Copyright 2020 Rubrik, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import logging
import os
import re

import urllib3

from .exceptions import InvalidParameterException

import pprint

pp = pprint.PrettyPrinter(indent=4)


class PolarisClient():
    from .common.connection import query, get_access_token as _get_access_token

    def __init__(self, domain, username, password, enable_logging=False, logging_level="debug", **kwargs):
        from .common.graphql import build_graphql_maps

        # Enable logging for the SDK
        valid_logging_levels = {
            "debug": logging.DEBUG,
            "critical": logging.CRITICAL,
            "error": logging.ERROR,
            "warning": logging.WARNING,
            "info": logging.INFO,
        }
        if logging_level not in valid_logging_levels:
            raise InvalidParameterException(
                "'{}' is not a valid logging_level. Valid choices are 'debug', 'critical', 'error', 'warning', "
                "or 'info'.".format(
                    logging_level))
        self.logging_level = logging_level
        if enable_logging:
            logging.getLogger().setLevel(valid_logging_levels[self.logging_level])

        # Set base variables
        self.kwargs = kwargs
        self.domain = domain
        self.username = username
        self.password = password
        self.module_path = os.path.dirname(os.path.realpath(__file__))
        self.data_path = "{}/data/".format(self.module_path)
        self._log("Polaris Domain: {}".format(self.domain))

        # Switch off SSL checks if needed
        if 'insecure' in self.kwargs and self.kwargs['insecure']:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Adjust Polaris domain if a custom root is defined
        if 'root_domain' in kwargs and kwargs['root_domain'] is not None:
            self.baseurl = "https://{}.{}/api/graphql".format(self.domain, self.kwargs['root_domain'])
        else:
            self.baseurl = "https://{}.my.rubrik.com/api/graphql".format(self.domain)

        # Get Auth Token and assemble header
        self.access_token = self._get_access_token()
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.access_token
        }

        # Get graphql content
        (self.graphql_query, self.graphql_mutation, self.graphql_file_type_map) = build_graphql_maps(self)

    def get_sla_domains(self, sla_domain_name = ""):
        """Retrieves dictionary of SLA Domain Names and Identifiers,
           or the ID of a single SLA Domain

        Arguments:
            sla_domain_name {str} -- Rubrik SLA Domain Name

       """
        query_name = "sla_domains"
        variables = {
            "filter": {
                "field": "NAME",
                "text" : sla_domain_name
            }
        }
        request = self.query(None, self.graphql_query[query_name], variables)
        request_nodes = self._dump_nodes(request, query_name)
        if sla_domain_name and len(request_nodes) == 1:
            return request_nodes[0]['id']
        else:
            return request_nodes

    def get_accounts_aws(self, filter=""):
        """Retrieves AWS account information from Polaris
        """
        query_name = "accounts_aws"
        variables = {
            "filter": filter
        }
        request = self.query(None, self.graphql_query[query_name], variables)
        return self._dump_nodes(request, query_name)

    def get_accounts_gcp(self, filter=""):
        """Retrieves GCP account information from Polaris

        Arguments:
            filter {str} -- Search string to filter results
        """
        query_name = "accounts_gcp"
        variables = {
            "filter": filter
        }
        request = self.query(None, self.graphql_query[query_name], variables)
        return self._dump_nodes(request, query_name)

    def get_accounts_azure(self, filter=""):
        """Retrieves Azure account information from Polaris

        Arguments:
            filter {str} -- Search string to filter results
        """
        query_name = "accounts_azure"
        variables = {
            "filter": filter
        }
        request = self.query(None, self.graphql_query[query_name], variables)
        return self._dump_nodes(request, query_name)

    def submit_on_demand(self, object_ids, sla_id):
        """Submits On Demand Snapshot

        Arguments:
            object_ids [string] -- Array of Rubrik Object IDs
            sla_id string -- Rubrik SLA Domain ID
        """
        mutation_name = "on_demand"
        variables = {
            "objectIds": object_ids,
            "slaId": sla_id
        }
        request = self.query(None, self.graphql_mutation[mutation_name], variables)
        return request

    def submit_assign_sla(self, object_ids, sla_id):
        """Submits a Rubrik SLA change for objects

        Arguments:
            object_ids [string] -- Array of Rubrik Object IDs
            sla_id string -- Rubrik SLA Domain ID
        """
        mutation_name = "assign_sla"
        variables = {
            "objectIds": object_ids,
            "slaId": sla_id
        }
        request = self.query(None, self.graphql_mutation[mutation_name], variables)
        return request

    def get_object_ids_ec2(self, match_all = True, **kwargs):
        """Retrieves all EC2 objects that match query

        Arguments:
            match_all bool -- Set to false to match ANY defined criteria
            kwargs -- Any top level object from the get_instances_ec2 call
        """
        o = []
        for instance in self.get_instances_ec2():
            t = len(kwargs)
            if 'tags' in kwargs:
                t = t + len(kwargs['tags']) - 1
            c = t
            for key in kwargs:
                if key is 'tags' and 'tags' in instance:
                    for instance_tag in instance['tags']:
                        if instance_tag['key'] in kwargs['tags'] and instance_tag['value'] == kwargs['tags'][
                                                                                              instance_tag['key']]:
                            c -= 1
                elif key in instance and instance[key] ==  kwargs[key]:
                    c -= 1
            if match_all and bool(c) is False:
                o.append(instance['id'])
            elif not match_all and c < t and bool(c) is True :
                o.append(instance['id'])
        return o

    def get_object_ids_azure(self, match_all = True, **kwargs):
        """Retrieves all Azure objects that match query

        Arguments:
            match_all bool -- Set to false to match ANY defined criteria
            kwargs -- Any top level object from the get_instances_ec2 call
        """
        o = []
        for instance in self.get_instances_azure():
            t = len(kwargs)
            c = t
            for key in kwargs:
                if key in instance and instance[key] ==  kwargs[key]:
                    c -= 1
            if match_all and bool(c) is False:
                o.append(instance['id'])
            elif not match_all and c < t and bool(c) is True :
                o.append(instance['id'])
        return o

    def get_object_ids_gce(self, match_all = True, **kwargs):
        """Retrieves all Azure objects that match query

        Arguments:
            match_all bool -- Set to false to match ANY defined criteria
            kwargs -- Any top level object from the get_instances_ec2 call
        """
        o = []
        for instance in self.get_instances_gce():
            t = len(kwargs)
            c = t
            for key in kwargs:
                if key in instance and instance[key] ==  kwargs[key]:
                    c -= 1
            if match_all and bool(c) is False:
                o.append(instance['id'])
            elif not match_all and c < t and bool(c) is True :
                o.append(instance['id'])
        return o

    def get_instances_ec2(self):
        query_name = "instances_ec2"
        request = self.query(None, self.graphql_query[query_name], None)
        return self._dump_nodes(request, query_name)

    def get_instances_azure(self):
        query_name = "instances_azure"
        request = self.query(None, self.graphql_query[query_name], None)
        return self._dump_nodes(request, query_name)

    def get_instances_gce(self):
        query_name = "instances_gce"
        request = self.query(None, self.graphql_query[query_name], None)
        return self._dump_nodes(request, query_name)

    def schema(self):
        query = """
            fragment FullType on __Type {
                kind
                name
                fields(includeDeprecated: true) {
                    name
                    args {
                        ...InputValue
                    }
                    type {
                        ...TypeRef
                    }
                    isDeprecated
                    deprecationReason
                }
                inputFields {
                    ...InputValue
                }
                interfaces {
                    ...TypeRef
                }
                enumValues(includeDeprecated: true) {
                    name
                    isDeprecated
                    deprecationReason
                }
                possibleTypes {
                    ...TypeRef
                }
            }
            fragment InputValue on __InputValue {
                name
                type {
                    ...TypeRef
                }
                defaultValue
            }
            fragment TypeRef on __Type {
                kind
                name
                ofType {
                    kind
                    name
                    ofType {
                        kind
                        name
                        ofType {
                            kind
                            name
                            ofType {
                                kind
                                name
                                ofType {
                                    kind
                                    name
                                    ofType {
                                        kind
                                        name
                                        ofType {
                                            kind
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            query IntrospectionQuery {
                __schema {
                    queryType {
                        name
                    }
                    mutationType {
                        name
                    }
                    types {
                        ...FullType
                    }
                    directives {
                        name
                        locations
                        args {
                            ...InputValue
                        }
                    }
                }
            }
            """
        return self.query(query=query)

    # Private

    def _get_query_names_from_graphql_query(self, _graphql_query_text):
        o = re.findall(r'(\S+) ?\(.*\)', _graphql_query_text)
        return o

    def _dump_nodes(self, request, query_name):
        o = []
        for query_returned in request['data']:
            if query_returned in self.graphql_file_type_map[query_name]:
                for node_returned in request['data'][query_returned]['edges']:
                    o.append(node_returned['node'])
        return o



    def _log(self, log_message):
        """Create properly formatted debug log messages.

        Arguments:
            log_message {str} -- The message to pass to the debug log.
        """

        log = logging.getLogger(__name__)

        set_logging = {
            "debug": log.debug,
            "critical": log.critical,
            "error": log.error,
            "warning": log.warning,
            "info": log.info

        }
        set_logging[self.logging_level](log_message)
