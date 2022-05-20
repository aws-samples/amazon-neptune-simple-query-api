import os
import json
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import *
from gremlin_python.process.anonymous_traversal import *
from gremlin_python.process.strategies import *

NEPTUNE_DOMAIN = os.environ['NEPTUNE_DOMAIN']

def handler(event, _context):
    queryStringParams = event['queryStringParameters']

    if 'target_user' not in queryStringParams:
        return {
            'statusCode': 400,
            'body': json.dumps({ 'error': 'target_user must be specified.' }),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
        }

    targetUser = queryStringParams['target_user']

    remoteConn = DriverRemoteConnection(f'wss://{NEPTUNE_DOMAIN}:8182/gremlin','g')

    g = Graph().traversal().withRemote(remoteConn)

    recommendations = g.V().hasLabel('User').has('name', targetUser).as_('user'). \
        both('FRIEND').aggregate('friends'). \
        both('FRIEND'). \
        where(P.neq('user')).where(P.without('friends')). \
        groupCount().by('name'). \
        order(Scope.local).by(Column.values, Order.desc). \
        next()

    remoteConn.close()

    return {
        'statusCode': 200,
        'body': json.dumps(recommendations),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
    }
