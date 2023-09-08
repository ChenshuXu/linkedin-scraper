import React, { useState, useEffect } from "react";
import axios from "axios";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import TextHighlighter from "./TextHighlighter";

interface JobPost {
    id: number
    url: string
    title: string
    description: string
    company_name: string
    location: string
    timestamp: number
    status: string
    keywords: string
    search_location: string
}

export default function BasicTable(): React.JSX.Element {
    const [data, setData] = useState<JobPost[]>([]);

    useEffect(() => {
        // Fetch data from the FastAPI server
        axios.get<JobPost[]>("http://192.168.1.79:8000/job_post_all/?skip=0&limit=100")
            .then((response) => {
                setData(response.data);
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
            });
    }, []);


    return (
        <div>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>title</TableCell>
                            <TableCell>company</TableCell>
                            <TableCell align="left">description</TableCell>
                            <TableCell>location</TableCell>
                            <TableCell>link</TableCell>
                            <TableCell>time</TableCell>
                            <TableCell>status</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {data.map((row) => (
                            <TableRow
                                key={row.id}
                                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                <TableCell component="th" scope="row">
                                    {row.title}
                                </TableCell>
                                <TableCell>{row.company_name}</TableCell>
                                <TableCell align="left">
                                    <TextHighlighter text={row.description} />
                                </TableCell>
                                <TableCell>
                                    <Typography variant="body2" gutterBottom>
                                        {row.location}
                                    </Typography>
                                </TableCell>
                                <TableCell>
                                    <Button variant="contained" href={row.url} target="_blank" rel="noopener">
                                        Go
                                    </Button>
                                </TableCell>
                                <TableCell>
                                    <Typography variant="body2" gutterBottom>
                                        {new Date(row.timestamp * 1000).toLocaleString()}
                                    </Typography>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    );
}