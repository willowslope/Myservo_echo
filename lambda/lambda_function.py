import paho.mqtt.publish as publish
import sys
import logging
import time
import getopt
import traceback
import uuid

#mTopic="item-test/device-1/test1"
mTopic="item-kuc/device-1/test1"
mMQTT_HostName="ec2-xx-xx-xx-xx.us-west-2.compute.amazonaws.com"

def lambda_handler(event, context):
    print('# Lambda-handler')
    print(event)
    if event['directive']['header']['namespace'] =='Alexa.Discovery':
        return handle_discovery_v3(event)
    elif event['directive']['header']['namespace'] == 'Alexa.PowerController':
        return handle_power_controller(event)
    elif event['directive']['header']['namespace'] == 'Alexa.Authorization':
        return handle_authorization(event)

#det proc_iotSender
def proc_iotSender( sPay ):
	try:
#		sPay="1"
		publish.single(topic=mTopic, payload=sPay, hostname=mMQTT_HostName , port=1883 )		
	except:
		print "--------------------------------------------"
		print traceback.format_exc(sys.exc_info()[2])
		print "--------------------------------------------" 
def handle_power_controller(request):
    request_name = request["directive"]["header"]["name"]
    if request_name == "TurnOn":
    	print('#turn on ')
    	proc_iotSender("1")
    	value = "ON"
    else:
    	print('#turn off ')
    	proc_iotSender("0")
    	value = "OFF"

    response = {
        "context": {
            "properties": [
                {
                    "namespace": "Alexa.PowerController",
                    "name": "powerState",
                    "value": value,
                    "timeOfSample": time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime()),
                    "uncertaintyInMilliseconds": 500
                }
            ]
        },
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "Response",
                    "payloadVersion": "3",
                    "messageId": str(uuid.uuid4()),
                    "correlationToken": request["directive"]["header"]["correlationToken"]
                },
                "endpoint": {
                    "scope": {
                        "type": "BearerToken",
                        "token": "access-token-from-Amazon"
                    },
                    "endpointId": request["directive"]["endpoint"]["endpointId"]
                },
                "payload": {}
            }
        }
    return response

def handle_authorization(request):
    request_name = request["directive"]["header"]["name"]
    if request_name == "AcceptGrant":
        response = {
            "event": {
                "header": {
                    "namespace": "Alexa.Authorization",
                    "name": "AcceptGrant.Response",
                    "payloadVersion": "3",
                    "messageId": "5f8a426e-01e4-4cc9-8b79-65f8bd0fd8a4"
                },
                "payload": {}
            }
        }
        return response


def handle_discovery_v3(request):
    endpoint = {
        "endpointId": "device001",
        "manufacturerName": "yourManufacturerName",
        "friendlyName": "Smart Home Virtual Device",
        "description": "Virtual Device for the Sample Hello World Skill",
        "displayCategories": ["OTHER"],
        "cookie": 
        {
             "extraDetail1":"optionalDetailForSkillAdapterToReferenceThisDevice",
             "extraDetail2":"There can be multiple entries",
             "extraDetail3":"but they should only be used for reference purposes.",
             "extraDetail4":"This is not a suitable place to maintain current device state"
        },
        "capabilities": [
        {
            "type": "AlexaInterface",
            "interface": "Alexa.PowerController",
            "version": "3",
            "properties": {
                "supported": [
                    { "name": "powerState" }
                ],
                "proactivelyReported": True,
                "retrievable": True
            }
        },
        {
            "type": "AlexaInterface",
            "interface": "Alexa.EndpointHealth",
            "version": "3",
            "properties": {
                "supported":[{ "name":"connectivity" }],
                "proactivelyReported": True,
                "retrievable": True
            }
        },
        {
            "type": "AlexaInterface",
            "interface": "Alexa",
            "version": "3"
        }]
    }

    endpoints = []
    endpoints.append(endpoint)

    response = {
        "event": {
            "header": {
                "namespace": "Alexa.Discovery",
                "name": "Discover.Response",
                "payloadVersion": "3",
                "messageId": str(uuid.uuid4())
            },
            "payload": {
                "endpoints": endpoints
            }
        }
    }
    return response
def handleDiscovery(context, event):
    print('# Discovery')
#    proc_iotSender()
    payload = ''
    header = {
        "namespace": "Alexa.ConnectedHome.Discovery",
        "name": "DiscoverAppliancesResponse",
        "payloadVersion": "2"
        }

#    if event['header']['name'] == 'DiscoverAppliancesRequest':
    if 1:
        payload = {
            "discoveredAppliances":[
                {
                    "applianceId":"device001",
                    "manufacturerName":"yourManufacturerName",
                    "modelName":"model 01",
                    "version":"your software version number here.",
                    "friendlyName":"Smart Home Virtual Device",
                    "friendlyDescription":"Virtual Device for the Sample Hello World Skill",
                    "isReachable":True,
                    "actions":[
                        "turnOn",
                        "turnOff"
                    ],
                    "additionalApplianceDetails":{
                        "extraDetail1":"optionalDetailForSkillAdapterToReferenceThisDevice",
                        "extraDetail2":"There can be multiple entries",
                        "extraDetail3":"but they should only be used for reference purposes.",
                        "extraDetail4":"This is not a suitable place to maintain current device state"
                    }
                }
            ]
        }
    return { 'header': header, 'payload': payload }

def handleControl(context, event):
    print('# control_device ')
    payload = ''
    device_id = event['payload']['appliance']['applianceId']
    message_id = event['header']['messageId']
    
    name=''
    if event['header']['name'] == 'TurnOnRequest':
    	print('#turn on ' + event['payload']['appliance']['applianceId'])
    	proc_iotSender("1")
        payload = { }
        name='TurnOnConfirmation'
        
    if event['header']['name'] == 'TurnOffRequest':
    	print('#turn off ' + event['payload']['appliance']['applianceId'])
    	proc_iotSender("0")
        payload = ''
        name='TurnOffConfirmation'

    header = {
        "namespace": event['header']['namespace'],
        "name": name,
        "payloadVersion": event['header']['payloadVersion'],
        "messageId": message_id
        }
        
#   header = {
#       "namespace":"Alexa.ConnectedHome.Control",
#       "name":"TurnOnConfirmation",
#       "payloadVersion":"2",
#       "messageId": message_id
#       }
    return { 'header': header, 'payload': payload }

