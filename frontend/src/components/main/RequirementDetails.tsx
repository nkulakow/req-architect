import Grid from "@mui/material/Grid";
import { useContext } from "react";
import { MainContext } from "../../pages/MainPage.tsx";

export default function RequirementDetails() {
    const contextTools = useContext(MainContext);
    return (
        <Grid
            container
            borderLeft="1px solid green"
            sx={{
                p: 0,
                justifyContent: "center",
                // width: "15%",
                height: "100%",
            }}
        >
            Requirement Details. Reviewed:{" "}
            {contextTools?.data.selectedRequirement?.reviewed}
        </Grid>
    );
}
