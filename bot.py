import os
import requests
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

PROXMOX_HOST = os.getenv('PROXMOX_HOST')
PROXMOX_TOKEN = os.getenv('PROXMOX_TOKEN')
VMID = os.getenv('VMID')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
allowed_users_str = os.getenv('ALLOWED_USERS')
if allowed_users_str: allowed_users = list(map(int, allowed_users_str.split(',')))
else: allowed_users = []


def get_vm_status(vmid):
    url = f"{PROXMOX_HOST}/api2/json/nodes/pve/qemu/{vmid}/status/current"
    headers = { 'Authorization': f'PVEAPIToken={PROXMOX_TOKEN}', }
    response = requests.get(url, headers=headers, verify=False)
    return response.json()['data']['status']


def start_vm(vmid):
    status = get_vm_status(vmid)
    if status == 'running': return {'message': 'VM is already running.'}

    url = f"{PROXMOX_HOST}/api2/json/nodes/pve/qemu/{vmid}/status/start"
    headers = {'Authorization': f'PVEAPIToken={PROXMOX_TOKEN}',}
    response = requests.post(url, headers=headers, verify=False)
    return response.json()


def stop_vm(vmid):
    status = get_vm_status(vmid)
    if status == 'stopped': return {'message': 'VM is already stopped.'}

    url = f"{PROXMOX_HOST}/api2/json/nodes/pve/qemu/{vmid}/status/stop"
    headers = {'Authorization': f'PVEAPIToken={PROXMOX_TOKEN}',}
    response = requests.post(url, headers=headers, verify=False)
    return response.json()

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


def is_user_allowed(user_id):
    return user_id in allowed_users


@dp.message(Command('start'))
async def handle_start_command(message: Message):
    if is_user_allowed(message.from_user.id):
        response = start_vm(VMID)
        await message.answer(f'Start VM: {response.get("message", response)}')
    else:
        await message.answer('You are not authorized to use this bot.')


@dp.message(Command('stop'))
async def handle_stop_command(message: Message):
    if is_user_allowed(message.from_user.id):
        response = stop_vm(VMID)
        await message.answer(f'Stop VM: {response.get("message", response)}')
    else:
        await message.answer('You are not authorized to use this bot.')


@dp.message(Command('status'))
async def handle_status_command(message: Message):
    if is_user_allowed(message.from_user.id):
        status = get_vm_status(VMID)
        await message.answer(f'VM status: {status}')
    else:
        await message.answer('You are not authorized to use this bot.')

async def main():
    await dp.start_polling(bot)


asyncio.run(main())

