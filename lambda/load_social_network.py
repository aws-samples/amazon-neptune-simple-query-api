import os
from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection

# https://github.com/aws-samples/amazon-neptune-samples/blob/master/neptune-sagemaker/notebooks/Getting-Started/03-Social-Network-Recommendations.ipynb

NEPTUNE_DOMAIN = os.environ['NEPTUNE_DOMAIN']

def handler(_event, _context):
    remoteConn = DriverRemoteConnection(f'wss://{NEPTUNE_DOMAIN}:8182/gremlin','g')

    g = Graph().traversal().withRemote(remoteConn)
    g. \
        addV('User').property('name','Bill').property('birthdate', '1988-03-22'). \
        addV('User').property('name','Sarah').property('birthdate', '1992-05-03'). \
        addV('User').property('name','Ben').property('birthdate', '1989-10-21'). \
        addV('User').property('name','Lucy').property('birthdate', '1998-01-17'). \
        addV('User').property('name','Colin').property('birthdate', '2001-08-14'). \
        addV('User').property('name','Emily').property('birthdate', '1998-03-05'). \
        addV('User').property('name','Gordon').property('birthdate', '2002-12-04'). \
        addV('User').property('name','Kate').property('birthdate', '1995-02-12'). \
        addV('User').property('name','Peter').property('birthdate', '2001-02-27'). \
        addV('User').property('name','Terry').property('birthdate', '1989-10-02'). \
        addV('User').property('name','Alistair').property('birthdate', '1992-06-30'). \
        addV('User').property('name','Eve').property('birthdate', '2000-05-13'). \
        addV('User').property('name','Gary').property('birthdate', '1998-09-20'). \
        addV('User').property('name','Mary').property('birthdate', '1997-01-27'). \
        addV('User').property('name','Charlie').property('birthdate', '1989-11-02'). \
        addV('User').property('name','Sue').property('birthdate', '1994-03-08'). \
        addV('User').property('name','Arnold').property('birthdate', '2002-07-23'). \
        addV('User').property('name','Chloe').property('birthdate', '1988-11-04'). \
        addV('User').property('name','Henry').property('birthdate', '1996-03-15'). \
        addV('User').property('name','Josie').property('birthdate', '2003-08-21'). \
        V().hasLabel('User').has('name','Sarah').as_('a').V().hasLabel('User').has('name','Bill').addE('FRIEND').to('a').property('strength',1). \
        V().hasLabel('User').has('name','Colin').as_('a').V().hasLabel('User').has('name','Bill').addE('FRIEND').to('a').property('strength',2). \
        V().hasLabel('User').has('name','Terry').as_('a').V().hasLabel('User').has('name','Bill').addE('FRIEND').to('a').property('strength',3). \
        V().hasLabel('User').has('name','Peter').as_('a').V().hasLabel('User').has('name','Colin').addE('FRIEND').to('a').property('strength',1). \
        V().hasLabel('User').has('name','Kate').as_('a').V().hasLabel('User').has('name','Ben').addE('FRIEND').to('a').property('strength',2). \
        V().hasLabel('User').has('name','Kate').as_('a').V().hasLabel('User').has('name','Lucy').addE('FRIEND').to('a').property('strength',3). \
        V().hasLabel('User').has('name','Eve').as_('a').V().hasLabel('User').has('name','Lucy').addE('FRIEND').to('a').property('strength',1). \
        V().hasLabel('User').has('name','Alistair').as_('a').V().hasLabel('User').has('name','Kate').addE('FRIEND').to('a').property('strength',2). \
        V().hasLabel('User').has('name','Gary').as_('a').V().hasLabel('User').has('name','Colin').addE('FRIEND').to('a').property('strength',3). \
        V().hasLabel('User').has('name','Gordon').as_('a').V().hasLabel('User').has('name','Emily').addE('FRIEND').to('a').property('strength',1). \
        V().hasLabel('User').has('name','Alistair').as_('a').V().hasLabel('User').has('name','Emily').addE('FRIEND').to('a').property('strength',3). \
        V().hasLabel('User').has('name','Terry').as_('a').V().hasLabel('User').has('name','Gordon').addE('FRIEND').to('a').property('strength',3). \
        V().hasLabel('User').has('name','Alistair').as_('a').V().hasLabel('User').has('name','Terry').addE('FRIEND').to('a').property('strength',1). \
        V().hasLabel('User').has('name','Gary').as_('a').V().hasLabel('User').has('name','Terry').addE('FRIEND').to('a').property('strength',2). \
        V().hasLabel('User').has('name','Mary').as_('a').V().hasLabel('User').has('name','Terry').addE('FRIEND').to('a').property('strength',3). \
        V().hasLabel('User').has('name','Henry').as_('a').V().hasLabel('User').has('name','Alistair').addE('FRIEND').to('a').property('strength',1). \
        V().hasLabel('User').has('name','Sue').as_('a').V().hasLabel('User').has('name','Eve').addE('FRIEND').to('a').property('strength',2). \
        V().hasLabel('User').has('name','Sue').as_('a').V().hasLabel('User').has('name','Charlie').addE('FRIEND').to('a').property('strength',3). \
        V().hasLabel('User').has('name','Josie').as_('a').V().hasLabel('User').has('name','Charlie').addE('FRIEND').to('a').property('strength',1). \
        V().hasLabel('User').has('name','Henry').as_('a').V().hasLabel('User').has('name','Charlie').addE('FRIEND').to('a').property('strength',2). \
        V().hasLabel('User').has('name','Henry').as_('a').V().hasLabel('User').has('name','Mary').addE('FRIEND').to('a').property('strength',3). \
        V().hasLabel('User').has('name','Mary').as_('a').V().hasLabel('User').has('name','Gary').addE('FRIEND').to('a').property('strength',1). \
        V().hasLabel('User').has('name','Henry').as_('a').V().hasLabel('User').has('name','Gary').addE('FRIEND').to('a').property('strength',2). \
        V().hasLabel('User').has('name','Chloe').as_('a').V().hasLabel('User').has('name','Gary').addE('FRIEND').to('a').property('strength',3). \
        V().hasLabel('User').has('name','Henry').as_('a').V().hasLabel('User').has('name','Arnold').addE('FRIEND').to('a').property('strength',1). \
        next()

    remoteConn.close()
