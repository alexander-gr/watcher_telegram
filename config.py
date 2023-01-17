import os

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Group_id or user_id to forward the message
TARGET_GROUP_ID = 1845926666
ADMIN_ID = 343868413

CONFIG = {
    1429590454: {
        "name": "Пивоваров (Редакция)", "pattern": ["#ньюсдня", "фото дня"], "target_id": TARGET_GROUP_ID,
    },
    1380524958: {
        "name": "Хулиномика", "pattern": ["#Хулиновости"], "target_id": TARGET_GROUP_ID,
    },
    1078868616: {
        "name": "Зеркало | Новости", "pattern": ["#главное_за_день"], "target_id": TARGET_GROUP_ID,
    },
}
