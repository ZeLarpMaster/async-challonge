from async_challonge import Challonge


class Match:
    def __init__(self, api: Challonge, response: dict):
        self.api = api
        self.base_endpoint = "tournaments/{}/matches/{}".format(response["tournament_id"], response["id"])
        self.raw_response = response

    async def update(self, **params):
        if "winner_id" in params and "scores_csv" not in params:
            raise ValueError("If winner_id is provided, scores_csv must also be provided")
        response = await self.api.fetch("PUT", self.base_endpoint, params)
        self.raw_response.update(response["match"])

    async def reopen(self):
        response = await self.api.fetch("POST", self.base_endpoint + "/reopen")
        self.raw_response.update(response["match"])

    def __getattr__(self, item):
        return self.raw_content.get(item)
