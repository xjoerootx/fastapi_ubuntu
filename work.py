import imghdr
import os
import shutil

from fastapi import UploadFile, File, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from async_session import get_session
from database import Documents, Documents_text


class Document_Main:
    async def upload_doc(self, file: UploadFile = File(), session: AsyncSession = Depends(get_session)):
        """
        Загружает файл, проверяет тип и сохраняет на диск

        Args:
            file (UploadFile): Загружаемый файл
            session (AsyncSession): Асинхронная сессия

        Returns:
            Dict: Словарь с информацией о загруженном документе или сообщением об ошибке
        """
        file_bytes = await file.read()
        await file.seek(0)
        file_type = imghdr.what(None, h=file_bytes)
        if not file_type:
            return {"Message": "The file is not an image."}
        save_path = os.path.abspath(f"documents/{file.filename}")
        if not os.path.exists(save_path):
            with open(save_path, 'wb') as buffer:
                shutil.copyfileobj(file.file, buffer, length=16384)

            document = Documents(path=save_path)
            session.add(document)
            await session.commit()
            await session.refresh(document)
            return {"id": document.id,
                    "path": document.path,
                    "date": document.date
                    }

        return {"Message": f'Файл {file.filename} уже существует!'}

    async def get_item(self, id_doc, session: AsyncSession):
        document = await session.get(Documents, id_doc)
        return document

    async def doc_delete(self, id_doc: int, session: AsyncSession):
        document = await session.get(Documents, id_doc)

        if document:
            file_path = document.path
            if os.path.exists(file_path):
                os.remove(file_path)
            else:
                return {'Message': 'Файл не найден на диске'}

            await session.delete(document)
            await session.commit()
            return {"Message": f'Документ с id {id_doc} успешно удален из диска и базы данных'}
        else:
            return {"Message": f'Документ с id {id_doc} не найден в базе данных'}

class Document_Text_Main:
    async def create_to_database(self, id_doc: int, text: str, session: AsyncSession):
        data = Documents_text(id_doc=id_doc, text=text)
        session.add(data)
        await session.commit()
        return {"Message": f"Задача на анализ и добавление в базуданных документа с id {id_doc} успешно заверешна"}

    async def get_doc_text(self, id_doc: int, session: AsyncSession):
        db_item = await session.execute(select(Documents_text).where(Documents_text.id_doc == id_doc).order_by())
        return db_item.scalar_one_or_none()

main_document_text = Document_Text_Main()
main_document = Document_Main()