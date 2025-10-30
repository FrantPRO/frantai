import { Box, Paper, Typography } from '@mui/material';
import ReactMarkdown from 'react-markdown';

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
            <ReactMarkdown>
              {message.content || (isLast ? '...' : '')}
            </ReactMarkdown>
          </Box>
        )}
      </Paper>
    </Box>
  );
}

export default ChatMessage;
