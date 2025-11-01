import {useState, memo} from "react";
import {Box, ListItem, Typography, Collapse, IconButton} from "@mui/material";
import ExpandMore from "@mui/icons-material/ExpandMore";

function DetailItemImpl({point}) {
    const [open, setOpen] = useState(false);

    return (
        <Box sx={{width: "100%"}}>
            <ListItem
                onClick={() => setOpen((v) => !v)}
                sx={{
                    px: 0,
                    py: 0.75,
                    cursor: "pointer",
                    userSelect: "none",
                    borderRadius: 1,
                    "&:hover": {bgcolor: "grey.50"},
                    display: "flex",
                    alignItems: "center",
                    gap: 1
                }}
            >
                {/* Синяя стрелка слева */}
                <IconButton
                    size="small"
                    sx={{
                        color: "primary.main",
                        transform: open ? "rotate(0deg)" : "rotate(-90deg)",
                        transition: "transform 0.2s ease"
                    }}
                >
                    <ExpandMore fontSize="small"/>
                </IconButton>

                {/* Заголовок */}
                <Typography
                    variant="body1"
                    sx={{
                        flex: 1,
                        fontWeight: 500
                    }}
                >
                    {point.title}
                </Typography>
            </ListItem>

            {/* Описание (разворачивается вниз) */}
            <Collapse in={open} timeout="auto" unmountOnExit>
                <Box sx={{pl: 5, pr: 1, pb: 1}}>
                    <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{whiteSpace: "pre-line"}}
                    >
                        {point.description}
                    </Typography>
                </Box>
            </Collapse>
        </Box>
    );
}

const DetailItem = memo(DetailItemImpl, (prev, next) => prev.point === next.point);
export default DetailItem;
