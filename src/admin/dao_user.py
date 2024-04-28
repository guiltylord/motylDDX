# dao.py – DAO (Data Access Object) является распространённым шаблоном и подходит для файлов,
# содержащих классы или функции, которые производят непосредственный доступ к данным.

from sqlalchemy import select, func

from src.database import async_session_maker, User


# TODO: сделать проверку исключений везде чтоб сервак не падал
async def getRowCount():
    async with async_session_maker() as session:
        result = await session.execute(select(func.count()).select_from(User))
        count = result.scalar_one()
        return count


async def getHashUser(user_id: int):
    async with async_session_maker() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one()
        if user is not None:
            user_data = {"hash": user.hashed_password}
        return user_data


async def getUserInfo(user_id: int):
    async with async_session_maker() as session:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user is not None:
            # Преобразование экземпляра модели User в словарь
            user_data = {
                column.name: getattr(user, column.name)
                for column in user.__table__.columns
            }
            return user_data
        else:
            return None


async def getUserWeight(user_id: int):
    async with async_session_maker() as session:
        # Сначала извлекаем пользователя по ID
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        user_instance = result.scalar_one_or_none()

        if user_instance:
            size_sum = sum(
                func.pg_column_size(getattr(user_instance, column.name))
                for column in User.__table__.columns
            )
            result = await session.execute(select(size_sum))
            row_size = result.scalar_one()
            return row_size

        else:
            raise ValueError(f"User with id {user_id} does not exist.")
