import os
import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiohttp import web, request

TOKEN = 'API TOKEN'
APP_NAME = 'NAME OF YOUR APPLICATION'
WEBHOOK = f'https://{APP_NAME}.herokuapp.com/'

routes = web.RouteTableDef()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@routes.post(f'/{TOKEN}')
async def getUpdate(request):
	await dp.updates_handler.notify(types.Update(**(await request.json())))
	return web.Response(text="OK")
@routes.get(f'/')
async def reset_hooks(app):
	await bot.delete_webhook()
	await bot.set_webhook(WEBHOOK+TOKEN)
	return web.Response(text="OK")

app = web.Application()
app.add_routes(routes)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	await bot.send_message(message.chat.id, 'hello!')

if __name__ == '__main__':
	web.run_app(app, port = int(os.environ.get('PORT', 5000))	)
