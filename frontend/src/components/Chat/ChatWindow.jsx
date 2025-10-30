import { useRef, useEffect } from 'react';
import { Box, Paper } from '@mui/material';
import ChatHeader from './ChatHeader';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

function ChatWindow({
  messages,
  onSendMessage,
  onClose,
  onNewChat,
  isLoading,
}) {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <Paper
      elevation={8}
      sx={{
        position: 'fixed',
        bottom: 100,
        right: 24,
        width: 400,
        maxWidth: 'calc(100vw - 48px)',
        height: 600,
        maxHeight: 'calc(100vh - 150px)',
        zIndex: 999,
        display: 'flex',
        flexDirection: 'column',
        borderRadius: 2,
        overflow: 'hidden',
      }}
    >
      <ChatHeader onClose={onClose} onNewChat={onNewChat} />

      <Box
        sx={{
          flex: 1,
          overflowY: 'auto',
          p: 2,
          bgcolor: 'background.default',
        }}
      >
        {messages.length === 0 ? (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: 'text.secondary',
            }}
          >
            Ask me anything about Stan Frant
          </Box>
        ) : (
          messages.map((message, index) => (
            <ChatMessage
              key={index}
              message={message}
              isLast={index === messages.length - 1}
            />
          ))
        )}
        <div ref={messagesEndRef} />
      </Box>

      <ChatInput onSend={onSendMessage} disabled={isLoading} />
    </Paper>
  );
}

export default ChatWindow;
