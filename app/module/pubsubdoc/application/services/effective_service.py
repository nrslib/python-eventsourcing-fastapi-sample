from uuid import UUID

from eventsourcing.application import Application, AggregateNotFoundError

from app.module.pubsubdoc.domain.models.effective import Effective


class EffectiveService(Application):
    def mark(self, doc_id: UUID, user_id: UUID):
        effective_id = Effective.create_id(doc_id, user_id)
        try:
            effective = self.repository.get(effective_id)
            effective.mark()
        except AggregateNotFoundError:
            effective = Effective(doc_id, user_id)

        self.save(effective)

        return effective.id

    def get(self, doc_id: UUID, user_id: UUID):
        effective = self.repository.get(Effective.create_id(doc_id, user_id))

        return effective

    def unmark(self, doc_id: UUID, user_id: UUID):
        try:
            effective_id = Effective.create_id(doc_id, user_id)
            effective = self.repository.get(effective_id)
            effective.unmark()
            self.save(effective)
        except AggregateNotFoundError:  # The class does not exist in the version of the eventsourcing library compatible with the current version of the Axon Framework plugin.
            raise
