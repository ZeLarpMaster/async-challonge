from async_challonge import Challonge


class Participant:
    def __init__(self, api: Challonge, response: dict):
        self.api = api
        self.base_endpoint = "tournaments/{}/participants/{}".format(response["tournament_id"], response["id"])
        self.raw_content = response

    async def update(self, **params):
        await self.api.fetch("PUT", self.base_endpoint, params)
        self.raw_content.update(params)

    async def check_in(self):
        await self.api.fetch("POST", self.base_endpoint + "/check_in")

    async def undo_check_in(self):
        await self.api.fetch("POST", self.base_endpoint + "/undo_check_in")

    async def destroy(self):
        await self.api.fetch("DELETE", self.base_endpoint)

    def __getattr__(self, item):
        return self.raw_content.get(item)
