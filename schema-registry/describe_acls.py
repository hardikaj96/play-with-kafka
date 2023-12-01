from confluent_kafka.admin import AdminClient, AclOperation, AclPermissionType, ResourceType, ResourcePatternType,AclBinding, AclBindingFilter

a = AdminClient({'bootstrap.servers': 'localhost:19092'})
acl_binding = AclBinding(ResourceType.TOPIC, 'mytopic', ResourcePatternType.LITERAL, 'User:Alice', '*', AclOperation.READ, AclPermissionType.ALLOW)
f = a.create_acls([acl_binding])

filter = AclBindingFilter(ResourceType.TOPIC, 'mytopic', ResourcePatternType.LITERAL, 'User:Alice', '*', AclOperation.ANY, AclPermissionType.ANY)
fs = a.describe_acls(filter)
print(fs)
# # Wait for each operation to finish.
# for acl_binding, f in fs.items():
#     try:
#         # f.result() # The result itself is None
#         print(f)
#         print("ACL: {}".format(acl_binding))
#     except Exception as e:
#         print("Failed to describe ACL: {}".format(e))

try:
    acls = fs.result() # The result is a list of AclBinding objects
    print(acls)
    for acl in acls:
        print("ACL: {}".format(acl))
except Exception as e:
    print("Failed to describe ACLs: {}".format(e))
