from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from clerk_backend_api import Clerk
from models.user import User
from config import settings

clerk_client=Clerk(bearer_auth=settings.CLERK_SECRET_KEY)
security=HTTPBearer()

async def protect_route(auth: HTTPAuthorizationCredentials = Depends(security)):
    token = auth.credentials
    
    try:
        request_state = clerk_client.authenticate_request(token)
        
        if not request_state.is_signed_in:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized - invalid token"
            )
        clerk_id = request_state.payload.get("sub")
        
       
        user = await User.find_one({"clerk_id": clerk_id}) 

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        return user 
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in protect_route dependency: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )