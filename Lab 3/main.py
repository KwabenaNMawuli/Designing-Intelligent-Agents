import asyncio
import spade
from reactive_agent import ReactiveAgent

async def main():
    agent = ReactiveAgent("kwabena23@xmpp.jp", "bSUQHgs6Xxzmr!E")
    await agent.start(auto_register=True)

    print("Reactive agent running for 60 seconds...")
    await asyncio.sleep(60)

    await agent.stop()
    print("\nAgent stopped. Check response_logs.txt for full logs.")

if __name__ == "__main__":
    spade.run(main())