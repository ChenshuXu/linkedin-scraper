import React from 'react';

interface Props {
    text: string;
}

const TextHighlighter: React.FC<Props> = ({text}) => {
    let splitText = text.split(' ').map((word, index) => (
        <span key={index} style={word.match(/year/ig) ? { background: 'yellow' } : {} }>
            {word}{' '}
        </span>
    ));

    return (<React.Fragment>{splitText}</React.Fragment>);
}

export default TextHighlighter;