import React, { useState, useEffect } from "react";
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
import Status from "./Status";
import {fetchJobPosts} from "../api/apiServices";
import {JobPost} from "../api/schema";


export default function BasicTable(): React.JSX.Element {
    const [jobPosts, setJobPosts] = useState<JobPost[]>([]);

    useEffect(() => {
        fetchJobPosts().then((response) => {
            setJobPosts(response);
        })
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
                        {jobPosts.map((row, index) => {

                            return (
                            <TableRow
                                key={index}
                                style={ row.status==="deleted" ? {backgroundColor:"grey"} : {} }
                                sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                                <TableCell component="th" scope="row">
                                    {row.title}
                                </TableCell>
                                <TableCell>{row.company_name}</TableCell>
                                <TableCell align="left">
                                    <Typography variant="body2" gutterBottom>
                                        <TextHighlighter text={row.description} />
                                    </Typography>
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
                                <TableCell>
                                    <Status status={row.status} id={row.id} index={index} jobPosts={jobPosts} setJobPosts={setJobPosts}/>
                                </TableCell>
                                <TableCell>{row.status}</TableCell>
                            </TableRow>
                            )
                        })}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    );
}