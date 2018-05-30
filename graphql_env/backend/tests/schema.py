import graphene


class Query(graphene.ObjectType):
    hello = graphene.String(required=True)

    def resolve_hello(self, info):
        return "World"


schema = graphene.Schema(query=Query)
