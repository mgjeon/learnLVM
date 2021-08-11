# hello_actor_amqp.py
import asyncio
import click
from clu import AMQPActor, command_parser

# Define task that the actor does
@command_parser.command()
@click.argument('NAME', type=str)
def say_hello(command, name):
    command.write('i', text=f'Hello {name}!')
    command.finish()

# A child class 'HelloActor' inherits a parent class 'AMQPActor'
class HelloActor(AMQPActor):
    def __init__(self):
        super().__init__(name='hello_actor',
                         user='guest', password='guest',
                         host='localhost', port=5672,
                         version='0.1.0')

# You can delete inheritance codes above and replace all codes below with these codes:
# ================================
# async def run_actor():
#   hello_actor = await AMQPActor(name='hello_actor',
#                                 user='guest', password='guest',
#                                 host='localhost', port=5672,
#                                 version='0.1.0').start()
#   await hello_actor.run_forever()
# 
# asyncio.run(run_actor())
# ================================
async def run_actor():
    hello_actor = await HelloActor().start()
    await hello_actor.run_forever()

asyncio.run(run_actor())