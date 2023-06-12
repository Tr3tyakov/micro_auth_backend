import graphene

from src.user.graphql.mutations.create_user_mutation import CreateUserMutation
from src.user.graphql.mutations.update_user_mutation import UpdateUserMutation
from src.user.graphql.query.get_users_query import GetUsersQuery
from src.user.graphql.query.get_user_info_query import GetUserInfoQuery


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()


class Query(graphene.ObjectType):
    get_users = graphene.Field(GetUsersQuery)
    get_info = graphene.Field(GetUserInfoQuery)

    def resolve_get_users(self, info):
        return info

    def resolve_get_info(self, info):
        return info


user_schema = graphene.Schema(query=Query, mutation=Mutation)
