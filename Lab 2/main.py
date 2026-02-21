import asyncio
import spade
from sensor_agent import SensorAgent

async def main():
    agent = SensorAgent("kwabena23@xmpp.jp", "bSUQHgs6Xxzmr!E")
    await agent.start(auto_register=True)

    print("Earthquake monitoring active for 30 seconds...")
    await asyncio.sleep(30)

    await agent.stop()
    print("\nAgent stopped. Check earthquake_logs.txt for full logs.")

if __name__ == "__main__":
    spade.run(main())