import { Box } from '@mui/material';
import ProfileDisplay from '../components/Profile/ProfileDisplay';

function Home({ profile }) {
  return (
    <Box component="main" sx={{ minHeight: 'calc(100vh - 200px)', py: 4 }}>
      <ProfileDisplay profile={profile} />
    </Box>
  );
}

export default Home;
