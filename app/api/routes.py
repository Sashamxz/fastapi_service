from fastapi import  Response, status, Depends, Query, File, UploadFile, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from app import models 
from starlette.responses import FileResponse
from app.config import settings
from app.methods import get_file_from_db, get_file_size, get_files_from_db_limit_offset, save_file_to_uploads, format_filename, \
                    add_file_to_db, delete_file_from_db, delete_file_from_uploads, update_file_in_db
from app.database import get_db



router = APIRouter(prefix='/file')

@router.get('/get', tags=['Get files'], status_code=status.HTTP_200_OK)
async def root(
                # *,
                response: Response,
                id: Optional[List[int]] = Query(None),
                name: Optional[List[str]] = Query(None),
                tag: Optional[List[str]] = Query(None),
                limit: Optional[int] = None,
                offset: Optional[int] = None,
                db: Session = Depends(get_db)
            ):

    # All records by default
    query = db.query(models.Image).all()
    files_in_db = get_files_from_db_limit_offset(db, query, limit, offset)

    if id and not name and not tag:
        query = db.query(models.Image).filter(models.Image.file_id.in_(id)).all()
        files_in_db = get_files_from_db_limit_offset(db, query, limit, offset)

    elif id and name and not tag:
        query = db.query(models.Image).filter(models.Image.file_id.in_(id)) \
                                        .filter(models.Image.name.in_(name)) \
                                        .all()
        files_in_db = get_files_from_db_limit_offset(db, query, limit, offset)

    elif id and name and tag:
        query = db.query(models.Image).filter(models.Image.file_id.in_(id)) \
                                        .filter(models.Image.name.in_(name)) \
                                        .filter(models.Image.tag.in_(tag)) \
                                        .all()
        files_in_db = get_files_from_db_limit_offset(db, query, limit, offset)

    elif id and not name and tag:
        query = db.query(models.Image).filter(models.Image.file_id.in_(id)) \
                                        .filter(models.Image.tag.in_(tag)) \
                                        .all()
        files_in_db = get_files_from_db_limit_offset(db, query, limit, offset)

    elif not id and name and tag:
        query = db.query(models.Image).filter(models.Image.name.in_(name)) \
                                        .filter(models.Image.tag.in_(tag)) \
                                        .all()
        files_in_db = get_files_from_db_limit_offset(db, query, limit, offset)

    elif not id and not name and tag:
        query = db.query(models.Image).filter(models.Image.tag.in_(tag)).all()
        files_in_db = get_files_from_db_limit_offset(db, query, limit, offset)

    elif not id and name and not tag:
        query = db.query(models.Image).filter(models.Image.name.in_(name)).all()
        files_in_db = get_files_from_db_limit_offset(db, query, limit, offset)

    if len(files_in_db) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': 'No results =('}

    response.status_code = status.HTTP_200_OK
    return files_in_db



@router.post('/upload', tags=['Upload'], status_code=status.HTTP_200_OK)
async def upload_file(
                        response: Response,
                        file_id: int,
                        name: Optional[str] = None,
                        tag: Optional[str] = None,
                        file: UploadFile = File(...),
                        db: Session = Depends(get_db)
                    ):

    # Format new filename
    full_name = format_filename(file, file_id, name)

    # Save file
    await save_file_to_uploads(file, full_name)

    # Get file size
    file_size = get_file_size(full_name)

    # Get info from DB
    file_info_from_db = get_file_from_db(db, file_id)

    # Add to DB
    if not file_info_from_db:
        response.status_code = status.HTTP_201_CREATED
        return add_file_to_db(
                                db,
                                file_id=file_id,
                                full_name=full_name,
                                tag=tag,
                                file_size=file_size,
                                file=file
                            )

    # Update in DB
    if file_info_from_db:
        # Delete file from uploads
        delete_file_from_uploads(file_info_from_db.name)

        response.status_code = status.HTTP_201_CREATED
        return update_file_in_db(
                                    db,
                                    file_id=file_id,
                                    full_name=full_name,
                                    tag=tag,
                                    file_size=file_size,
                                    file=file
                                )



@router.get('/download', tags=['Download'], status_code=status.HTTP_200_OK)
async def download_file(
                        response: Response,
                        file_id: int,
                        db: Session = Depends(get_db)
                    ):
    file_info_from_db = get_file_from_db(db, file_id)

    if file_info_from_db:
        file_resp = FileResponse(settings.UPLOADED_FILES_PATH + file_info_from_db.name,
                                media_type=file_info_from_db.mime_type,
                                filename=file_info_from_db.name)
        response.status_code = status.HTTP_200_OK
        return file_resp
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'msg': 'File not found'}



@router.delete("/delete", tags=["Delete"])
async def delete_file(
                        response: Response,
                        file_id: int,
                        db: Session = Depends(get_db)
                    ):
    file_info_from_db = get_file_from_db(db, file_id)

    if file_info_from_db:
        # Delete file from DB
        delete_file_from_db(db, file_info_from_db)

        # Delete file from uploads
        delete_file_from_uploads(file_info_from_db.name)

        response.status_code = status.HTTP_200_OK
        return {'msg': f'File {file_info_from_db.name} successfully deleted'}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'msg': f'File does not exist'}