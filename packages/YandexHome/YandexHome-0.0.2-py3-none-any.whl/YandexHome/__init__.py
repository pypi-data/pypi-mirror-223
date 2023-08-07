from flask import Flask, request
from threading import Thread, Event
import base64
import aiohttp
from .Device import Device
from typing import Any

class StoppableThread(Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class ClientDataInvalid(BaseException): pass

app = Flask(__name__)
server = StoppableThread(target=app.run, args=('localhost', 5030))
pclient_id = None
pclient_secret = None

class YandexHome:
    def __init__(self, token: str = None, *, client_id: str = None, client_secret: str = None) -> None:
        if not token and client_id and client_secret:
            global pclient_id
            global pclient_secret
            pclient_id = client_id
            pclient_secret = client_secret
            self.get_token()
        elif (not token and not client_id and client_secret) or (not token and client_id and not client_secret) or (not token and not client_id and not client_secret):
            raise ClientDataInvalid("Отсутствуют client_id и client_secret для получения токена!")
        self.token = token

    def get_token(self):
        server.start()
        server.join()

    async def get_devices(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.iot.yandex.net/v1.0/user/info', headers={'Authorization': f'Bearer {self.token}'}) as req:
                json = await req.json()
                if json['status'] == 'ok':
                    devices = []
                    for device in json['devices']:
                        device = Device.Device(device['id'], device['name'], device['aliases'], device['room'], device['external_id'], device['skill_id'], device['type'], device['groups'], device['capabilities'], device['properties'], device['household_id'], self.token)
                        devices.append(device)
                    return devices
                else:
                    return 'error!'
            
    async def get_device_state(self, deviceId: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.iot.yandex.net/v1.0/devices/{deviceId}', headers={'Authorization': f'Bearer {self.token}'}) as req:
                json = await req.json()
                if json['status'] == 'ok':
                    device = Device.Device(json['id'], json['name'], json['aliases'], json['room'], json['external_id'], json['skill_id'], json['type'], json['groups'], json['capabilities'], json['properties'], json.get('household_id', '0'), self.token)
                    return device
                else:
                    return 'error!'
            
    async def action(self, device: Device.Device, actionType: str, instance: str, value: Any):
        async with aiohttp.ClientSession() as session:
            async with session.post(f'https://api.iot.yandex.net/v1.0/devices/actions', headers={'Authorization': f'Bearer {self.token}'}, json={'devices': [{'id': device.id, 'actions': [{'type': actionType, 'state': {'instance': instance, 'value': value}}]}]}) as req:
                json = await req.json()
                return json

@app.route('/')
async def yandex_callback():
    if pclient_id and pclient_secret:
        code = request.args.get('code')
        auth = f"{pclient_id}:{pclient_secret}"
        auth_bytes = auth.encode('ascii')
        base64_bytes = base64.b64encode(auth_bytes)
        base64_auth = base64_bytes.decode('ascii')
        async with aiohttp.ClientSession() as session:
            async with session.post('https://oauth.yandex.ru/token', headers={'Authorization': f'Basic {base64_auth}'}, data={'grant_type': 'authorization_code', 'code': code}) as req:
                json = await req.json()
                token = json['access_token']
                return f'Твой токен: {token}'
