"""
Background service that migrates scheduled flow runs to the latest flow version.
"""

from prefect.logging.loggers import get_logger
from prefect.server.services.base import LoopService

logger = get_logger(__name__)


class FlowVersionMigration(LoopService):
    """Migrates scheduled flow runs to the latest flow version.

    Runs periodically to find scheduled flow runs that were created against
    an older version of a flow and updates their version reference to the
    current version, preserving parameter bindings and run history.
    """

    loop_seconds: float = 60

    async def run_once(self) -> None:
        from sqlalchemy import select, update

        from prefect.server.database import provide_database_interface

        db = provide_database_interface()
        async with db.session_context(begin_transaction=True) as session:
            # Find scheduled runs pointing to an older flow version
            result = await session.execute(
                select(db.FlowRun.id, db.Flow.version)
                .join(db.Flow, db.Flow.id == db.FlowRun.flow_id)
                .where(
                    db.FlowRun.state_type == "SCHEDULED",
                    db.FlowRun.flow_version < db.Flow.version,
                )
                .limit(100)
            )
            rows = result.all()

            if not rows:
                return

            run_ids = [r[0] for r in rows]
            logger.info(
                "Migrating %d scheduled flow run(s) to latest flow version",
                len(run_ids),
            )

            await session.execute(
                update(db.FlowRun)
                .where(db.FlowRun.id.in_(run_ids))
                .values(flow_version=db.Flow.version)
            )
