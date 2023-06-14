import graphene

from src.articles.article.graphql.mutation.create_article_mutation import CreateArticleMutation
from src.articles.article.graphql.mutation.delete_article_mutation import DeleteArticleMutation
from src.articles.article.graphql.mutation.update_article_mutation import UpdateArticleMutation
from src.articles.article.graphql.query.get_articles_query import GetArticlesQuery


class Mutation(graphene.ObjectType):
    create_article = CreateArticleMutation.Field()
    update_article = UpdateArticleMutation.Field()
    delete_article = DeleteArticleMutation.Field()


class Query(graphene.ObjectType):
    get_articles = graphene.Field(GetArticlesQuery)

    def resolve_get_articles(self, info):
        return info


article_schema = graphene.Schema(query=Query, mutation=Mutation)
