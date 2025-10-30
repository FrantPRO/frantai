import { useState, useEffect } from 'react';
import { Box, CircularProgress, Container } from '@mui/material';
import Background from './components/Layout/Background';
import Header from './components/Layout/Header';
import Footer from './components/Layout/Footer';
import Home from './pages/Home';
import ChatWidget from './components/Chat/ChatWidget';
import { profileAPI } from './api/client';

function App() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await profileAPI.getProfile();
        setProfile(response.data);
      } catch (err) {
        setError(err.message || 'Failed to load profile');
        console.error('Error fetching profile:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '100vh',
        }}
      >
        <Container>
          <Box sx={{ textAlign: 'center', color: 'error.main' }}>
            Error: {error}
          </Box>
        </Container>
      </Box>
    );
  }

  return (
    <Box sx={{ position: 'relative', minHeight: '100vh' }}>
      <Background />
      <Header profile={profile} />
      <Home profile={profile} />
      <Footer />
      <ChatWidget />
    </Box>
  );
}

export default App;
