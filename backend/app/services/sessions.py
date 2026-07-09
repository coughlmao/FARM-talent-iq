from beanie import PydanticObjectId
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.logger import logger
from app.models.session import Session, SessionStatus
from app.models.user import User
from app.repositories.session import (
    create,
    get_by_id,
    list_active,
    list_recent,
    save,
)
from app.schemas.session import (
    SessionCreateRequest,
    SessionCreateResponse,
    SessionDetailResponse,
    SessionEndResponse,
    SessionJoinResponse,
    SessionListResponse,
)

from .session_ids import generate_call_id
from .stream import (
    build_stream_token,
    get_chat_channel,
    get_video_call,
    upsert_stream_user,
)


async def create_session(
    data: SessionCreateRequest,
    current_user: User,
) -> SessionCreateResponse:
    try:
        problem_title = data.problem_title
        difficulty = data.difficulty

        await upsert_stream_user(current_user)

        call_id = generate_call_id()

        # 1. Create Session in MongoDB
        new_session = Session(
            problem_title=problem_title,
            difficulty=difficulty,
            host=current_user,
            call_id=call_id,
        )
        await create(new_session)

        # 2. Create Video Call in Stream
        call = get_video_call(call_id)
        call.get_or_create(
            data={
                "created_by_id": current_user.clerk_id,
                "custom": {
                    "problemTitle": problem_title,
                    "difficulty": difficulty,
                    "session_id": str(new_session.id),
                },
            },
        )

        # Create Chat messaging Channel in Stream
        channel = get_chat_channel(call_id)
        channel.get_or_create(
            data={
                "name": f"{problem_title} Session",
                "members": [current_user.clerk_id],
                "created_by_id": current_user.clerk_id,
            },
            hide_for_creator=False,
        )

        stream_token = build_stream_token(current_user)

        return SessionCreateResponse(
            session=new_session,
            stream_token=stream_token,
            stream_api_key=settings.STREAM_API_KEY,
            user_id=current_user.clerk_id,
        )

    except HTTPException:
        raise

    except Exception as err:
        logger.exception("Failed to create session.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Session creation failed.",
        ) from err


# Get active sessions
# Query with Filters, Sorting, and Limits
# sort("-created_at") matches .sort({ createdAt: -1 })
# fetch_links=True matches .populate() for host and participant
async def list_active_sessions() -> SessionListResponse:
    try:
        sessions = await list_active()

        return SessionListResponse(
            sessions=sessions,
        )

    except Exception as err:
        logger.exception("Failed to fetch active sessions.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fetching active session failed.",
        ) from err


# Get recent sessions for current user
async def list_recent_sessions(
    current_user: User,
) -> SessionListResponse:
    try:
        # get sessions where user is either host or participant and status is completed
        # fetch_links=True is used if you want to populate host/participant data
        sessions = await list_recent(current_user)

        return SessionListResponse(
            sessions=sessions,
        )

    except Exception as err:
        logger.exception("Failed to fetch recent sessions.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Fetching recent sessions failed.",
        ) from err


# Get session by ID
async def get_session(
    session_id: PydanticObjectId,
) -> SessionDetailResponse:
    try:
        # Fetch by ID and populate links
        # .get() is the equivalent of Mongoose.findById()
        #   fetch_links=true handles the .populate() for host and participant
        session = await get_by_id(session_id)

        if session is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        return SessionDetailResponse(
            session=session,
        )

    except HTTPException:
        # Check if the error is already a handled 404
        raise

    except Exception as err:
        logger.exception("Failed to fetch session.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Session fetching failed.",
        ) from err


# Joining session
async def join_session(
    session_id: PydanticObjectId,
    current_user: User,
) -> SessionJoinResponse:
    try:
        # Fetch the session and populate links(similiar to .findById(session_id))
        session = await get_by_id(session_id)

        # Check existence
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        if session.status != SessionStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot join a completed session",
            )

        # Prevent host from joining own session (session.host.ttoString() === userId.toString())
        # We compare the IDs directly as Beanie handles the ObjectId object
        if str(session.host.id) == str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Host cannot join their own session as participant",
            )

    except HTTPException:
        raise

    except Exception as err:
        # Catch unexpected error(DB connection,Stream API failure,etc)
        logger.exception("Failed while validating join request..")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Session joining failed.",
        ) from err

    # Check if session is already full(has a partcipant)
    if session.participant:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Session is full",
        )

    # Update participant in MongoDB
    session.participant = current_user
    await save(session)

    # 3. Add member to Stream Chat Channel
    # Note: Using your existing 'chat_features' and 'session.call_id'

    try:
        # Stream logic
        channel = get_chat_channel(session.call_id)
        await channel.add_members([current_user.clerk_id])

        return SessionJoinResponse(
            session=session,
        )

    except HTTPException:
        # Re-raise without modification
        raise

    except Exception as error:
        # Log exactly like your Node.js code
        logger.exception("Failed while updating Stream channel.")

        # Use 'from error' to keep the exception chain for the Stream failure
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to join session.",
        ) from error


# end session
async def end_session(
    session_id: PydanticObjectId,
    current_user: User,
) -> SessionEndResponse:
    try:
        session = await get_by_id(session_id)

        # Check if session exists
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        # Check if user is the host
        # Comparing IDs as strings is safest for MongoDB ObjectIds
        if str(session.host.id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the host can end the session",
            )

        # Check if session is already completed
        if session.status == SessionStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is already completed",
            )

        # 1. Delete Stream Video Call
        # Matches: const call = streamClient.video.call("default", session.callId);
        # await call.delete({ hard: true });
        call = get_video_call(session.call_id)
        call.delete()  # Note: Stream Python SDK delete is often hard-delete by default or check your specific wrapper

        # 2. Delete Stream Chat Channel
        # Matches: const channel = chatClient.channel("messaging", session.callId);
        # await channel.delete();
        channel = get_chat_channel(session.call_id)
        channel.delete()

        # 3. Update Session Status in MongoDB
        # Matches: session.status = "completed"; await session.save();
        session.status = SessionStatus.COMPLETED
        await save(session)

        # 4. Success Response
        # Matches: res.status(200).json({ session, message: "Session ended successfully" });
        return SessionEndResponse(
            session=session,
            message="Session ended successfully",
        )

    except HTTPException:
        # Re-raise handled HTTP errors
        raise

    except Exception as err:
        # Log the error and raise 500
        logger.exception("Failed to end session.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Session ending failed.",
        ) from err
