import typing
import strawberry

# fake database :)
ALL_BUSINESSES = [
    {"id": "biz#1", "name": "McDonalds", "rating": 4},
    {"id": "biz#2", "name": "Burger King", "rating": 3},
    {"id": "biz#3", "name": "Subway", "rating": 5},
]

get_business_data = lambda id: next(biz for biz in ALL_BUSINESSES if biz["id"] == id)


@strawberry.federation.type(keys=["id"])
class Business:
    id: strawberry.ID
    name: str
    rating: int

    @classmethod
    def resolve_reference(cls, id: strawberry.ID) -> "Business":
        return Business(**get_business_data(id))


@strawberry.type
class Query:
    @strawberry.field(description="Fetch a single business (given an ID)")
    def business(self, id: str) -> Business:
        return Business(**get_business_data(id))

    @strawberry.field(description="Fetch all businesses")
    def businesses() -> list[Business]:
        return [Business(**biz) for biz in ALL_BUSINESSES]


schema = strawberry.federation.Schema(query=Query, enable_federation_2=True)
