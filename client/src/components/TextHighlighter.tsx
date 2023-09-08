import React from 'react';
import Typography from "@mui/material/Typography";

interface Props {
    text: string;
}

const TextHighlighter: React.FC<Props> = ({text}) => {
    let splitText: string[] = text.split(' ');

    return (
        <Typography variant="body2" gutterBottom>
            {splitText.map((word: string) => {
                if (word.match(/year/gi)) {
                    return <a style={{background: 'yellow'}}>{word} </a>
                } else {
                    return <a>{word} </a>
                }
            })}
        </Typography>
    );
}

export default TextHighlighter;