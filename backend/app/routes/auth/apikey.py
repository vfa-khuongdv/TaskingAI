from ..utils import auth_info_required
from fastapi import APIRouter, Depends, Request
from common.database.postgres.pool import postgres_db_pool
from typing import Dict
from common.services.auth.apikey import *
from app.schemas.auth.apikey import *
from app.schemas.base import BaseSuccessEmptyResponse, BaseSuccessDataResponse, BaseSuccessListResponse
from common.models import Apikey, SerializePurpose

router = APIRouter()


@router.get(
    "/apikeys",
    tags=["API Key"],
    summary="List API Keys",
    operation_id="list_apikeys",
    response_model=BaseSuccessListResponse,
)
async def api_list_apikeys(
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    apikeys, total, has_more = await list_apikeys(postgres_conn)
    return BaseSuccessListResponse(
        data=[apikey.to_dict(purpose=SerializePurpose.RESPONSE) for apikey in apikeys],
        fetched_count=len(apikeys),
        total_count=total,
        has_more=has_more,
    )


@router.get(
    "/apikeys/{apikey_id}",
    tags=["API Key"],
    summary="Get API Key",
    operation_id="get_apikey",
    response_model=BaseSuccessDataResponse,
)
async def api_get_apikey(
    apikey_id: str,
    request: Request,
    data: GetApikeyRequest = Depends(),
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    apikey: Apikey = await get_apikey(
        postgres_conn=postgres_conn,
        apikey_id=apikey_id,
    )
    return BaseSuccessDataResponse(data=apikey.to_dict(purpose=SerializePurpose.RESPONSE, plain=data.plain))


@router.post(
    "/apikeys",
    tags=["API Key"],
    summary="Create API Key",
    operation_id="create_apikey",
    response_model=BaseSuccessDataResponse,
)
async def api_create_apikey(
    request: Request,
    data: CreateApikeyRequest,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    apikey: Apikey = await create_apikey(
        postgres_conn=postgres_conn,
        name=data.name,
    )
    return BaseSuccessDataResponse(data=apikey.to_dict(purpose=SerializePurpose.RESPONSE))


@router.post(
    "/apikeys/{apikey_id}",
    tags=["API Key"],
    summary="Update API Key",
    operation_id="update_apikey",
    response_model=BaseSuccessDataResponse,
)
async def api_update_apikey(
    apikey_id: str,
    request: Request,
    data: UpdateApikeyRequest,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    apikey: Apikey = await update_apikey(
        postgres_conn=postgres_conn,
        apikey_id=apikey_id,
        name=data.name,
    )
    return BaseSuccessDataResponse(data=apikey.to_dict(purpose=SerializePurpose.RESPONSE))


@router.delete(
    "/apikeys/{apikey_id}",
    tags=["API Key"],
    summary="Delete API Key",
    operation_id="delete_apikey",
    response_model=BaseSuccessEmptyResponse,
)
async def api_delete_apikey(
    apikey_id: str,
    request: Request,
    auth_info: Dict = Depends(auth_info_required),
    postgres_conn=Depends(postgres_db_pool.get_db_connection),
):
    await delete_apikey(
        postgres_conn=postgres_conn,
        apikey_id=apikey_id,
    )
    return BaseSuccessEmptyResponse()
