import { Box, Paper, Typography } from '@mui/material';
import ReactMarkdown from 'react-markdown';

const TypingIndicator = () => {
  const dotStyle = {
    display: 'inline-block',
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    bgcolor: 'text.secondary',
    mx: 0.25,
    animation: 'bounce 1.4s infinite ease-in-out',
  };

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        gap: 0.5,
        '@keyframes bounce': {
          '0%, 80%, 100%': {
            transform: 'translateY(0)',
          },
          '40%': {
            transform: 'translateY(-8px)',
          },
        },
      }}
    >
      <Box
        sx={{
          ...dotStyle,
          animationDelay: '0s',
        }}
      />
      <Box
        sx={{
          ...dotStyle,
          animationDelay: '0.2s',
        }}
      />
      <Box
        sx={{
          ...dotStyle,
          animationDelay: '0.4s',
        }}
      />
    </Box>
  );
};

function ChatMessage({ message, isLast }) {
  const isUser = message.role === 'user';

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        mb: 2,
      }}
    >
      <Paper
        elevation={1}
        sx={{
          p: 1.5,
          maxWidth: '80%',
          bgcolor: isUser ? 'primary.main' : 'background.paper',
          color: isUser ? 'primary.contrastText' : 'text.primary',
          borderRadius: 2,
          ...(message.error && {
            bgcolor: 'error.main',
            color: 'error.contrastText',
          }),
        }}
      >
        {isUser ? (
          <Typography variant="body1">{message.content}</Typography>
        ) : (
          <>
            <Box
              sx={{
                '& p': { m: 0, mb: 1 },
                '& p:last-child': { mb: 0 },
                '& code': {
                  bgcolor: 'action.hover',
                  px: 0.5,
                  py: 0.25,
                  borderRadius: 0.5,
                  fontSize: '0.875em',
                },
                '& pre': {
                  bgcolor: 'action.hover',
                  p: 1,
                  borderRadius: 1,
                  overflowX: 'auto',
                },
                '& ul, & ol': { pl: 2, my: 0.5 },
              }}
            >
              {message.content ? (
                <ReactMarkdown>{message.content}</ReactMarkdown>
              ) : (
                isLast && <TypingIndicator />
              )}
            </Box>
            {message.response_time_ms && (
              <Typography
                variant="caption"
                sx={{
                  display: 'block',
                  mt: 0.5,
                  color: 'text.secondary',
                  fontSize: '0.7rem',
                }}
              >
                {(message.response_time_ms / 1000).toFixed(2)}s
              </Typography>
            )}
          </>
        )}
      </Paper>
    </Box>
  );
}

export default ChatMessage;
