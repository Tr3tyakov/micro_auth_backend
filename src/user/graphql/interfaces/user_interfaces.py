import graphene
class User(graphene.ObjectType):
    id = graphene.ID()
    email = graphene.String()
    is_confirmed = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    age = graphene.Int()
    city = graphene.String()
    date_register = graphene.String()
    date_last_actions = graphene.String()
    phone = graphene.String()
    avatar = graphene.String()
