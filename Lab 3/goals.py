# Defines all rescue and response goals for the earthquake agent

class Goal:
    def __init__(self, name, priority, condition, action):
        self.name = name
        self.priority = priority      # Higher number = more urgent
        self.condition = condition    # Function that returns True/False
        self.action = action          # What the agent should do

# Define all goals
def define_goals():
    return [
        Goal(
            name="Evacuate Population",
            priority=5,
            condition=lambda r: r["magnitude"] >= 7.0,
            action="Trigger immediate mass evacuation of affected zones"
        ),
        Goal(
            name="Deploy Search and Rescue",
            priority=4,
            condition=lambda r: r["magnitude"] >= 6.0,
            action="Dispatch search and rescue teams to epicenter"
        ),
        Goal(
            name="Issue Tsunami Warning",
            priority=5,
            condition=lambda r: "EVACUATE" in r["tsunami_risk"],
            action="Broadcast tsunami warning to all coastal areas"
        ),
        Goal(
            name="Dispatch Medical Teams",
            priority=3,
            condition=lambda r: r["magnitude"] >= 5.0,
            action="Send medical teams and emergency supplies"
        ),
        Goal(
            name="Monitor Aftershocks",
            priority=2,
            condition=lambda r: r["aftershock_probability"] in ["Moderate", "High"],
            action="Deploy aftershock monitoring sensors"
        ),
        Goal(
            name="Issue Public Advisory",
            priority=1,
            condition=lambda r: r["magnitude"] >= 4.0,
            action="Broadcast public safety advisory and instructions"
        ),
    ]