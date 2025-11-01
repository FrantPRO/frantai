import {useState} from "react";
import {
    Paper,
    Typography,
    Card,
    CardContent,
    Box,
    IconButton,
    Collapse,
    List
} from "@mui/material";
import Work from "@mui/icons-material/Work";
import LocationOn from "@mui/icons-material/LocationOn";
import ExpandMore from "@mui/icons-material/ExpandMore";
import DetailItem from "./DetailItem";

export default function WorkExperience({experience = []}) {
    const [expandedIndex, setExpandedIndex] = useState(null);
    const toggle = (idx) => setExpandedIndex((p) => (p === idx ? null : idx));

    return (
        <Paper elevation={2} sx={{p: 3, mb: 4, borderRadius: 2}}>
            <Typography variant="h5" gutterBottom
                        sx={{display: "flex", alignItems: "center", mb: 3}}>
                <Work sx={{mr: 1, color: "primary.main"}}/>
                Work Experience
            </Typography>

            {experience.map((job, index) => (
                <Card
                    key={index}
                    variant="outlined"
                    sx={{
                        mb: 3,
                        "&:last-child": {mb: 0},
                        borderLeft: "4px solid",
                        borderLeftColor: "primary.main",
                        "&:hover": {
                            boxShadow: 3,
                            transform: "translateY(-2px)"
                        },
                        transition: "all 0.3s ease"
                    }}
                >
                    <CardContent sx={{p: 2.5}}>
                        <Box
                            onClick={() => toggle(index)}
                            role="button"
                            aria-expanded={expandedIndex === index}
                            sx={{
                                display: "flex",
                                alignItems: {xs: "flex-start", sm: "center"},
                                justifyContent: "space-between",
                                gap: 2,
                                cursor: "pointer",
                                userSelect: "none"
                            }}
                        >
                            <Box sx={{flex: 1, minWidth: 0}}>
                                <Typography variant="h6" fontWeight="bold"
                                            color="primary.main" sx={{mb: 0.5}}>
                                    {job.position}
                                </Typography>
                                <Box sx={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    flexDirection: {xs: "column", sm: "row"},
                                    gap: {xs: 0.5, sm: 1}
                                }}>
                                    <Typography variant="subtitle1"
                                                color="text.secondary" sx={{
                                        display: "flex",
                                        alignItems: "center"
                                    }}>
                                        <LocationOn fontSize="small"
                                                    sx={{mr: 0.5}}/>
                                        {job.company}
                                    </Typography>
                                    <Typography variant="subtitle1"
                                                sx={{fontWeight: "bold"}}>
                                        {job.period}
                                    </Typography>
                                </Box>
                            </Box>
                            <IconButton
                                aria-label="expand"
                                onClick={(e) => {
                                    e.stopPropagation();
                                    toggle(index);
                                }}
                                sx={{
                                    transform: expandedIndex === index ? "rotate(180deg)" : "rotate(0deg)",
                                    transition: "transform 0.2s ease"
                                }}
                            >
                                <ExpandMore/>
                            </IconButton>
                        </Box>

                        <Collapse in={expandedIndex === index} timeout="auto"
                                  unmountOnExit>
                            <List dense sx={{mt: 1}}>
                                {job.details?.map((point, idx) => (
                                    <DetailItem key={idx} point={point}/>
                                ))}
                            </List>
                            {job.tech_stack && (
                                <Box sx={{
                                    mt: 2,
                                    p: 2,
                                    bgcolor: "grey.50",
                                    borderRadius: 1
                                }}>
                                    <Typography variant="caption"
                                                color="primary.main"
                                                fontWeight="bold"
                                                display="block">
                                        Tech Stack:
                                    </Typography>
                                    <Typography variant="body1" sx={{mt: 0.5}}>
                                        {job.tech_stack}
                                    </Typography>
                                </Box>
                            )}
                        </Collapse>
                    </CardContent>
                </Card>
            ))}
        </Paper>
    );
}
