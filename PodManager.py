class PodManager:
    def __init__(self):
        self.pods = {}  

    def add_pod(self, name, is_producer, is_consumer, topic=None):
        self.pods[name] = {
            'is_producer': is_producer,
            'is_consumer': is_consumer,
            'topic': topic
        }

    def get_pod_info(self, name):
        return self.pods.get(name, None)

    def display_pods(self):
        for name, info in self.pods.items():
            role = []
            if info['is_producer']:
                role.append('Producer')
            if info['is_consumer']:
                role.append('Consumer')
            print(f"Pod Name: {name}, Role: {' & '.join(role)}, Topic: {info['topic']}")


# usecase
pod_manager = PodManager()
pod_manager.add_pod('service-a', is_producer=True, is_consumer=False, topic='service-a-topic')
pod_manager.add_pod('service-b', is_producer=True, is_consumer=True, topic='service-b-topic')
pod_manager.add_pod('service-c', is_producer=False, is_consumer=True, topic='service-c-topic')

pod_manager.display_pods()
