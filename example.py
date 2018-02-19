#!/usr/bin/env python3
import asyncio

from async_challonge import Challonge, Tournament

async def test():
    # Initialize the API with your credentials
    async with Challonge("your_challonge_username", "your_api_key") as api:
        # Fetch all of your tournaments
        tournaments = await Tournament.find(api)
        # Create a new tournament
        tournament = await Tournament.create(api, name="TestTournament #" + str(len(tournaments)),
                                             url="test_tournament_" + str(len(tournaments)))

        print(tournament.started_at)  # None
        print(tournament.name)  # TestTournament #41

        # Add participants
        await tournament.bulk_add_participants({"name": "Player 1"}, {"name": "Player 2"})

        # Start the tournament
        await tournament.start()

        # Update the tournament's information
        await tournament.refetch()

        print(tournament.started_at)  # 2018-02-18 22:37:50.321000-06:00

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(test())
