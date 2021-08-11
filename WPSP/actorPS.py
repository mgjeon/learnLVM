# actorPS.py
import asyncio
import lvmpower as ps
import click
from clu import AMQPActor, command_parser


# Fuction that shows ON/OFF statuses
async def showStatus(dli, command, number=0, when=""):
    statlist = await dli.statuslist()
    for stat in statlist:
        if(number == 0):
            command.write('i', text=f"{when} => {stat[1]}: {stat[2]}")
        elif(stat[0] == number):
            command.write('i', text=f"{when} => {stat[1]}: {stat[2]}")


# Fuctions that wait whether the ON/OFF tasks were performed
async def isDoneAll(dli, ONorOFF, num):
    isOK = []
    while(sum(isOK) != num):
        isOK.clear()
        statlist = await dli.statuslist()
        for stat in statlist:
            isOK.append(stat[2] == ONorOFF)


async def isDone(dli, ONorOFF, num):
    isOK = False
    while(not isOK):
        statlist = await dli.statuslist()
        for stat in statlist:
            if (stat[0] == num):
                isOK = (stat[2] == ONorOFF)


@command_parser.command()
# Define arguments that are passed to the actor
@click.argument('name', type=str)
@click.argument('number', type=int, default=0)
# Define task that the actor does
async def main(command, name, number):
    # Default the web interface infomation of Web Power Switch Pro
    host = '163.180.145.158'
    userid = 'admin'
    password = '1234'
    # Connect the web interface of Web Power Switch Pro
    dli = ps.LVMPowerSwitch(hostname=host, userid=userid, password=password)
    await dli.add_client()

    # Define commands that actor performs
    if (('on' == name) and (number in range(1, 9))):
        await showStatus(dli, command, number, "Before")
        await dli.on(outlet_number=number)
        await isDone(dli, 'ON', number)
    elif (('off' == name) and (number in range(1, 9))):
        await showStatus(dli, command, number, "Before")
        await dli.off(outlet_number=number)
        await isDone(dli, 'OFF', number)
    elif ('onall' == name):
        await showStatus(dli, command, number, "Before")
        await dli.onall()
        await isDoneAll(dli, 'ON', 8)
    elif ('offall' == name):
        await showStatus(dli, command, number, "Before")
        await dli.offall()
        await isDoneAll(dli, 'OFF', 8)
    elif ('status' == name):
        pass
    else:
        command.write('i', text="incorret command")
        command.finish()

    await showStatus(dli, command, number, "Current")
    await dli.close()
    command.finish()


class HelloActor(AMQPActor):
    def __init__(self):
        super().__init__(name='PS',
                         user='guest', password='guest',
                         host='localhost', port='5672',
                         version='0.1.0')


async def run_actor():
    hello_actor = await HelloActor().start()
    await hello_actor.run_forever()


asyncio.run(run_actor())
