# import pytest
# from fastapi.testclient import TestClient
# from unittest.mock import patch, MagicMock, ANY
# from main import app
# import io
# from PIL import Image
#
# client = TestClient(app)
#
# @pytest.fixture
# def mock_session():
#     return MagicMock()
#
# @pytest.fixture
# def mock_png_image():
#     # Создаем тестовое изображение PNG
#     image = Image.new('RGB', (100, 100), color='red')
#     img_byte_arr = io.BytesIO()
#     image.save(img_byte_arr, format='PNG')
#     img_byte_arr = img_byte_arr.getvalue()
#     return img_byte_arr
#
# def test_add_document(mock_session):
#     mock_data = {"path": "/home/evgeniy/PycharmProjects/fastapi_ubuntu/documents/test10.png", "date": "2023-07-20"}
#     with patch("router.add_date", return_value=mock_data) as mock_add_date:
#         response = client.post("/table/add_date/", json=mock_data)
#
#     assert response.status_code == 200
#     assert response.json() == {"ok": True, "date_id": mock_data["id"]}
#     mock_add_date.assert_called_once_with(mock_data)
# #
# def test_get_documents(mock_session):
#     mock_documents = [{"id": 1, "path": "documents/test.png", "date": "2023-07-20"}]
#     with patch("router.get_dates", return_value=mock_documents) as mock_get_dates:
#         response = client.get("/table/get_date/")
#
#     assert response.status_code == 200
#     assert response.json() == mock_documents
#     mock_get_dates.assert_called_once()
#
# def test_upload_doc(mock_png_image):
#     with patch("router.upload_doc",
#                return_value={"id": 1, "path": "documents/test.png", "date": "2023-07-20"}) as mock_upload:
#         response = client.post("/table/upload_doc/", files={"file": ("test.png", mock_png_image, "image/png")})
#
#     assert response.status_code == 200
#     assert response.json() == {"id": 1, "path": "documents/test.png", "date": "2023-07-20"}
#     mock_upload.assert_called_once()
#
# def test_analyze_doc():
#     with patch("router.get_item", return_value=MagicMock(path="documents/test.png")) as mock_get_item, \
#             patch("os.path.abspath",
#                   return_value="/home/evgeniy/PycharmProjects/FastAPI/documents/test.png") as mock_abspath, \
#             patch("celery_worker.get_text.delay",
#                   return_value=MagicMock(get=MagicMock(return_value="Extracted text from image"))) as mock_get_text, \
#             patch("work.main_document_text.create_to_database", return_value={
#                 "Message": "Задача на анализ и добавление в базу данных документа с id 1 успешно завершена"}) as mock_create:
#         response = client.post("/table/doc_analyze/1/")
#
#     assert response.status_code == 200
#     assert response.json() == {"Message": "Задача на анализ и добавление в базу данных документа с id 1 успешно завершена"}
#     mock_get_item.assert_called_once_with(1, ANY)
#     assert "/home/evgeniy/PycharmProjects/FastAPI/documents/test.png" in mock_abspath.call_args[0]
#     mock_get_text.assert_called_once()
#     expected_path = "/home/evgeniy/PycharmProjects/FastAPI/documents/test.png"
#     assert mock_get_text.call_args[0][0] == expected_path
#     mock_create.assert_called_once()
#
# def test_analyze_doc_not_found():
#     with patch("router.get_doc_text", return_value=None) as mock_get_item:
#         response = client.post("/table/doc_analyze/1/")
#
#     assert response.status_code == 200
#     assert response.json() == {'Message': 'Документ с номером 1 не существует в базе данных'}
#     mock_get_item.assert_called_once()
#     assert mock_get_item.call_args[0][0] == 1
#
# def test_doc_delete():
#     with patch("router.doc_delete", return_value={"Message": "Документ успешно удален"}) as mock_delete:
#         response = client.delete("/table/doc_delete/1/")
#
#     assert response.status_code == 200
#     assert response.json() == {"Message": "Документ успешно удален"}
#     mock_delete.assert_called_once()
#     assert mock_delete.call_args[0][0] == 1



