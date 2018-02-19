from async_challonge import Challonge, Participant, Match
from .challonge import prepare_prefixed_params, sanitize_boolean_params, flatten_array_params

# TODO: Explode **params into individual params as documentation
# TODO: Add attachments support


class Tournament:
    def __init__(self, api: Challonge, response: dict):
        self.api = api
        self.base_endpoint = "tournaments/{}".format(response["id"])
        self.raw_content = response

    # Tournaments
    async def refetch(self):
        response = await self.api.fetch("GET", self.base_endpoint)
        self.raw_content.update(response["tournament"])

    @classmethod
    async def find(cls, api: Challonge, **params):
        return [Tournament(api, t["tournament"]) for t in await api.fetch("GET", "tournaments", params)]

    @classmethod
    async def create(cls, api: Challonge, **params):
        response = await api.fetch("POST", "tournaments", prepare_prefixed_params("tournament", params))
        return Tournament(api, response["tournament"])

    @classmethod
    async def get(cls, api: Challonge, tournament: str, **params):
        response = await api.fetch("GET", "tournaments/" + tournament, sanitize_boolean_params(params))
        return Tournament(api, response["tournament"])

    async def update(self, **params):
        await self.api.fetch("PUT", self.base_endpoint, prepare_prefixed_params("tournament", params))
        self.raw_content.update(params)

    async def destroy(self):
        await self.api.fetch("DELETE", self.base_endpoint)
        self.raw_content.clear()

    async def start(self, **params):
        await self.api.fetch("POST", self.base_endpoint + "/start", sanitize_boolean_params(params))

    async def finalize(self, **params):
        await self.api.fetch("POST", self.base_endpoint + "/finalize", sanitize_boolean_params(params))

    async def reset(self, **params):
        await self.api.fetch("POST", self.base_endpoint + "/reset", sanitize_boolean_params(params))

    # Participants
    async def list_participants(self):
        response = await self.api.fetch("GET", self.base_endpoint + "/participants")
        return [Participant(self.api, p["participant"]) for p in response]

    async def create_participant(self, **params):
        response = await self.api.fetch("POST", self.base_endpoint + "/participants",
                                        prepare_prefixed_params("participant", params))
        return Participant(self.api, response["participant"])

    async def bulk_add_participants(self, *participants):
        await self.api.fetch("POST", self.base_endpoint + "/participants/bulk_add",
                             flatten_array_params("participants", participants))

    async def get_participant(self, participant_id: str, **params):
        response = await self.api.fetch("GET", self.base_endpoint + "/participants/" + participant_id,
                                        sanitize_boolean_params(params))
        return Participant(self.api, response["participant"])

    async def randomize_participants(self):
        await self.api.fetch("POST", self.base_endpoint + "/participants/randomize")

    # Matches
    async def list_matches(self, **params):
        response = await self.api.fetch("GET", self.base_endpoint + "/matches", params)
        return [Match(self.api, m["match"]) for m in response]

    async def get_match(self, match_id: str, **params):
        response = await self.api.fetch("GET", self.base_endpoint + "/matches/" + match_id,
                                        sanitize_boolean_params(params))
        return Match(self.api, response["match"])

    def __getattr__(self, item):
        return self.raw_content.get(item)
