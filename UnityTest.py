import asyncio
import json
import keyboard

counter = 0

# Asynchronous communication with Unity 3D over TCP
async def tcp_echo_client(message, loop):
    # open connection with Unity 3D
    reader, writer = await asyncio.open_connection('127.0.0.1', 8052,
                                                   loop=loop)
    print('Send: %r' % message)

    # test purposes
    global counter

    # convert JSON to bytes
    message_json = json.dumps(message).encode()
    # send message
    writer.write(message_json)
    '''counter += 1

    # wait for data from Unity 3D
    data = await reader.read(100)
    # we expect data to be JSON formatted
    #data_json = json.loads(data.decode())
    print('Received:\n%r' % data)

    print('Close the socket')'''
    writer.close()

flag = 0
loop = asyncio.get_event_loop()
message = '2,5,8,1,0'
try:
    print('Connected')
    while True:
        if keyboard.is_pressed('s') and flag == 0:
            loop.run_until_complete(tcp_echo_client(message, loop))
            flag = 10000
        if flag > 0:
            flag -= 1
        print(flag)
except KeyboardInterrupt:
    loop.close()
