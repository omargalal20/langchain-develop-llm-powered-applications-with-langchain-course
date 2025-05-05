from fastapi import APIRouter

router = APIRouter(prefix="")


@router.get("/healthy")
def health_check():
    return {'status': 'Healthy'}
