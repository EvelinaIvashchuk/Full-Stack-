# Лабораторна робота №14. FastAPI-додаток з Ormar-моделями із зовнішніми ключами
# Виконала: Іващук Евеліна

# Головний файл додатку. Містить ендпоїнти для моделей Human і Dog (хід роботи)
# та підключає ендпоїнти моделей Author, Book і Review (самостійне завдання)
# з модуля library.

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Response
from ormar.exceptions import NoMatch
from sqlalchemy.exc import IntegrityError    # порушення цілісності бази даних

from database import database, metadata
from library import router as library_router, seed_data
from models import Dog, Human
from schemas import DogCreate, DogUpdate, HumanCreate, HumanUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код до yield виконується під час запуску додатку:
    # підключаємося до бази даних і створюємо таблиці, якщо їх ще немає
    if not database.is_connected:
        await database.connect()
    async with database.engine.begin() as connection:
        await connection.run_sync(metadata.create_all)
    await seed_data()

    yield    # у цей час додаток працює і обробляє запити

    # Код після yield виконується під час завершення роботи додатку
    if database.is_connected:
        await database.disconnect()


app = FastAPI(title="Library API", lifespan=lifespan)

# Підключаємо ендпоїнти самостійного завдання
app.include_router(library_router)


async def get_human_or_404(human_id: int):
    # Повертає людину або помилку 404, якщо людини з таким номером немає
    try:
        return await Human.objects.get(id=human_id)
    except NoMatch:
        raise HTTPException(status_code=404, detail=f"Human with id {human_id} not found!")


async def get_dog_or_404(dog_id: int):
    # select_related("owner") завантажує разом із собакою дані її власника
    try:
        return await Dog.objects.select_related("owner").get(id=dog_id)
    except NoMatch:
        raise HTTPException(status_code=404, detail=f"Dog with id {dog_id} not found!")


# ---------- Люди ----------

@app.get("/human/", tags=["Human"])
async def get_humans():
    humans = await Human.objects.all()
    return humans


@app.get("/human/{id}", tags=["Human"])
async def get_human_by_id(id: int):
    # Разом з людиною повертаємо список її собак (зворотний зв'язок dogs)
    try:
        return await Human.objects.select_related("dogs").get(id=id)
    except NoMatch:
        raise HTTPException(status_code=404, detail=f"Human with id {id} not found!")


@app.post("/human/", tags=["Human"], status_code=201)
async def create_human(human: HumanCreate):
    return await Human(**human.model_dump()).save()


@app.patch("/human/{id}", tags=["Human"])
async def update_human(id: int, human: HumanUpdate):
    db_human = await get_human_or_404(id)
    # exclude_unset=True залишає лише ті поля, які користувач надіслав у запиті,
    # тому можна оновити, наприклад, тільки вік
    await db_human.update(**human.model_dump(exclude_unset=True))
    return db_human


@app.delete("/human/{id}", tags=["Human"])
async def delete_human(id: int):
    db_human = await get_human_or_404(id)
    try:
        await db_human.delete()
    except IntegrityError:
        # База даних не дозволяє видалити людину, на яку посилаються собаки
        raise HTTPException(status_code=409,
                            detail=f"Human with id {id} owns dogs and cannot be deleted!")
    return Response(status_code=204)


# ---------- Собаки ----------

@app.get("/dog/", tags=["Dog"])
async def get_dogs():
    dogs = await Dog.objects.select_related("owner").all()
    return dogs


@app.get("/dog/{id}", tags=["Dog"])
async def get_dog_by_id(id: int):
    return await get_dog_or_404(id)


@app.post("/dog/", tags=["Dog"], status_code=201)
async def create_dog(dog: DogCreate):
    # Перевіряємо цілісність даних: якщо власника вказано, він має існувати
    if dog.owner is not None:
        await get_human_or_404(dog.owner)
    new_dog = await Dog(**dog.model_dump()).save()
    return await get_dog_or_404(new_dog.id)


@app.patch("/dog/{id}", tags=["Dog"])
async def update_dog(id: int, dog: DogUpdate):
    db_dog = await get_dog_or_404(id)
    data = dog.model_dump(exclude_unset=True)
    if data.get("owner") is not None:
        await get_human_or_404(data["owner"])
    await db_dog.update(**data)
    return await get_dog_or_404(id)


@app.delete("/dog/{id}", tags=["Dog"])
async def delete_dog(id: int):
    db_dog = await get_dog_or_404(id)
    await db_dog.delete()
    return Response(status_code=204)
