import { Box, Typography, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import RefreshIcon from '@mui/icons-material/Refresh';

function ChatHeader({ onClose, onNewChat }) {
  return (
    <Box
      sx={{
        p: 2,
        bgcolor: 'primary.main',
        color: 'primary.contrastText',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}
    >
      <Typography variant="h6">Chat with AI</Typography>
      <Box>
        <IconButton
          size="small"
          onClick={onNewChat}
          sx={{ color: 'primary.contrastText', mr: 1 }}
        >
          <RefreshIcon />
        </IconButton>
        <IconButton
          size="small"
          onClick={onClose}
          sx={{ color: 'primary.contrastText' }}
        >
          <CloseIcon />
        </IconButton>
      </Box>
    </Box>
  );
}

export default ChatHeader;
