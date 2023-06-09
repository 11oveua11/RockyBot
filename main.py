import config
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

# log
logging.basicConfig(level=logging.INFO)

# init
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

# prices
PRICE = types.LabeledPrice(label="Сыыыр...", amount=10*100)

# buy. Покупка и отправка пользователю инвойса платежа
@dp.message_handler(commands="buy") # message_handler - метод обработчика сообщений
async def buy(message: types.Message):
    if config.SBER_TEST_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платёж!")

    await bot.send_invoice(message.chat.id,
                           title="Сыр рокфор",
                           description="Любимый сыр крысы Monty",
                           provider_token=config.SBER_TEST_TOKEN,
                           currency="rub",
                           photo_url="https://avatars.mds.yandex.net/get-goods_pic/6799855/pic75236c1e6370fcfd3e241ec507d4cade/500x500",
                           photo_width=500,
                           photo_height=365,
                           photo_size=500,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-item",
                           payload="test-invoice-payload"
                           )

# pre checkout (ответ должен быть в течении 10 сек.)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

# successful payment (наши действия после успешной оплаты)
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")
    await bot.send_message(message.chat.id,
                           f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")

# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)