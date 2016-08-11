# Monkey patch bravado to work around null object values
# import bravado_core.unmarshal
# old_unmarshal_object = bravado_core.unmarshal.unmarshal_object
#
#
# def _unmarshal_object(swagger_spec, object_spec, object_value):
#     if object_value is None:
#         return None
#     return old_unmarshal_object(swagger_spec, object_spec, object_value)
#
# bravado_core.unmarshal.unmarshal_object = _unmarshal_object
# End monkey patch

from bravado.client import SwaggerClient

import pkg_resources
import yaml

###
# import requests
# import logging
#
# try:
#     import httplib
# except ImportError:
#     import http.client as httplib
#
# httplib.HTTPConnection.debuglevel = 1
#
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True
###

# Load the swagger from the resource file
with pkg_resources.resource_stream('dartclient', 'swagger.yaml') as f:
    spec_dict = yaml.load(f)

origin_url = 'http://dart.reporting.rmn.io/api/1'

config = {
#    'validate_swagger_spec': False,
#    'validate_requests': False,
#    'validate_responses': False,
#    'use_models': False
}

# Create the client so that we can get to the models and APIs.
# It's annoying that the creators of Bravado decided to do things
# in this way, since it makes it difficult to build a module that
# mimics the output of swagger-codegen
client = SwaggerClient.from_spec(spec_dict, origin_url=origin_url, config=config)

# import models into sdk package
Action = client.get_model('Action')
ActionContext = client.get_model('ActionContext')
ActionContextResponse = client.get_model('ActionContextResponse')
ActionData = client.get_model('ActionData')
ActionResponse = client.get_model('ActionResponse')
ActionResult = client.get_model('ActionResult')
ActionType = client.get_model('ActionType')
Column = client.get_model('Column')
DataFormat = client.get_model('DataFormat')
Dataset = client.get_model('Dataset')
DatasetData = client.get_model('DatasetData')
DatasetResponse = client.get_model('DatasetResponse')
Datastore = client.get_model('Datastore')
DatastoreData = client.get_model('DatastoreData')
DatastoreResponse = client.get_model('DatastoreResponse')
Engine = client.get_model('Engine')
EngineData = client.get_model('EngineData')
EngineResponse = client.get_model('EngineResponse')
ErrorResponse = client.get_model('ErrorResponse')
Event = client.get_model('Event')
EventData = client.get_model('EventData')
EventResponse = client.get_model('EventResponse')
Filter = client.get_model('Filter')
GraphEntity = client.get_model('GraphEntity')
GraphEntityIdentifier = client.get_model('GraphEntityIdentifier')
GraphEntityIdentifierResponse = client.get_model('GraphEntityIdentifierResponse')
GraphEntityIdentifiersResponse = client.get_model('GraphEntityIdentifiersResponse')
GraphEntityResponse = client.get_model('GraphEntityResponse')
JSONPatch = client.get_model('JSONPatch')
JSONSchema = client.get_model('JSONSchema')
JSONSchemaResponse = client.get_model('JSONSchemaResponse')
OKResponse = client.get_model('OKResponse')
ObjectResponse = client.get_model('ObjectResponse')
ObjectsResponse = client.get_model('ObjectsResponse')
OrderBy = client.get_model('OrderBy')
PagedActionsResponse = client.get_model('PagedActionsResponse')
PagedDatasetsResponse = client.get_model('PagedDatasetsResponse')
PagedDatastoresResponse = client.get_model('PagedDatastoresResponse')
PagedEnginesResponse = client.get_model('PagedEnginesResponse')
PagedEventsResponse = client.get_model('PagedEventsResponse')
PagedObjectsResponse = client.get_model('PagedObjectsResponse')
PagedSubscriptionElementsResponse = client.get_model('PagedSubscriptionElementsResponse')
PagedSubscriptionsResponse = client.get_model('PagedSubscriptionsResponse')
PagedTriggerTypesResponse = client.get_model('PagedTriggerTypesResponse')
PagedTriggersResponse = client.get_model('PagedTriggersResponse')
PagedWorkflowInstancesResponse = client.get_model('PagedWorkflowInstancesResponse')
PagedWorkflowsResponse = client.get_model('PagedWorkflowsResponse')
Subgraph = client.get_model('Subgraph')
SubgraphDefinition = client.get_model('SubgraphDefinition')
SubgraphDefinitionResponse = client.get_model('SubgraphDefinitionResponse')
SubgraphResponse = client.get_model('SubgraphResponse')
Subscription = client.get_model('Subscription')
SubscriptionData = client.get_model('SubscriptionData')
SubscriptionElement = client.get_model('SubscriptionElement')
SubscriptionResponse = client.get_model('SubscriptionResponse')
Trigger = client.get_model('Trigger')
TriggerData = client.get_model('TriggerData')
TriggerResponse = client.get_model('TriggerResponse')
TriggerType = client.get_model('TriggerType')
Workflow = client.get_model('Workflow')
WorkflowData = client.get_model('WorkflowData')
WorkflowInstance = client.get_model('WorkflowInstance')
WorkflowInstanceData = client.get_model('WorkflowInstanceData')
WorkflowInstanceResponse = client.get_model('WorkflowInstanceResponse')
WorkflowResponse = client.get_model('WorkflowResponse')

# import apis into sdk package
ActionApi = client.Action
DatasetApi = client.Dataset
DatastoreApi = client.Datastore
EngineApi = client.Engine
EventApi = client.Event
GraphApi = client.Graph
GraphEntityIdentifierApi = client.GraphEntityIdentifier
SchemaApi = client.Schema
SubgraphApi = client.Subgraph
SubgraphDefinitionApi = client.SubgraphDefinition
SubscriptionApi = client.Subscription
TriggerApi = client.Trigger
TriggerTypeApi = client.TriggerType
WorkflowApi = client.Workflow
WorkflowInstanceApi = client.WorkflowInstance


def debug_callback(response, operation):
    print(response.text)


DEBUG_ARGS = {
    '_request_options': {
        'response_callbacks': [
            debug_callback
        ]
    }
}


class SyncManager(object):
    """
    Provides convenient methods for synchronizing descriptions of the Dart workflow with the Dart server.
    """

    def __init__(self, client):
        self.client = client
        self.datastore_api = client.Datastore
        self.workflow_api = client.Workflow
        self.action_api = client.Action

    def sync_datastore(self, datastore_name, callback):
        """
        Synchronize a datastore with Dart.

        :param datastore_name: The name of the datastore.
        :param callback: A function with a signature (datastore) => datastore
        :return: The created or updated datastore.
        """
        response = self.datastore_api.listDatastores(filters='["name = %s"]' % (datastore_name,), limit=20, offset=0).result()
        if response.total > 0:
            datastore = callback(response.results[0])
            response = self.datastore_api.updateDatastore(datastore_id=datastore.id, datastore=datastore).result()
            return response.results
        else:
            datastore = callback(Datastore(data=DatastoreData()))
            response = self.datastore_api.createDatastore(datastore=datastore).result()
            return response.results

    def sync_workflow(self, workflow_name, datastore, callback):
        """
        Synchronize a workflow with Dart.

        :param workflow_name: The name of the workflow.
        :param datastore: The datastore containing the workflow.
        :param callback: A function with a signature (workflow) => workflow
        :return: The created or updated workflow.
        """
        response = self.workflow_api.listWorkflows(filters='["name = %s"]' % (workflow_name,), limit=20, offset=0).result()
        if response.total > 0:
            workflow = callback(response.results[0])
            response = self.workflow_api.updateWorkflow(workflow_id=workflow.id, workflow=workflow).result()
            return response.results
        else:
            workflow = callback(Workflow(data=WorkflowData()))
            workflow.data.datastore_id = datastore.id
            response = self.datastore_api.createDatastoreWorkflow(datastore_id=datastore.id, workflow=workflow).result()
            return response.results

    def sync_action(self, action_name, workflow, callback):
        response = ActionApi.listActions(filters='["name = %s"]' % (action_name,), limit=20, offset=0).result()
        if response.total > 0:
            action = callback(response.results[0])
            response = self.action_api.updateAction(action_id=action.id, action=action).result()
            return response.results
        else:
            action = callback(Action(data=ActionData()))
            response = self.workflow_api.createWorkflowActions(workflow_id=workflow.id, actions=[action]).result()
            return response.results


def create_sync_manager():
    return SyncManager(client=client)
