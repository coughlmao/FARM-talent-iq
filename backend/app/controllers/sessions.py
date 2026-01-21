import time
import uuid

from beanie.operators import Or
from fastapi import HTTPException, status

from ..lib.config import settings
from ..lib.stream import (
    chat_features,
    create_stream_token,
    upsert_stream_user,
    video_features,
)
from ..models.session import Session, SessionStatus
from ..models.user import User


async def create_session(data: dict, current_user: User):
    try:
        problemTitle = data.get("problemTitle")
        difficulty = data.get("difficulty")

        if not problemTitle or not difficulty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Problem and difficulty are required",
            )

        await upsert_stream_user(
            {
                "id": current_user.clerk_id,
                "name": current_user.name,
                "image": current_user.profile_image,
            }
        )

        timestamp = int(time.time())
        unique_suffix = uuid.uuid4().hex[:12]
        call_id = f"session_{timestamp}_{unique_suffix}"

        # 1. Create Session in MongoDB
        new_session = Session(
            problemTitle=problemTitle,
            difficulty=difficulty,
            host=current_user,
            call_id=call_id,
        )
        await new_session.create()

        # 2. Create Video Call in Stream
        call = video_features.call("default", call_id)
        call.get_or_create(
            data={
                "created_by_id": current_user.clerk_id,
                "custom": {
                    "problemTitle": problemTitle,
                    "difficulty": difficulty,
                    "session_id": str(new_session.id),
                },
            },
        )

        # Create Chat messaging Channel in Stream
        channel = chat_features.channel("messaging", call_id)
        channel.get_or_create(
            data={
                "name": f"{problemTitle} Session",
                "members": [current_user.clerk_id],
                "created_by_id": current_user.clerk_id,
            },
            hide_for_creator=False,
        )

        stream_token = create_stream_token(current_user.clerk_id)

        return {
            "session": new_session,
            "stream_token": stream_token,
            "stream_api_key": settings.STREAM_API_KEY,
            "user_id": current_user.clerk_id,
        }

    except HTTPException:
        raise
    except Exception as err:
        print(f"Error in create_session: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Session creation failed: {str(err)}",
        ) from err


# Get active sessions
# Query with Filters, Sorting, and Limits
# sort("-created_at") matches .sort({ createdAt: -1 })
# fetch_links=True matches .populate() for host and participant
async def get_active_sessions():
    try:
        sessions = (
            await Session.find(
                Session.status == SessionStatus.active,
                fetch_links=True,
            )
            .sort("-created_at")
            .limit(20)
            .to_list()
        )

        return {"sessions": sessions}

    except Exception as err:
        print(f"Error in get_active_sessions controller: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from err


# Get recent sessions for current user
async def get_my_recent_session(current_user: User):
    try:
        # get sessions where user is either host or participant and status is completed
        # fetch_links=True is used if you want to populate host/participant data
        sessions = (
            await Session.find(
                Session.status == SessionStatus.completed,
                Or(
                    Session.host.id == current_user.id,
                    Session.participant.id == current_user.id,
                ),
                fetch_links=True,
            )
            .sort("-created_at")
            .limit(20)
            .to_list()
        )

        return {"sessions": sessions}

    except Exception as err:
        print(f"Error in get_my_recent_sessions controller: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from err


# Get session by ID
async def get_session_by_id(id: str):
    try:
        # Fetch by ID and populate links
        # .get() is the equivalent of Mongoose.findById()
        #   fetch_links=true handles the .populate() for host and participant
        session = await Session.get(id, fetch_links=True)

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        return {"session": session}

    except HTTPException:
        # Check if the error is already a handled 404
        raise
    except Exception as err:
        print(f"Error in get_session_by_id controller: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from err


# Joining session
async def join_session(id: str, current_user: User):
    try:
        # Fetch the session and populate links(similiar to .findById(id))
        session = await Session.get(id, fetch_links=True)

        # Check existence
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found",
            )

        if session.status != SessionStatus.active:
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

        print(f"Error in join_session controller: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from err

    # Check if session is already full(has a partcipant)
    if session.participant:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Session is full",
        )

    # Update participant in MongoDB
    session.participant = current_user
    await session.save()

    # 3. Add member to Stream Chat Channel
    # Note: Using your existing 'chat_features' and 'session.call_id'

    try:
        # Stream logic
        channel = chat_features.channel("messaging", session.call_id)
        await channel.add_members([current_user.clerk_id])

        return {"session": session}

    except HTTPException:
        # Re-raise without modification
        raise
    except Exception as error:
        # Log exactly like your Node.js code
        print(f"Error in joinSession controller: {str(error)}")

        # Use 'from error' to keep the exception chain for the Stream failure
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        ) from error


# end session
async def end_session(id: str, current_user: User):
    try:
        session = await Session.get(id, fetch_links=True)

        # Check if session exists
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
            )

        # Check if user is the host
        # Comparing IDs as strings is safest for MongoDB ObjectIds
        if str(session.host.id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the host can end the session",
            )

        # Check if session is already completed
        if session.status == SessionStatus.completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is already completed",
            )

        # 1. Delete Stream Video Call
        # Matches: const call = streamClient.video.call("default", session.callId);
        # await call.delete({ hard: true });
        call = video_features.call("default", session.call_id)
        call.delete()  # Note: Stream Python SDK delete is often hard-delete by default or check your specific wrapper

        # 2. Delete Stream Chat Channel
        # Matches: const channel = chatClient.channel("messaging", session.callId);
        # await channel.delete();
        channel = chat_features.channel("messaging", session.call_id)
        channel.delete()

        # 3. Update Session Status in MongoDB
        # Matches: session.status = "completed"; await session.save();
        session.status = SessionStatus.completed
        await session.save()

        # 4. Success Response
        # Matches: res.status(200).json({ session, message: "Session ended successfully" });
        return {"session": session, "message": "Session ended successfully"}

    except HTTPException:
        # Re-raise handled HTTP errors
        raise
    except Exception as err:
        # Log the error and raise 500
        print(f"Error in end_session controller : {str(err)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from err
