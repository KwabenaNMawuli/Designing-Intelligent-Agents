import asyncio
import spade
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour

class BasicAgent(Agent):
    class MyBehaviour(OneShotBehaviour):
        async def run(self):
            print(f"Hello! I am agent {self.agent.jid}")
            print("My first SPADE behaviour is running!")
            await self.agent.stop()

    async def setup(self):
        print(f"Agent {self.jid} is starting...")
        behaviour = self.MyBehaviour()
        self.add_behaviour(behaviour)

async def main():
    agent = BasicAgent("kwabena23@xmpp.jp", "bSUQHgs6Xxzmr!E")
    await agent.start(auto_register=True)
    await agent.stop()

if __name__ == "__main__":
    spade.run(main())