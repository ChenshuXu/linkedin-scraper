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
import {fetchJobPosts, fetchJobPostsFiltered} from "../api/apiServices";
import {JobPost} from "../api/schema";
import {Box, TableFooter, TablePagination, useTheme} from "@mui/material";
import IconButton from "@mui/material/IconButton";
import {KeyboardArrowLeft, KeyboardArrowRight} from "@mui/icons-material";
import FirstPageIcon from '@mui/icons-material/FirstPage';
import LastPageIcon from '@mui/icons-material/LastPage';


interface TablePaginationActionsProps {
    count: number,
    page: number;
    rowsPerPage: number;
    onPageChange: (
        event: React.MouseEvent<HTMLButtonElement>,
        newPage: number,
    ) => void;
}

function TablePaginationActions(props: TablePaginationActionsProps) {
    const theme = useTheme();
    const { count, page, rowsPerPage, onPageChange } = props;

    const handleFirstPageButtonClick = (
        event: React.MouseEvent<HTMLButtonElement>,
    ) => {
        onPageChange(event, 0);
    };

    const handleBackButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        onPageChange(event, page - 1);
    };

    const handleNextButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        onPageChange(event, page + 1);
    };

    return (
        <Box sx={{ flexShrink: 0, ml: 2.5 }}>
            <IconButton
                onClick={handleFirstPageButtonClick}
                disabled={page === 0}
                aria-label="first page"
            >
                {theme.direction === 'rtl' ? <LastPageIcon /> : <FirstPageIcon />}
            </IconButton>
            <IconButton
                onClick={handleBackButtonClick}
                disabled={page === 0}
                aria-label="previous page"
            >
                {theme.direction === 'rtl' ? <KeyboardArrowRight /> : <KeyboardArrowLeft />}
            </IconButton>
            <IconButton
                onClick={handleNextButtonClick}
                aria-label="next page"
            >
                {theme.direction === 'rtl' ? <KeyboardArrowLeft /> : <KeyboardArrowRight />}
            </IconButton>
        </Box>
    );
}


export default function DataTable(): React.JSX.Element {
    const [jobPosts, setJobPosts] = useState<JobPost[]>([]);
    const [rowsPerPage, setRowsPerPage] = React.useState(5);
    const [page, setPage] = React.useState(0);

    useEffect(() => {
        fetchJobPostsFiltered(page, rowsPerPage).then((response) => {
            setJobPosts(response);
        })
    }, [page, rowsPerPage]);

    const handleChangePage = (
        event: React.MouseEvent<HTMLButtonElement> | null,
        newPage: number) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (
        event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    ) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    return (
        <div>
            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="custom pagination table">
                    <TableHead>
                        <TableRow>
                            <TableCell>title</TableCell>
                            <TableCell>company</TableCell>
                            <TableCell align="left">description</TableCell>
                            <TableCell>location</TableCell>
                            <TableCell>link</TableCell>
                            <TableCell>time</TableCell>
                            <TableCell></TableCell>
                            <TableCell>status</TableCell>
                            <TableCell>priority</TableCell>
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
                                <TableCell>{row.priority}</TableCell>
                            </TableRow>
                            )
                        })}
                    </TableBody>
                    <TableFooter>
                        <TableRow>
                            <TablePagination
                                rowsPerPageOptions={[5, 10, 25, { label: 'All', value: 100 }]}
                                colSpan={3}
                                count={-1}
                                rowsPerPage={rowsPerPage}
                                page={page}
                                SelectProps={{
                                    inputProps: {
                                        'aria-label': 'rows per page',
                                    },
                                    native: true,
                                }}
                                onPageChange={handleChangePage}
                                onRowsPerPageChange={handleChangeRowsPerPage}
                                ActionsComponent={TablePaginationActions}
                            />
                        </TableRow>
                    </TableFooter>
                </Table>
            </TableContainer>

        </div>
    );
}