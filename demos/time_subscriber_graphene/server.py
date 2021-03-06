"""Time Subscriber Server"""

import uvicorn

from bareasgi import Application
from bareasgi_graphql_next.graphene import add_graphene

from demos.time_subscriber_graphene.time_schema import SCHEMA

app = Application()
add_graphene(app, SCHEMA)

uvicorn.run(app, port=9009)
