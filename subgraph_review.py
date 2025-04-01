import typing
import strawberry

# fake database :)
ALL_REVIEWS = [
    {
        "id": "review#1",
        "business_id": "biz#1",
        "author": "Wayne R.",
        "text": "The fries were great",
    },
    {
        "id": "review#2",
        "business_id": "biz#2",
        "author": "David B.",
        "text": "Loved the sauce",
    },
    {
        "id": "review#3",
        "business_id": "biz#2",
        "author": "Gary N.",
        "text": "Nice atmosphere",
    },
    {
        "id": "review#4",
        "business_id": "biz#3",
        "author": "Paul S.",
        "text": "Will come again",
    },
]

get_review_data = lambda id: next(r for r in ALL_REVIEWS if r["id"] == id)


@strawberry.federation.type(keys=["id"])
class Review:
    id: strawberry.ID
    author: str
    text: str

    @strawberry.field(description="Fetches all reviews for this business")
    def business(self) -> "Business":
        data = get_review_data(self.id)
        return Business(id=data["business_id"])


@strawberry.federation.type(keys=["id"])
class Business:
    id: strawberry.ID

    @strawberry.field(description="Fetches all reviews for this business")
    def reviews(self) -> list[Review]:
        matched_reviews = filter(
            lambda review: review["business_id"] == self.id, ALL_REVIEWS
        )
        return [
            Review(id=data["id"], author=data["author"], text=data["text"])
            for data in matched_reviews
        ]


@strawberry.type
class Query:
    @strawberry.field(description="Fetch a single review (given an ID)")
    def reviews() -> list[Review]:
        return [
            Review(id=data["id"], author=data["author"], text=data["text"])
            for data in ALL_REVIEWS
        ]

    @strawberry.field(description="Fetch all reviews")
    def review(self, id: str) -> Review:
        data = get_review_data(id)
        return Review(id=id, author=data["author"], text=data["text"])


schema = strawberry.federation.Schema(
    query=Query, types=[Business], enable_federation_2=True
)
