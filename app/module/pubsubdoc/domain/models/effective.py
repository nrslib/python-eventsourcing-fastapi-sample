from functools import singledispatchmethod
from uuid import UUID, NAMESPACE_URL, uuid5

from eventsourcing.domain import Aggregate, event


class Effective(Aggregate):
    doc_id: UUID
    user_id: UUID
    marked: bool

    # Event Classes
    class Created(Aggregate.Created):
        def apply(self, aggregate: Aggregate):
            aggregate.when(self)

    class Event(Aggregate.Event):
        def apply(self, aggregate: Aggregate):
            aggregate.when(self)

    class EffectiveCreated(Created):
        doc_id: UUID
        user_id: UUID

    class EffectiveMarked(Event):
        doc_id: UUID

    class EffectiveUnmarked(Event):
        doc_id: UUID

        # def apply(self, effective: Aggregate):
        #     effective.marked = False

    @classmethod
    def create(cls, doc_id: UUID, user_id: UUID):
        return cls._create(
            event_class=cls.Created,
            id=cls.create_id(doc_id, user_id),
            doc_id=doc_id,
            user_id=user_id,
        )

    @staticmethod
    def create_id(doc_id: UUID, user_id: UUID) -> UUID:
        return uuid5(NAMESPACE_URL, f"/effective/{doc_id}|{user_id}")

    @event(EffectiveCreated)
    def __init__(self, doc_id: UUID, user_id: UUID):
        self.doc_id = doc_id
        self.user_id = user_id
        self.marked = True

    def mark(self):
        if not self.marked:
            self._mark(self.doc_id)

    @event(EffectiveMarked)
    def _mark(self, doc_id: UUID):
        self.marked = True

    def unmark(self):
        if self.marked:
            self._unmark()

    def _unmark(self):
        self.trigger_event(Effective.EffectiveUnmarked, doc_id=self.doc_id)

    # Event handlers

    @singledispatchmethod
    def when(self, event) -> None:
        raise NotImplementedError(f"Unsupported event type: {type(event)}")

    @when.register(EffectiveCreated)
    def _(self, event: EffectiveCreated) -> None:
        self.doc_id = event.doc_id
        self.user_id = event.user_id

    @when.register(EffectiveMarked)
    def _(self, event: EffectiveMarked) -> None:
        pass

    @when.register(EffectiveUnmarked)
    def _(self, event: EffectiveUnmarked) -> None:
        self.marked = False
