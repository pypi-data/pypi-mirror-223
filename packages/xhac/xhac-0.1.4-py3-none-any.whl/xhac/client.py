# Author: Snow Yang
# E-mail: yangsw@mxchip.com
# Since: 2023-07-31
# Version: 1.0
# Description: This file contains the HTTPClient class.
# This file is part of the xHAC project.
# License: MIT License

# Python built-in modules
import sys
import json
import socket
import asyncio
import hashlib
from functools import partial
from threading import Thread, Semaphore
# Third-party modules
import srp
import hkdf
from chacha20poly1305 import ChaCha20Poly1305
# Private modules
from .pyparser import HttpParser
from .model import *


class HTTPClient:
    def __init__(self):
        self.is_secure = False

        self.connected = False

        self.connect_sem = Semaphore(0)
        self.disconnect_sem = Semaphore(0)
        self.response_sem = None

        self.on_disconnect = lambda: None
        self.on_event = lambda event: None

        self.loop = asyncio.new_event_loop()
        Thread(target=self._loop_thread, daemon=True).start()

    def _loop_thread(self):
        self.loop.run_forever()

    def connect(self, host, port, username, password):
        self.loop.call_soon_threadsafe(partial(
            self._connect, host=host, port=port, username=username, password=password))
        self.connect_sem.acquire()
        return self.connected

    def _connect(self, host, port, username, password):
        if self.connected:
            self.connect_sem.release()
            return

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            # Linux specific: after 10 idle seconds, start sending keepalives every 2 seconds.
            # Drop connection after 10 failed keepalives
            self.socket.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_KEEPALIVE if sys.platform == 'darwin' else socket.TCP_KEEPIDLE, 10)
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 2)
            self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 10)

            usr = srp.User(username, password,
                           hash_alg=srp.SHA256, ng_type=srp.NG_1024)
            _, A = usr.start_authentication()

            self.socket.settimeout(5)
            self.socket.connect((host, port))

            self.post('/srp', None)
            body = self.recv_response()
            body = json.loads(body)
            s, B = bytes.fromhex(body['salt']), bytes.fromhex(body['B'])

            M = usr.process_challenge(s, B)
            self.post('/srp', json.dumps({'A': A.hex(), 'proof': M.hex()}))
            body = self.recv_response()
            body = json.loads(body)
            proof = bytes.fromhex(body['proof'])
            usr.verify_session(proof)

            sk = usr.get_session_key()

            kdf = hkdf.Hkdf(b'Control-Salt', sk, hash=hashlib.sha512)
            C2S_Key = kdf.expand(b'Control-Write-Encryption-Key', 32)
            self.SendCipher = ChaCha20Poly1305(C2S_Key)
            S2C_Key = kdf.expand(b'Control-Read-Encryption-Key', 32)
            self.recvCipher = ChaCha20Poly1305(S2C_Key)

            self.sendSeq = 0
            self.recvSeq = 0

            self.is_secure = True

            self.socket.setblocking(False)

            self.recv_task = self.loop.create_task(self.recv_task())

            self.connected = True
        except:
            self.socket.close()
        finally:
            self.connect_sem.release()

    def disconnect(self):
        self.loop.call_soon_threadsafe(self._disconnect)
        self.disconnect_sem.acquire()

    def _disconnect(self):
        self.loop.create_task(self._disconnect_task())

    async def _disconnect_task(self):
        if self.connected:
            self.loop
            self.socket.close()
            self.recv_task.cancel()
            await self.recv_task
            self.connected = False
            self.is_secure = False
        self.disconnect_sem.release()

    def post(self, path, body):
        self._send(
            (
                f'POST {path} HTTP/1.1\r\n'
                f'Content-Type: application/hap+json\r\n'
                f'Content-Length: {len(body) if body else 0}\r\n'
                f'\r\n'
                f'{body if body else ""}'
            )
        )

    def get(self, path, params=None):
        if params:
            path += '?'
            for key, value in params.items():
                path += f'{key}={value}&'
            path = path[:-1]
        self.response_sem = Semaphore(0)
        self.loop.call_soon_threadsafe(
            self._send, f'GET {path} HTTP/1.1\r\n\r\n')
        self.response_sem.acquire(timeout=10)
        return self.responseBody

    def put(self, path, body):
        self.response_sem = Semaphore(0)
        self.loop.call_soon_threadsafe(
            self._send,
            (
                f'PUT {path} HTTP/1.1\r\n'
                f'Content-Type: application/hap+json\r\n'
                f'Content-Length: {len(body)}\r\n'
                f'\r\n'
                f'{body}'
            )
        )
        self.response_sem.acquire(timeout=5)
        return self.responseBody

    def _send(self, data):
        if self.is_secure:
            self.socket.send(len(data).to_bytes(2, 'little'))

            nonce = b'\x00' * 4 + self.sendSeq.to_bytes(8, 'little')
            add = len(data).to_bytes(2, 'little')
            self.socket.send(self.SendCipher.encrypt(
                nonce, data.encode('utf-8'), add))

            self.sendSeq += 1
        else:
            self.socket.send(data.encode('utf-8'))

    def recv_response(self):
        body = b''
        p = HttpParser()
        while True:
            data = self.socket.recv(1024)
            p.execute(data, len(data))
            if p.is_partial_body():
                body += p.recv_body()
            if p.is_message_complete():
                return body.decode('utf-8')

    async def recv(self, total_len):
        data = b''
        recved_len = 0
        while True:
            recved_data = await self.loop.sock_recv(self.socket, total_len - recved_len)
            data += recved_data
            recved_len += len(recved_data)
            if recved_len == total_len:
                return data

    async def recv_task(self):
        body = b''
        p = HttpParser()
        try:
            while True:
                len = int.from_bytes(await self.recv(2), 'little')
                msg = await self.recv(len + 16)

                nonce = b'\x00' * 4 + self.recvSeq.to_bytes(8, 'little')
                add = len.to_bytes(2, 'little')
                data = self.recvCipher.decrypt(nonce, msg, add)

                self.recvSeq += 1

                p.execute(data, len)
                if p.is_partial_body():
                    body += p.recv_body()

                if p.is_message_complete():
                    if p.protocol == 'HTTP':
                        self.responseBody = body.decode('utf-8')
                        self.response_sem.release()
                    else:
                        self.loop.run_in_executor(
                            None,
                            partial(
                                self.on_event,
                                client=self,
                                event=json.loads(body.decode('utf-8'))
                            )
                        )
                    body = b''
                    p = HttpParser()
        except:
            pass
        finally:
            self.socket.close()
            self.connected = False
            self.is_secure = False
            if self.response_sem:
                self.response_sem.release()
            self.loop.run_in_executor(None, self.on_disconnect, self)


class HomeClient(HTTPClient):
    def __init__(self, host, port, username, password):
        super().__init__()
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.home_db = None
        self.lights = []
        self.on_event = self._on_event

    def _on_event(self, client, event):
        if "attributes" in event:
            self._on_attrs(event["attributes"])

    def connect(self):
        if super().connect(self.host, self.port, self.username, self.password):
            self.home_db = json.loads(self.get('/home'))
            for device in self.home_db['devices']:
                for index, service in enumerate(device['services']):
                    if service['type'] == ServiceType.LIGHT:
                        self.lights.append(
                            Light(
                                self,
                                device['name'],
                                device['did'],
                                index,
                                service['attributes']
                            )
                        )
            return True
        return False

    def set_scene(self, sid):
        return self.put('/scenes', json.dumps({'scenes': [{'sid': sid}]}))

    def set_attr(self, did, iid, value):
        return self.put('/attributes', json.dumps({'attributes': [{'did': did, 'iid': iid, 'value': value}]}))

    def attr_type(self, did, iid):
        if self.home_db is None:
            return None
        for device in self.home_db['devices']:
            if device['did'] == did:
                for service in device['services']:
                    for attr in service['attributes']:
                        if attr['iid'] == iid:
                            return attr['type']
        return None

    def _on_attrs(self, attrs):
        for attr in attrs:
            did, iid, value = attr['did'], attr['iid'], attr['value']
            for light in self.lights:
                if did == light.did:
                    light.changed_attrs = set()
                    light._onoff = 1
                    if iid == light.onoff_iid:
                        light._onoff = value
                        light.changed_attrs.add(AttrType.ONOFF)
                    elif iid == light.brightness_iid:
                        light._brightness = value
                        light.changed_attrs.add(AttrType.BRIGHTNESS)
                    elif iid == light.colortemp_iid:
                        light._colortemp = value
                        light.changed_attrs.add(AttrType.COLOR_TEMPERATURE)
                    elif iid == light.hsv_iid:
                        light._hsv = (
                            value['hue'],
                            value['saturation'],
                            value['brightness']
                        )
                        light.changed_attrs.add(AttrType.HSV)

        for light in self.lights:
            if light.changed_attrs:
                light.on_state_change(light, light.changed_attrs)
                light.changed_attrs = set()


LIGHT_MODE_COLOR_TEMP = 0x00
LIGHT_MODE_HSV = 0x01


class Light():

    def __init__(self, client: HomeClient, name, did, iid, attrs):
        self.client = client
        self.name = name
        self.did = did
        self.iid = iid
        self.supported_modes = []
        for attr in attrs:
            if attr['type'] == AttrType.ONOFF:
                self.onoff_iid = attr['iid']
            elif attr['type'] == AttrType.BRIGHTNESS:
                self.brightness_iid = attr['iid']
            elif attr['type'] == AttrType.COLOR_TEMPERATURE:
                self.colortemp_iid = attr['iid']
                self.supported_modes.append(LIGHT_MODE_COLOR_TEMP)
            elif attr['type'] == AttrType.HSV:
                self.hsv_iid = attr['iid']
                self.supported_modes.append(LIGHT_MODE_HSV)
        self.changed_attrs = set()
        self.on_state_change = lambda light, attrs: None

    @property
    def onoff(self):
        return self._onoff

    @onoff.setter
    def onoff(self, value):
        self.client.set_attr(self.did, self.onoff_iid, value)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self.client.set_attr(self.did, self.brightness_iid, value)

    @property
    def colortemp(self):
        return self._colortemp

    @colortemp.setter
    def colortemp(self, value):
        self.client.set_attr(self.did, self.colortemp_iid, value)

    @property
    def hsv(self):
        return self._hsv

    @hsv.setter
    def hsv(self, value):
        self.client.set_attr(
            self.did,
            self.hsv_iid,
            {
                'hue': value[0],
                'saturation': value[1],
                'brightness': value[2]
            }
        )

    def toggle(self):
        self.client.set_attr(self.did, self.onoff_iid, 2)
