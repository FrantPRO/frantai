import {Paper, Typography, List, ListItem} from "@mui/material";
import Assignment from "@mui/icons-material/Assignment";
import WorkspacePremiumIcon from "@mui/icons-material/WorkspacePremium";

export default function ListBlocks({projects = [], certificates = []}) {
    return (
        <>
            {projects.length > 0 && (
                <Paper elevation={2} sx={{p: 3, mb: 3, borderRadius: 2}}>
                    <Typography variant="h5" gutterBottom sx={{
                        display: "flex",
                        alignItems: "center",
                        mb: 2
                    }}>
                        <Assignment sx={{mr: 1, color: "primary.main"}}/>
                        Projects
                    </Typography>
                    <List>
                        {projects.map((project, idx) => (
                            <ListItem key={idx} sx={{px: 0, py: 1}}>
                                <Typography variant="body1" sx={{
                                    "&::before": {
                                        content: '"▸ "',
                                        color: "primary.main",
                                        fontWeight: "bold"
                                    }
                                }}>
                                    {project}
                                </Typography>
                            </ListItem>
                        ))}
                    </List>
                </Paper>
            )}

            {certificates.length > 0 && (
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
                        {certificates.map((certificate, idx) => (
                            <ListItem key={idx} sx={{px: 0, py: 1}}>
                                <Typography variant="body1" sx={{
                                    "&::before": {
                                        content: '"▸ "',
                                        color: "primary.main",
                                        fontWeight: "bold"
                                    }
                                }}>
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
        </>
    );
}
