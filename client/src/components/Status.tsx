import React from 'react';
import DeleteIcon from "@mui/icons-material/Delete";
import RestoreFromTrashIcon from '@mui/icons-material/RestoreFromTrash';
import IconButton from "@mui/material/IconButton";
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import {JobPost} from "../api/schema";
import {updateJobPost} from "../api/apiServices";

interface Props {
    status: string,
    id: number,
    index: number,
    jobPosts: JobPost[],
    setJobPosts: Function
}

const Status: React.FC<Props> = (props: Props) => {
    const applied = props.status === "applied";
    const deleted = props.status === "deleted";

    const handleApplyClick = () => {
        if (!applied) {
            updateJobPost(props.id, "applied")
                .then((response) => {
                    updateRows(response);
                });
        } else {
            updateJobPost(props.id, "success")
                .then((response) => {
                    updateRows(response);
                });
        }
    }

    const handleDeleteClick = () => {
        if (!deleted) {
            updateJobPost(props.id, "deleted")
                .then((response) => {
                    updateRows(response);
                });
        } else {
            if (applied) {
                updateJobPost(props.id, "applied")
                    .then((response) => {
                        updateRows(response);
                    });
            } else {
                updateJobPost(props.id, "success")
                    .then((response) => {
                        updateRows(response);
                    });
            }
        }
    }

    const updateRows = (newRow: JobPost) => {
        const newPosts = [...props.jobPosts];
        newPosts[props.index] = newRow;
        props.setJobPosts(newPosts);
    }

    return (
        <>
            <IconButton onClick={handleApplyClick}>
                { applied ? <CheckCircleIcon /> : <RadioButtonUncheckedIcon /> }
            </IconButton>
            <IconButton onClick={handleDeleteClick}>
                { deleted ? <RestoreFromTrashIcon /> : <DeleteIcon /> }
            </IconButton>
        </>
    );
}

export default Status;