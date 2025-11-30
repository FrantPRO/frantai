import { useState, useEffect } from 'react';
import ChatButton from './ChatButton';
import ChatWindow from './ChatWindow';
import {
  getSessionId,
  setSessionId,
  clearSession,
} from '../../utils/session';
import { chatAPI } from '../../api/client';

function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionIdState] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const existingSessionId = getSessionId();
    if (existingSessionId) {
      setSessionIdState(existingSessionId);
    }
  }, []);

  // Add initial greeting message when chat opens for the first time
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const greetingMessage = {
        role: 'assistant',
        content: "Hi! I'm here to help answer any questions you have about Stan Frant. What would you like to know?",
        timestamp: new Date().toISOString(),
      };
      setMessages([greetingMessage]);
    }
  }, [isOpen]);

  const handleToggle = () => {
    setIsOpen(!isOpen);
  };

  const handleNewChat = async () => {
    clearSession();
    setMessages([]);
    setSessionIdState(null);
    try {
      const response = await chatAPI.createSession();
      const newSessionId = response.data.session_id;
      setSessionId(newSessionId);
      setSessionIdState(newSessionId);
    } catch (error) {
      console.error('Failed to create new session:', error);
    }
  };

  const handleSendMessage = async (messageText) => {
    if (!messageText.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: messageText,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    const assistantMessage = {
      role: 'assistant',
      content: '',
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, assistantMessage]);

    try {
      const stream = chatAPI.sendMessage(messageText, sessionId);

      for await (const data of stream) {
        if (data.session_id && !sessionId) {
          setSessionId(data.session_id);
          setSessionIdState(data.session_id);
        }

        if (data.token) {
          setMessages((prev) => {
            const newMessages = [...prev];
            const lastIndex = newMessages.length - 1;
            newMessages[lastIndex] = {
              ...newMessages[lastIndex],
              content: newMessages[lastIndex].content + data.token,
            };
            return newMessages;
          });
        }

        if (data.done) {
          setIsLoading(false);
          // Save response time to the last message
          if (data.response_time_ms) {
            setMessages((prev) => {
              const newMessages = [...prev];
              const lastIndex = newMessages.length - 1;
              newMessages[lastIndex] = {
                ...newMessages[lastIndex],
                response_time_ms: data.response_time_ms,
              };
              return newMessages;
            });
          }
        }
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages((prev) => {
        const newMessages = [...prev];
        const lastIndex = newMessages.length - 1;
        newMessages[lastIndex] = {
          ...newMessages[lastIndex],
          content: 'Error: Failed to get response. Please try again.',
          error: true,
        };
        return newMessages;
      });
      setIsLoading(false);
    }
  };

  return (
    <>
      <ChatButton onClick={handleToggle} isOpen={isOpen} />
      {isOpen && (
        <ChatWindow
          messages={messages}
          onSendMessage={handleSendMessage}
          onClose={handleToggle}
          onNewChat={handleNewChat}
          isLoading={isLoading}
        />
      )}
    </>
  );
}

export default ChatWidget;
