import os
from typing import Dict, Any

from eventsourcing.application import Application

from app.module.pubsubdoc.domain.models.doc import Doc


class DocService(Application):
    is_snapshotting_enabled = True

    def create(self, body):
        doc = Doc(body)
        self.save(doc)

        return doc.id

    def modify(self, doc_id, body):
        doc = self.repository.get(doc_id)
        doc.modify(body)
        self.save(doc)
        self.take_snapshot(doc.id)

    def get(self, doc_id):
        doc = self.repository.get(doc_id)

        return doc

    def compare_fields(self, other: 'CustomApplication') -> Dict[str, Any]:
        differences = {}

        # 比較するフィールドのリストを定義
        fields_to_compare = [
            'env',
            'log_section_size',
            'notify_topics'
            # 必要な他のフィールドを追加
        ]

        for field in fields_to_compare:
            # 自身のフィールドと他のインスタンスのフィールドを比較
            self_value = getattr(self, field, None)
            other_value = getattr(other, field, None)

            if self_value != other_value:
                differences[field] = {
                    'self': self_value,
                    'other': other_value
                }

        return differences
