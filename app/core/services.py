import os

from eventsourcing.system import System, SingleThreadedRunner, MultiThreadedRunner

from app.config import setup
from app.module.pubsubdoc.application.query.document.document_projection import DocumentDataModelProjection
from app.module.pubsubdoc.application.query.document.document_query_service import DocumentQueryService
from app.module.pubsubdoc.application.services.doc_service import DocService
from app.module.pubsubdoc.application.services.effective_service import EffectiveService

setup()

os.environ['PERSISTENCE_MODULE'] = 'eventsourcing_sqlalchemy'
os.environ['SQLALCHEMY_URL'] = 'sqlite:///./db/sqlite.db'

# os.environ['PERSISTENCE_MODULE'] = 'eventsourcing_axonserver'
# os.environ['AXONSERVER_URI'] = '127.0.0.1:8124'

system = System(
    pipes=[
        [DocService, DocumentDataModelProjection],
        [EffectiveService, DocumentDataModelProjection],
    ]
)

runner = MultiThreadedRunner
runner = runner(system, None)
runner.start()

doc_service = runner.get(DocService)


# ----- for axon server. It's still not supported by the runner. -----
# doc_service = DocService(env={
#     "PERSISTENCE_MODULE": "eventsourcing_axonserver",
#     "AXONSERVER_URI": "127.0.0.1:8124",
# })
# ----- end for -----

def get_doc_service():
    return doc_service


def get_document_query_service():
    return DocumentQueryService()


effective_service = runner.get(EffectiveService)


def get_effective_service():
    return effective_service
