from confluent_kafka.admin import AdminClient

a = AdminClient({'bootstrap.servers': 'localhost:19092'})
fs = a.list_consumer_groups()

# Wait for the operation to finish.
try:
 consumer_groups = fs.result() # The result is a list of ConsumerGroupInfo objects
 print(consumer_groups.__dict__)
 for group in consumer_groups.valid:
     print("Consumer group: {}".format(group.group_id))
except Exception as e:
 print("Failed to list consumer groups: {}".format(e))
