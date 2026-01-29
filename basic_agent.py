"""
Basic SPADE Agent Example
This demonstrates a simple SPADE agent with a periodic behavior.
"""

import asyncio
from datetime import datetime


class SimpleBehaviour:
    """A simple behavior that executes periodically."""
    
    def __init__(self, agent, interval=2):
        self.agent = agent
        self.interval = interval
        self.is_active = True
    
    async def run(self):
        """Execute the behavior."""
        while self.is_active:
            await self.execute()
            await asyncio.sleep(self.interval)
    
    async def execute(self):
        """Override this method in subclasses."""
        pass
    
    def stop(self):
        """Stop the behavior."""
        self.is_active = False


class GreetingBehaviour(SimpleBehaviour):
    """A behavior that greets the world."""
    
    async def execute(self):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {self.agent.name}: Hello from SPADE Agent!")
        print(f"[{timestamp}] {self.agent.name}: I'm running a periodic task...")


class CounterBehaviour(SimpleBehaviour):
    """A behavior that counts iterations."""
    
    def __init__(self, agent, interval=3):
        super().__init__(agent, interval)
        self.counter = 0
    
    async def execute(self):
        self.counter += 1
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {self.agent.name}: Counter = {self.counter}")


class BasicAgent:
    """A simple SPADE-like agent."""
    
    def __init__(self, name):
        self.name = name
        self.behaviours = []
        self.is_running = False
    
    def add_behaviour(self, behaviour):
        """Add a behavior to the agent."""
        self.behaviours.append(behaviour)
        print(f"[{self.name}] Added behaviour: {behaviour.__class__.__name__}")
    
    async def start(self):
        """Start the agent."""
        self.is_running = True
        print(f"\n✓ Agent '{self.name}' started!")
        print(f"✓ Running {len(self.behaviours)} behaviour(s)\n")
    
    async def stop(self):
        """Stop the agent."""
        self.is_running = False
        for behaviour in self.behaviours:
            behaviour.stop()
        print(f"\n✓ Agent '{self.name}' stopped!")
    
    async def run(self):
        """Run the agent and its behaviors."""
        await self.start()
        
        # Run all behaviors concurrently
        tasks = [behaviour.run() for behaviour in self.behaviours]
        
        try:
            # Run for a set duration
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            await self.stop()


async def main():
    """Main function to demonstrate the basic SPADE agent."""
    
    print("=" * 60)
    print("SPADE Basic Agent Demo")
    print("=" * 60)
    
    # Create an agent
    agent = BasicAgent("MyAgent")
    
    # Add behaviors
    greeting = GreetingBehaviour(agent, interval=2)
    counter = CounterBehaviour(agent, interval=3)
    
    agent.add_behaviour(greeting)
    agent.add_behaviour(counter)
    
    # Start the agent
    await agent.start()
    
    # Create tasks for behaviors
    tasks = [
        asyncio.create_task(greeting.run()),
        asyncio.create_task(counter.run())
    ]
    
    try:
        # Run for 10 seconds
        await asyncio.sleep(10)
    finally:
        # Stop the agent and its behaviors
        for behaviour in agent.behaviours:
            behaviour.stop()
        
        # Wait for tasks to complete
        await asyncio.gather(*tasks, return_exceptions=True)
        
        await agent.stop()
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
