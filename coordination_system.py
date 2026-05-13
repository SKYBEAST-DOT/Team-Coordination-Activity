"""Team coordination activity management."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


VALID_STATUSES = {"planned", "in_progress", "completed", "blocked"}


@dataclass
class Activity:
    id: int
    title: str
    function: str
    owner: Optional[str] = None
    status: str = "planned"


class TeamCoordinationActivitySystem:
    """In-memory activity system for coordinating work across any function."""

    def __init__(self) -> None:
        self._activities: Dict[int, Activity] = {}
        self._next_id = 1

    def create_activity(self, title: str, function: str, owner: Optional[str] = None) -> dict:
        if not title.strip():
            raise ValueError("title must not be empty")
        if not function.strip():
            raise ValueError("function must not be empty")

        activity = Activity(id=self._next_id, title=title.strip(), function=function.strip(), owner=owner)
        self._activities[self._next_id] = activity
        self._next_id += 1
        return asdict(activity)

    def get_activity(self, activity_id: int) -> dict:
        activity = self._require_activity(activity_id)
        return asdict(activity)

    def update_activity(
        self,
        activity_id: int,
        *,
        title: Optional[str] = None,
        function: Optional[str] = None,
        owner: Optional[str] = None,
        status: Optional[str] = None,
    ) -> dict:
        activity = self._require_activity(activity_id)

        if title is not None:
            if not title.strip():
                raise ValueError("title must not be empty")
            activity.title = title.strip()
        if function is not None:
            if not function.strip():
                raise ValueError("function must not be empty")
            activity.function = function.strip()
        if owner is not None:
            activity.owner = owner
        if status is not None:
            self._validate_status(status)
            activity.status = status

        return asdict(activity)

    def assign_activity(self, activity_id: int, owner: str) -> dict:
        return self.update_activity(activity_id, owner=owner)

    def complete_activity(self, activity_id: int) -> dict:
        return self.update_activity(activity_id, status="completed")

    def delete_activity(self, activity_id: int) -> None:
        self._require_activity(activity_id)
        del self._activities[activity_id]

    def list_activities(
        self,
        *,
        function: Optional[str] = None,
        status: Optional[str] = None,
        owner: Optional[str] = None,
    ) -> List[dict]:
        if status is not None:
            self._validate_status(status)

        activities = self._activities.values()
        if function is not None:
            activities = (a for a in activities if a.function == function)
        if status is not None:
            activities = (a for a in activities if a.status == status)
        if owner is not None:
            activities = (a for a in activities if a.owner == owner)
        return [asdict(activity) for activity in activities]

    def summary(self) -> dict:
        status_summary = {status: 0 for status in VALID_STATUSES}
        function_summary: Dict[str, int] = {}

        for activity in self._activities.values():
            status_summary[activity.status] += 1
            function_summary[activity.function] = function_summary.get(activity.function, 0) + 1

        return {
            "total": len(self._activities),
            "by_status": status_summary,
            "by_function": function_summary,
        }

    def _validate_status(self, status: str) -> None:
        if status not in VALID_STATUSES:
            raise ValueError(f"status must be one of: {', '.join(sorted(VALID_STATUSES))}")

    def _require_activity(self, activity_id: int) -> Activity:
        activity = self._activities.get(activity_id)
        if activity is None:
            raise KeyError(f"activity {activity_id} not found")
        return activity
