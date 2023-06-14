import graphene

from src.articles.headline.graphql.mutations.create_headlines_mutation import CreateHeadlinesMutation
from src.articles.headline.graphql.mutations.delete_headlines_mutation import DeleteHeadlinesMutation
from src.articles.headline.graphql.mutations.update_headlines_mutation import UpdateHeadlinesMutation
from src.articles.headline.graphql.query.get_headlines_query import GetHeadlinesQuery


class Mutation(graphene.ObjectType):
    create_headline = CreateHeadlinesMutation.Field()
    update_headline = UpdateHeadlinesMutation.Field()
    delete_headline = DeleteHeadlinesMutation.Field()


class Query(graphene.ObjectType):
    get_headline = graphene.Field(GetHeadlinesQuery)

    def resolve_get_headline(self, info):
        return info


headline_schema = graphene.Schema(query=Query, mutation=Mutation)
