import gns3fy
from time import sleep
TESTBED_SERVER_NAME = 'sandbox-server'
VYOS_TEMPLATE_NAME = 'VyOS'

def create_node(name, template, gns3_project):
    try:
        gns3_project.create_node(name=name, template=template)
    except:
        print('JSON Schema handled')

# Define the server object to establish the connection
gns3_server = gns3fy.Gns3Connector("http://localhost:3080")
project = gns3fy.Project(name='MgrMain', connector=gns3_server)
try:
    project.get()
    project_to_delete_id = project.project_id
    gns3_server.delete_project(project_to_delete_id)
except:
    print('Project does not exist')
gns3_server.create_project(name='MgrMain')
project = gns3fy.Project(name='MgrMain', connector=gns3_server)
project.get()
project_id = project.project_id
print(project_id)
gns3_server.templates_summary(is_print=True)
create_node('TestBed Server', TESTBED_SERVER_NAME,project)
create_node('R1',VYOS_TEMPLATE_NAME, project)
sleep(2)
project.get()
nodes = gns3_server.get_nodes(project_id=project_id)
node1 = nodes[0]
node2 = nodes[1]
project = gns3fy.Project(name='MgrMain', connector=gns3_server)
project.get()
project.create_link(node1['name'], node1['ports'][0]['name'], node2['name'], node2['ports'][0]['name'])
print(node2)





