import {
  Box,
  Container,
  Typography,
  Paper,
  Chip,
  Grid,
  Card,
  CardContent,
} from '@mui/material';
import WorkIcon from '@mui/icons-material/Work';
import CodeIcon from '@mui/icons-material/Code';
import SchoolIcon from '@mui/icons-material/School';
import EmailIcon from '@mui/icons-material/Email';
import GitHubIcon from '@mui/icons-material/GitHub';
import TelegramIcon from '@mui/icons-material/Telegram';

function ProfileDisplay({ profile }) {
  if (!profile) return null;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ mb: 6, textAlign: 'center' }}>
        <Typography variant="h1" gutterBottom>
          {profile.name}
        </Typography>
        <Typography variant="h4" color="text.secondary" gutterBottom>
          {profile.title}
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, maxWidth: 800, mx: 'auto' }}>
          {profile.bio}
        </Typography>
      </Box>

      {profile.skills && profile.skills.length > 0 && (
        <Paper sx={{ p: 4, mb: 4 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <CodeIcon sx={{ mr: 1 }} />
            <Typography variant="h3">Skills</Typography>
          </Box>
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {profile.skills.map((skill, index) => (
              <Chip key={index} label={skill} color="primary" />
            ))}
          </Box>
        </Paper>
      )}

      {profile.experience && profile.experience.length > 0 && (
        <Paper sx={{ p: 4, mb: 4 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <WorkIcon sx={{ mr: 1 }} />
            <Typography variant="h3">Experience</Typography>
          </Box>
          <Grid container spacing={3}>
            {profile.experience.map((exp, index) => (
              <Grid item xs={12} key={index}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h5" gutterBottom>
                      {exp.position}
                    </Typography>
                    <Typography color="text.secondary" gutterBottom>
                      {exp.company} • {exp.period}
                    </Typography>
                    <Typography variant="body2">{exp.description}</Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Paper>
      )}

      {profile.education && profile.education.length > 0 && (
        <Paper sx={{ p: 4, mb: 4 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <SchoolIcon sx={{ mr: 1 }} />
            <Typography variant="h3">Education</Typography>
          </Box>
          <Grid container spacing={3}>
            {profile.education.map((edu, index) => (
              <Grid item xs={12} key={index}>
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h5" gutterBottom>
                      {edu.degree}
                    </Typography>
                    <Typography color="text.secondary" gutterBottom>
                      {edu.institution} • {edu.period}
                    </Typography>
                    {edu.description && (
                      <Typography variant="body2">{edu.description}</Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Paper>
      )}

      {(profile.email || profile.github || profile.telegram) && (
        <Paper sx={{ p: 4 }}>
          <Typography variant="h3" gutterBottom>
            Contact
          </Typography>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {profile.email && (
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <EmailIcon sx={{ mr: 1 }} />
                <Typography variant="body1">{profile.email}</Typography>
              </Box>
            )}
            {profile.github && (
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <GitHubIcon sx={{ mr: 1 }} />
                <Typography
                  variant="body1"
                  component="a"
                  href={`https://github.com/${profile.github}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  sx={{ textDecoration: 'none', color: 'inherit' }}
                >
                  {profile.github}
                </Typography>
              </Box>
            )}
            {profile.telegram && (
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <TelegramIcon sx={{ mr: 1 }} />
                <Typography
                  variant="body1"
                  component="a"
                  href={`https://t.me/${profile.telegram}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  sx={{ textDecoration: 'none', color: 'inherit' }}
                >
                  @{profile.telegram}
                </Typography>
              </Box>
            )}
          </Box>
        </Paper>
      )}
    </Container>
  );
}

export default ProfileDisplay;
