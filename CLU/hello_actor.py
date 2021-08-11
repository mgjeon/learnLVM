# hello_actor.py
import asyncio
import click
from clu import LegacyActor, command_parser

# Define task that the actor does
@command_parser.command()
@click.argument('NAME', type=str)
def say_hello(command, name):
  command.write('i', text=f'Hello {name}!')
  command.finish()

# A child class 'HelloActor' inherits a parent class 'LegacyActor'
class HelloActor(LegacyActor):
  def __init__(self):
    super().__init__(name='hello_actor',
                     host='localhost', port=9999,
                     version='0.1.0')

# You can delete inheritance codes above and replace all codes below with these codes:
# ================================
# async def run_actor():
#   hello_actor = await LegacyActor(name='hello_actor',
#                                   host='localhost', port=9999,
#                                   version='0.1.0').start()
#   await hello_actor.run_forever()
# 
# asyncio.run(run_actor())
# ================================
async def run_actor():
  hello_actor = await HelloActor().start()
  await hello_actor.run_forever()

asyncio.run(run_actor())