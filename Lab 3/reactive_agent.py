import sys
import os
import sys
sys.path.append('../Lab 2')
from earthquake_environment import EarthquakeEnvironment
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State

from goals import define_goals

# ── FSM States ─────────────────────────────────────────────────────────────────
STATE_MONITORING  = "MONITORING"
STATE_ANALYZING   = "ANALYZING"
STATE_RESPONDING  = "RESPONDING"
STATE_IDLE        = "IDLE"

class MonitoringState(State):
    async def run(self):
        reading = self.agent.environment.get_reading()
        self.agent.latest_reading = reading

        print(f"\n[MONITORING] Earthquake detected!")
        print(f"  Location  : {reading['location']}")
        print(f"  Magnitude : {reading['magnitude']} ML")
        print(f"  Severity  : {reading['severity']}")

        # Transition based on magnitude
        if reading["magnitude"] >= 4.0:
            self.set_next_state(STATE_ANALYZING)
        else:
            self.set_next_state(STATE_IDLE)


class AnalyzingState(State):
    async def run(self):
        reading = self.agent.latest_reading
        goals = define_goals()

        print(f"\n[ANALYZING] Evaluating goals for magnitude {reading['magnitude']} ML...")

        # Find all triggered goals
        triggered = [g for g in goals if g.condition(reading)]
        triggered.sort(key=lambda g: g.priority, reverse=True)

        self.agent.triggered_goals = triggered

        if triggered:
            print(f"  {len(triggered)} goal(s) triggered!")
            self.set_next_state(STATE_RESPONDING)
        else:
            print("  No goals triggered.")
            self.set_next_state(STATE_IDLE)


class RespondingState(State):
    async def run(self):
        reading = self.agent.latest_reading
        goals = self.agent.triggered_goals

        print(f"\n[RESPONDING] Executing response actions:")
        print(f"{'='*50}")

        with open("response_logs.txt", "a") as log:
            log.write(f"\n--- Event: {reading['timestamp']} | "
                      f"{reading['location']} | Mag: {reading['magnitude']} ---\n")

            for goal in goals:
                print(f"  [Priority {goal.priority}] {goal.name}")
                print(f"    → {goal.action}")
                log.write(f"  Goal: {goal.name} | Action: {goal.action}\n")

        print(f"{'='*50}")
        self.set_next_state(STATE_IDLE)


class IdleState(State):
    async def run(self):
        import asyncio
        print("\n[IDLE] Waiting for next sensor cycle...\n")
        await asyncio.sleep(5)
        self.set_next_state(STATE_MONITORING)


# ── Reactive Agent ─────────────────────────────────────────────────────────────
class ReactiveAgent(Agent):

    async def setup(self):
        self.environment = EarthquakeEnvironment()
        self.latest_reading = None
        self.triggered_goals = []

        print(f"ReactiveAgent {self.jid} started.\n")

        # Build FSM
        fsm = FSMBehaviour()
        fsm.add_state(name=STATE_MONITORING,  state=MonitoringState(), initial=True)
        fsm.add_state(name=STATE_ANALYZING,   state=AnalyzingState())
        fsm.add_state(name=STATE_RESPONDING,  state=RespondingState())
        fsm.add_state(name=STATE_IDLE,        state=IdleState())

        # Define transitions
        fsm.add_transition(source=STATE_MONITORING, dest=STATE_ANALYZING)
        fsm.add_transition(source=STATE_MONITORING, dest=STATE_IDLE)
        fsm.add_transition(source=STATE_ANALYZING,  dest=STATE_RESPONDING)
        fsm.add_transition(source=STATE_ANALYZING,  dest=STATE_IDLE)
        fsm.add_transition(source=STATE_RESPONDING, dest=STATE_IDLE)
        fsm.add_transition(source=STATE_IDLE,       dest=STATE_MONITORING)

        self.add_behaviour(fsm)