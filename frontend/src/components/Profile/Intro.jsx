import {useEffect, useState, Suspense, lazy} from "react";
import {
    Container,
    Typography,
    Stack,
    Link,
    Box,
    List,
    ListItem,
    Paper,
    Avatar
} from "@mui/material";
import LinkedIn from "@mui/icons-material/LinkedIn";
import GitHub from "@mui/icons-material/GitHub";
import Telegram from "@mui/icons-material/Telegram";
import Email from "@mui/icons-material/Email";
import LocationOn from "@mui/icons-material/LocationOn";
import School from "@mui/icons-material/School";
import Code from "@mui/icons-material/Code";
import Language from "@mui/icons-material/Language";
import Assignment from "@mui/icons-material/Assignment";
import WorkspacePremiumIcon from "@mui/icons-material/WorkspacePremium";

const WorkExperience = lazy(() => import("./WorkExperience.jsx"));

const apiUrl = import.meta.env.VITE_API_URL;

const iconMap = {
    GitHub: <GitHub fontSize="small"/>,
    LinkedIn: <LinkedIn fontSize="small"/>,
    Telegram: <Telegram fontSize="small"/>,
    Email: <Email fontSize="small"/>
};

// Transform new API format to old format
const transformProfileData = (apiData) => {
    const basics = apiData.basics || {};

    // Build contacts array from basics
    const contacts = [];
    if (basics.linkedin_url) contacts.push({ type: 'LinkedIn', url: basics.linkedin_url });
    if (basics.github_url) contacts.push({ type: 'GitHub', url: basics.github_url });
    if (basics.email) contacts.push({ type: 'Email', url: `mailto:${basics.email}` });

    // Transform education (take first from array)
    const education = apiData.education && apiData.education[0] ? {
        field: apiData.education[0].field_of_study,
        degree: apiData.education[0].degree_type,
        university: apiData.education[0].institution_name,
        location: apiData.education[0].location,
        specialization: apiData.education[0].field_of_study,
        period: `${apiData.education[0].start_year} - ${apiData.education[0].end_year || 'Present'}`
    } : null;

    // Transform skills to technologies_and_tools
    const technologies_and_tools = apiData.skills?.map(skill => skill.skill_name) || [];

    // Transform experience
    const experience = apiData.experience?.map(exp => ({
        position: exp.position,
        company: exp.company_name,
        period: `${exp.start_date}${exp.is_current ? ' - Present' : ` - ${exp.end_date}`}`,
        details: exp.achievements?.map(ach => ({ title: ach, description: '' })) || [],
        tech_stack: exp.technologies?.join(', ') || ''
    })) || [];

    // Transform certifications to certificates
    const certificates = apiData.certifications?.map(cert => ({
        name: cert.certification_name,
        link: cert.credential_url ? `<a href="${cert.credential_url}" target="_blank" rel="noopener noreferrer">(view)</a>` : ''
    })) || [];

    return {
        work_name: basics.full_name,
        legal_name: basics.full_name,
        aboutme: basics.bio || basics.summary,
        contacts,
        experience,
        education,
        technologies_and_tools,
        languages: apiData.languages?.map(lang => `${lang.language_name} (${lang.proficiency_level})`) || [],
        projects: apiData.projects?.map(proj => proj.project_name) || [],
        certificates
    };
};

export default function Intro() {
    const [data, setData] = useState(null);

    useEffect(() => {
        fetch(`${apiUrl}/profile`)
            .then((res) => res.json())
            .then((apiData) => {
                const transformed = transformProfileData(apiData);
                setData(transformed);
            })
            .catch((err) => {
                console.error("Failed to fetch resume data", err);
            });
    }, []);

    if (!data) return (
        <Container sx={{mt: 8, textAlign: "center"}}>
            <Typography variant="h6">Loading...</Typography>
        </Container>
    );

    return (
        <Container maxWidth="lg" sx={{py: 4}}>
            {/* Header Section */}
            <Paper
                elevation={2}
                sx={{
                    position: "relative",
                    p: 4,
                    mb: 4,
                    backgroundColor: "white",
                    borderRadius: 3,
                    border: "1px solid #e0e0e0"
                }}
            >
                <Link
                    href="/Stan_Frant_CV.pdf"
                    download
                    target="_blank"
                    rel="noopener noreferrer"
                    sx={{
                        position: "absolute",
                        top: 16,
                        right: 16,
                        fontWeight: "bold",
                        color: "text.primary",
                        border: "1px solid",
                        borderColor: "primary.main",
                        borderRadius: 1,
                        px: 1.5,
                        py: 0.5,
                        textDecoration: "none",
                        fontSize: "0.875rem",
                        transition: "0.2s ease",
                        "&:hover": {
                            bgcolor: "primary.main",
                            color: "white"
                        }
                    }}
                >
                    Download CV
                </Link>
                <Stack direction="row" spacing={2} alignItems="center"
                       sx={{mb: 2}}>
                    <Avatar
                        alt="Stan Frant"
                        src="/avatar.jpg"
                        sx={{width: 72, height: 72}}
                        slotProps={{
                            img: {
                                loading: "lazy",
                                decoding: "async",
                            }
                        }}
                    />
                    <Box>
                        <Typography variant="h3" fontWeight="bold"
                                    color="primary.main">
                            {data.work_name}
                        </Typography>
                        <Typography variant="subtitle2" color="text.secondary">
                            Legal name: {data.legal_name}
                        </Typography>
                    </Box>
                </Stack>
                <Typography variant="body1"
                            sx={{
                                lineHeight: 1.7,
                                color: "text.secondary",
                                textAlign: "justify"
                            }}>
                    {data.aboutme}
                </Typography>
            </Paper>

            {/* Contact Information */}
            <Paper elevation={2} sx={{p: 3, mb: 4, borderRadius: 2}}>
                <Typography variant="h5" gutterBottom
                            sx={{display: "flex", alignItems: "center", mb: 2}}>
                    <Email sx={{mr: 1, color: "primary.main"}}/>
                    Contact Information
                </Typography>
                <Stack direction="row" spacing={3} flexWrap="wrap" useFlexGap>
                    {data.contacts?.map(({type, url}) => (
                        <Link
                            key={type}
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                            color="inherit"
                            underline="hover"
                            sx={{
                                p: 1,
                                borderRadius: 1,
                                "&:hover": {
                                    bgcolor: "primary.main",
                                    color: "white"
                                },
                                transition: "all 0.3s ease"
                            }}
                        >
                            <Stack direction="row" alignItems="center"
                                   spacing={1}>
                                {iconMap[type]}
                                <Typography variant="body1">{type}</Typography>
                            </Stack>
                        </Link>
                    ))}
                </Stack>
            </Paper>

            {/* Work Experience */}
            <Suspense fallback={<Paper elevation={0} sx={{p: 3, mb: 4}}>
                Loading experience…</Paper>}>
                <WorkExperience experience={data.experience}/>
            </Suspense>

            {/* Education */}
            <Paper elevation={2} sx={{p: 3, mb: 3, borderRadius: 2}}>
                <Typography variant="h5" gutterBottom sx={{
                    display: "flex",
                    alignItems: "center",
                    mb: 2
                }}>
                    <School sx={{mr: 1, color: "primary.main"}}/>
                    Education
                </Typography>
                {data.education && (
                    <Box>
                        <Typography variant="h6" fontWeight="bold"
                                    gutterBottom>
                            {data.education.field}
                        </Typography>
                        <Typography variant="subtitle1"
                                    color="primary.main" gutterBottom>
                            {data.education.degree}
                        </Typography>
                        <Typography variant="body1"
                                    color="text.secondary" gutterBottom>
                            {data.education.university}
                        </Typography>
                        <Typography variant="body1"
                                    color="text.secondary" gutterBottom
                                    sx={{
                                        display: "flex",
                                        alignItems: "center"
                                    }}>
                            <LocationOn fontSize="small"
                                        sx={{mr: 0.5}}/>
                            {data.education.location}
                        </Typography>
                        <Typography variant="body1" gutterBottom>
                            <strong>Specialization:</strong> {data.education.specialization}
                        </Typography>
                        <Typography variant="body1"
                                    color="text.secondary">
                            {data.education.period}
                        </Typography>
                    </Box>
                )}
            </Paper>

            {/* Technologies and Tools */}
            {data.technologies_and_tools && data.technologies_and_tools.length > 0 && (
                <Paper elevation={2}
                       sx={{p: 3, mb: 3, borderRadius: 2}}>
                    <Typography variant="h5" gutterBottom sx={{
                        display: "flex",
                        alignItems: "center",
                        mb: 2
                    }}>
                        <Code sx={{mr: 1, color: "primary.main"}}/>
                        Technologies & Tools
                    </Typography>
                    <List dense>
                        {data.technologies_and_tools.map((item, idx) => (
                            <ListItem key={idx} sx={{px: 0, py: 0.5}}>
                                <Typography
                                    variant="body1"
                                    sx={{
                                        "&::before": {
                                            content: '"▸ "',
                                            color: "primary.main",
                                            fontWeight: "bold"
                                        }
                                    }}
                                >
                                    {item}
                                </Typography>
                            </ListItem>
                        ))}
                    </List>
                </Paper>
            )}

            {/* Languages */}
            {data.languages && data.languages.length > 0 && (
                <Paper elevation={2} sx={{p: 3, mb: 3, borderRadius: 2}}>
                    <Typography variant="h5" gutterBottom sx={{
                        display: "flex",
                        alignItems: "center",
                        mb: 2
                    }}>
                        <Language sx={{mr: 1, color: "primary.main"}}/>
                        Languages
                    </Typography>
                    <List>
                        {data.languages.map((lang, idx) => (
                            <ListItem key={idx} sx={{px: 0, py: 1}}>
                                <Typography
                                    variant="body1"
                                    sx={{
                                        "&::before": {
                                            content: '"▸ "',
                                            color: "primary.main",
                                            fontWeight: "bold"
                                        }
                                    }}
                                >
                                    {lang}
                                </Typography>
                            </ListItem>
                        ))}
                    </List>
                </Paper>
            )}

            {/* Projects */}
            {data.projects && data.projects.length > 0 && (
                <Paper elevation={2} sx={{p: 3, mb: 3, borderRadius: 2}}>
                    <Typography variant="h5" gutterBottom sx={{
                        display: "flex",
                        alignItems: "center",
                        mb: 2
                    }}>
                        <Assignment
                            sx={{mr: 1, color: "primary.main"}}/>
                        Projects
                    </Typography>
                    <List>
                        {data.projects.map((project, idx) => (
                            <ListItem key={idx} sx={{px: 0, py: 1}}>
                                <Typography
                                    variant="body1"
                                    sx={{
                                        "&::before": {
                                            content: '"▸ "',
                                            color: "primary.main",
                                            fontWeight: "bold"
                                        }
                                    }}
                                >
                                    {project}
                                </Typography>
                            </ListItem>
                        ))}
                    </List>
                </Paper>
            )}

            {/* Certificates */}
            {data.certificates && data.certificates.length > 0 && (
                <Paper elevation={2} sx={{p: 3, borderRadius: 2}}>
                    <Typography variant="h5" gutterBottom sx={{
                        display: "flex",
                        alignItems: "center",
                        mb: 2
                    }}>
                        <WorkspacePremiumIcon
                            sx={{mr: 1, color: "primary.main"}}/>
                        Certificates
                    </Typography>
                    <List>
                        {data.certificates.map((certificate, idx) => (
                            <ListItem key={idx} sx={{px: 0, py: 1}}>
                                <Typography
                                    variant="body1"
                                    sx={{
                                        "&::before": {
                                            content: '"▸ "',
                                            color: "primary.main",
                                            fontWeight: "bold"
                                        }
                                    }}
                                >
                                    {certificate.link ? (
                                        <span
                                            dangerouslySetInnerHTML={{__html: `${certificate.name} ${certificate.link}`}}/>
                                    ) : (
                                        certificate.name
                                    )}
                                </Typography>
                            </ListItem>
                        ))}
                    </List>
                </Paper>
            )}
        </Container>
    );
}
