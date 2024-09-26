from eventsourcing.domain import Aggregate, event, Snapshot, DomainEvent

class Doc(Aggregate):
    # ----- for axon server -----
    # INITIAL_VERSION = 0
    # ----- end -----
    body: str

    class DocCreated(Aggregate.Created):
        body: str

    @event(DocCreated)
    def __init__(self, body):
        self.body = body

    class DocModified(Aggregate.Event):
        body: str

    @event(DocModified)
    def modify(self, body):
        self.body = body
