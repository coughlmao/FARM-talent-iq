import { useState, useEffect, useRef } from "react";
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

  const cancelledRef = useRef(false);

  useEffect(() => {
    let videoCall = null;
    let chatClientInstance = null;

    cancelledRef.current = false;

    const initCall = async () => {
      if (!session?.callId || session.status === "completed") return;
      if (!isHost && !isParticipant) return;

      setIsInitializingCall(true);

      try {
        // 1️⃣ Fetch unified token from backend
        const { token, userId, userName, userImage } =
          await sessionApi.getUnifiedStreamToken();

        if (cancelledRef.current) return;

        // 2️⃣ Initialize video client
        const vClient = await initializeStreamClient(
          { id: userId, name: userName, image: userImage },
          token
        );

        if (cancelledRef.current) return;
        setStreamClient(vClient);

        // 3️⃣ Join the call (do NOT create)
        videoCall = vClient.call("default", session.callId);
        await Promise.race([
          videoCall.join(),
          new Promise((_, reject) =>
            setTimeout(
              () => reject(new Error("Video join timeout")),
              10000
            )
          ),
        ]);
        if (cancelledRef.current) return;
        setCall(videoCall);

        // 4️⃣ Connect chat client
        const apiKey = import.meta.env.VITE_STREAM_API_KEY;
        chatClientInstance = StreamChat.getInstance(apiKey);

        await Promise.race([
          chatClientInstance.connectUser(
            { id: userId, name: userName, image: userImage },
            token
          ),
          new Promise((_, reject) =>
            setTimeout(
              () => reject(new Error("Chat connect timeout")),
              10000
            )
          ),
        ]);
        if (cancelledRef.current) return;
        setChatClient(chatClientInstance);

        // 5️⃣ Watch the chat channel
        const chatChannel = chatClientInstance.channel(
          "messaging",
          session.callId
        );
        await chatChannel.watch();
        if (cancelledRef.current) return;
        setChannel(chatChannel);
      } catch (error) {
        if (!cancelledRef.current) {
          console.error("Stream init error:", error);
          toast.error("Failed to join session");
        }
      } finally {
        if (!cancelledRef.current) setIsInitializingCall(false);
      }
    };

    if (session && !loadingSession) initCall();

    return () => {
      cancelledRef.current = true;

      (async () => {
        try {
          if (videoCall) await videoCall.leave();
          if (chatClientInstance) await chatClientInstance.disconnectUser();
          // Only disconnect global singleton if you are sure no one else uses it
          // await disconnectStreamClient();
        } catch (error) {
          console.error("Cleanup error:", error);
        }
      })();
    };
  }, [session, loadingSession, isHost, isParticipant]);

  return {
    streamClient,
    call,
    chatClient,
    channel,
    isInitializingCall,
  };
};

export default useStreamClient;
