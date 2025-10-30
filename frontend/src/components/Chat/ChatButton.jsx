import { Fab } from '@mui/material';
import ChatIcon from '@mui/icons-material/Chat';
import CloseIcon from '@mui/icons-material/Close';

function ChatButton({ onClick, isOpen }) {
  return (
    <Fab
      color="primary"
      aria-label="chat"
      onClick={onClick}
      sx={{
        position: 'fixed',
        bottom: 24,
        right: 24,
        zIndex: 1000,
      }}
    >
      {isOpen ? <CloseIcon /> : <ChatIcon />}
    </Fab>
  );
}

export default ChatButton;
