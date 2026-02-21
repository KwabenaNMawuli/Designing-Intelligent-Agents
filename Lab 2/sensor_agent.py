from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from earthquake_environment import EarthquakeEnvironment

class SensorAgent(Agent):

    class EarthquakeMonitorBehaviour(PeriodicBehaviour):
        async def run(self):
            reading = self.agent.environment.get_reading()

            # Print to console
            print(f"\n{'='*50}")
            print(f"  EARTHQUAKE SENSOR READING")
            print(f"{'='*50}")
            print(f"  Timestamp    : {reading['timestamp']}")
            print(f"  Location     : {reading['location']}")
            print(f"  Fault Line   : {reading['fault_line']}")
            print(f"  Magnitude    : {reading['magnitude']} ML")
            print(f"  Severity     : {reading['severity']}")
            print(f"  Depth        : {reading['depth_km']} km")
            print(f"  Aftershocks  : {reading['aftershock_probability']}")
            print(f"  Tsunami Risk : {reading['tsunami_risk']}")
            print(f"{'='*50}\n")

            # Alert if severe
            if reading['magnitude'] >= 6.0:
                print(f"  ⚠️  ALERT: High magnitude earthquake detected!")
                print(f"  ⚠️  Immediate response required!\n")

            # Save to log file
            with open("earthquake_logs.txt", "a") as log:
                log.write(
                    f"{reading['timestamp']} | "
                    f"Location: {reading['location']} | "
                    f"Magnitude: {reading['magnitude']} ML | "
                    f"Severity: {reading['severity']} | "
                    f"Depth: {reading['depth_km']} km | "
                    f"Fault: {reading['fault_line']} | "
                    f"Aftershocks: {reading['aftershock_probability']} | "
                    f"Tsunami Risk: {reading['tsunami_risk']}\n"
                )

    async def setup(self):
        self.environment = EarthquakeEnvironment()
        print(f"SensorAgent {self.jid} started.")
        print("Monitoring for earthquake activity...\n")
        monitor = self.EarthquakeMonitorBehaviour(period=5)
        self.add_behaviour(monitor)