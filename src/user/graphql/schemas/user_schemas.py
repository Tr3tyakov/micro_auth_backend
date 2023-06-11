import graphene

from src.user.graphql.mutations.create_user_mutation import CreateUserMutation
from src.user.graphql.mutations.update_user_mutation import UpdateUserMutation
from src.user.graphql.query.get_users_query import Query


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()


user_schema = graphene.Schema(query=Query, mutation=Mutation)
