import graphene

from src.articles.article.graphql.interfaces.article_interfaces import Article


class Headline(graphene.ObjectType):
    id =graphene.ID()
    name = graphene.String()
    date_created = graphene.String()
    date_edited  = graphene.String()
    articles  = graphene.List(Article)