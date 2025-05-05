from fastapi import APIRouter, status

from presentation.dependencies import OrchestratorServiceDependency
from presentation.schemas.ice_breaker import IceBreakerRequest, IceBreakerResponse

router = APIRouter(prefix="/ice-breaker")


@router.post("/generate", status_code=status.HTTP_200_OK, response_model=IceBreakerResponse)
def generate_ice_breaker(request: IceBreakerRequest, service: OrchestratorServiceDependency) -> IceBreakerResponse:
    ice_breaker: IceBreakerResponse = service.ice_break_with(request.name)
    return ice_breaker
