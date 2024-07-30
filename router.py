import os
from datetime import datetime
from typing import Annotated, List

from fastapi import Depends, APIRouter, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from async_session import new_session, get_session
from celery_worker import get_text
from database import Documents, init_tables
from schemas import DocumentsAdd, DocumentstextAdd
from work import main_document_text, main_document

router = APIRouter(
    prefix="/table",
    tags=["Документы"]
)
@router.on_event("startup")
async def startup_event() -> None:
    """
    :return
           Инициализация таблиц
    """
    await init_tables()

#ВВОД ДАННЫХ В ТАБЛИЦУ
@router.post("/add_date/")
async def add_date(date: DocumentsAdd):
    """
    :param date: Данные для добавления нового документа
    :return: Результаты операции и id нового документа
    """
    async with new_session() as session:
        task = Documents(**date.dict())
        session.add(task)
        await session.flush()
        await session.commit()
        return {"ok": True, "date_id": task.id}

#ЧТЕНИЕ ДАННЫХ ТАБЛИЦЫ
@router.get("/get_date/", response_model=List[DocumentsAdd])
async def get_dates():
    """
    Получение данных из таблицы Documents

    :return: id документа и связанные с ним данные
    """
    async with new_session() as session:
        query = select(Documents)
        result = await session.execute(query)
        task_models = result.scalars().all()

        task_schemas = [
            DocumentsAdd(
                id=task_model.id,
                path=task_model.path,
                date=task_model.date.date() if isinstance(task_model.date, datetime) else task_model.date
            )
            for task_model in task_models
        ]
        return task_schemas


@router.post('/upload_doc/', response_model=DocumentsAdd)
async def upload_doc(file: UploadFile = File(), session: AsyncSession = Depends(get_session)):
    """
    Загружает файл
    :param
          file: Загружаемый файл
    :return
          Ответ с информацией о загруженном документе
    """
    upload_image_result = await main_document.upload_doc(file, session)
    return upload_image_result

@router.delete('/doc_delete/{id_doc}/')
async def doc_delete(id_doc: int, session: AsyncSession = Depends(get_session)):
    """
    Удаляет документ из системы по его id
    :param
          id_doc: id документа для удаления
    :return
          Ответ с информацией об удалении документа
    """
    delete_document_result = await main_document.doc_delete(id_doc, session)
    return delete_document_result


@router.post('/doc_analyze/{id_doc}/')
async def analyze_doc(id_doc: int, session: AsyncSession = Depends(get_session)):
    """
    Анализирует файл и сохраняет извлеченный текст в базу данных
    :param
          id_doc: id документа для анализа
    :return
          Ответ с информацией об анализе документа и сохранении текста.
    """
    document_from_db = await main_document.get_item(id_doc, session)
    if document_from_db:
        path_to_document = os.path.abspath(document_from_db.path)
        get_text_from_image = get_text.delay(str(path_to_document))
        get_text_from_image = str(get_text_from_image.get(timeout=1000)).replace('\n', '')
        add_text_to_db_result = await main_document_text.create_to_database(id_doc, get_text_from_image, session)
        return add_text_to_db_result
    else:
        return {'Message': f'Документ с номером {id_doc} не существует в базе данных'}

@router.get('/get_text/{id_doc}/', response_model=DocumentstextAdd)
async def get_text_docs(id_doc: int, session: AsyncSession = Depends(get_session)):
    """
    Получает текст документа по его id
    :param
          id_doc: id документа для получения текста
    :return
          Ответ с текстом  и параметрами документа или ошибка, если документ не найден
    """
    get_document_text_result: str = await main_document_text.get_doc_text(id_doc, session)
    if get_document_text_result:
        return get_document_text_result
    else:
        return {'Message': f'Документа с id {id_doc} нет в базе данных'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)