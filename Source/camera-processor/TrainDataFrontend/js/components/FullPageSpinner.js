import React from 'react';
import CircularProgress from 'material-ui/CircularProgress';

export default (props) => (
    <div style={{
        display: 'flex',
        paddingTop: 64,
        flexDirection: 'column',
        justifyContent: 'flex-start',
        alignItems: 'center'
    }}>
        <CircularProgress size={80} thickness={5}/>
    </div>
);