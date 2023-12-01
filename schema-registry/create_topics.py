from confluent_kafka.admin import AdminClient, NewTopic

a = AdminClient({'bootstrap.servers': 'localhost:19092'})
new_topics = [NewTopic(topic, num_partitions=3, replication_factor=1) for topic in ["topic1", "topic2"]]
fs = a.create_topics(new_topics)

# Wait for each operation to finish.
for topic, f in fs.items():
   try:
       f.result() # The result itself is None
       print("Topic {} created".format(topic))
   except Exception as e:
       print("Failed to create topic {}: {}".format(topic, e))
