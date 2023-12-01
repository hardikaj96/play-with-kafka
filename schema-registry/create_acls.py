from confluent_kafka.admin import AdminClient, AclOperation, AclPermissionType, ResourceType, ResourcePatternType,AclBinding

a = AdminClient({'bootstrap.servers': 'localhost:19092'})
acl_binding = AclBinding(ResourceType.TOPIC, 'mytopic', ResourcePatternType.LITERAL, 'User:Alice', '*', AclOperation.READ, AclPermissionType.ALLOW)
f = a.create_acls([acl_binding])


# Wait for the operation to finish.
try:
#    f.result() # The result itself is None

   print(f)
   print("ACL created")
except Exception as e:
   print("Failed to create ACL: {}".format(e))
