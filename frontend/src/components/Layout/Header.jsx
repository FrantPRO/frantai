import { AppBar, Toolbar, Typography, Container } from '@mui/material';

function Header({ profile }) {
  return (
    <AppBar position="static" elevation={0} sx={{ bgcolor: 'transparent' }}>
      <Container maxWidth="lg">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            component="div"
            sx={{ flexGrow: 1, fontWeight: 700 }}
          >
            {profile?.name || 'Stan Frant'}
          </Typography>
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default Header;
