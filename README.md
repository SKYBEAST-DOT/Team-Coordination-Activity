# Team-Coordination-Activity

Simple team coordination activity system to handle and manage work across any function (engineering, operations, design, support, etc.).

## Features
- Create activities with a function label
- Assign and reassign owners
- Update status (`planned`, `in_progress`, `completed`, `blocked`)
- Filter activities by function, status, and owner
- Generate a small status summary

## Quick usage
```python
from coordination_system import TeamCoordinationActivitySystem

system = TeamCoordinationActivitySystem()
activity = system.create_activity(
    title="Prepare sprint kickoff",
    function="operations",
    owner="Alex",
)

system.update_activity(activity["id"], status="in_progress")
system.complete_activity(activity["id"])
print(system.summary())
```
