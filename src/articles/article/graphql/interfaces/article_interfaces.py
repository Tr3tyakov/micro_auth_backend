import graphene


class Article(graphene.ObjectType):
    id = graphene.ID()
    name =graphene.String()
    date_created = graphene.String()
    date_edited = graphene.String()
    headline_id = graphene.Int()
