import { useState, useEffect } from "react";
import { StreamChat } from "stream-chat";
import toast from "react-hot-toast";

import {
  initializeStreamClient,
  disconnectStreamClient,
} from "../lib/stream.js";
import { sessionApi } from "../api/sessions.js";

const useStreamClient = (session, loadingSession, isHost, isParticipant) => {
  const [streamClient, setStreamClient] = useState(null);
  const [call, setCall] = useState(null);
  const [chatClient, setChatClient] = useState(null);
  const [channel, setChannel] = useState(null);
  const [isInitializingCall, setIsInitializingCall] = useState(true);

  useEffect(() => {
    let videoCall = null;
    let chatClientInstance = null;

    const initCall = async () => {
      if (!session?.callId) return;
      if (!isHost && !isParticipant) return;
      if (session.status === "completed") return;

      try {
        const { token, userId, userName, userImage } =
          await sessionApi.getStreamToken();

        const client = await initializeStreamClient(
          {
            id: userId,
            name: userName,
            image: userImage,
          },
          token,
        );

        setStreamClient(client);

        videoCall = client.call("default", session.callId);
        await videoCall.join({ create: true });
        setCall(videoCall);

        const apiKey = import.meta.env.VITE_STREAM_API_KEY;
        chatClientInstance = StreamChat.getInstance(apiKey);

        await chatClientInstance.connectUser(
          {
            id: userId,
            name: userName,
            image: userImage,
          },
          token,
        );
        setChatClient(chatClientInstance);

        const chatChannel = chatClientInstance.channel(
          "messaging",
          session.callId,
        );
        await chatChannel.watch();
        setChannel(chatChannel);
      } catch (error) {
        toast.error("Failed to join video call");
        console.error("Error init call", error);
      } finally {
        setIsInitializingCall(false);
      }
    };

    if (session && !loadingSession) initCall();

    // cleanup - performance reasons
    return () => {
      // iife
      (async () => {
        try {
          if (videoCall) {
            try {
              await videoCall.leave();
            } catch (err) {
              // Ignore "already left" errors
              if (!err.message?.includes("already been left")) {
                console.error("Error leaving call:", err);
              }
            }
          }
          if (chatClientInstance) {
            try {
              await chatClientInstance.disconnectUser();
            } catch (err) {
              console.error("Error disconnecting chat:", err);
            }
          }
          await disconnectStreamClient();
        } catch (error) {
          console.error("Cleanup error:", error);
        }
      })();
    };
  }, [session, loadingSession]);

  return {
    streamClient,
    call,
    chatClient,
    channel,
    isInitializingCall,
  };
};

export default useStreamClient;
