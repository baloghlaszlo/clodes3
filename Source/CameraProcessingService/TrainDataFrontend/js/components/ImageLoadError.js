import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';

const ImageLoadError = (props) => (
    <div style={{
        display: 'flex',
        paddingTop: 32,
        flexDirection: 'column',
        justifyContent: 'flex-start',
        alignItems: 'center'
    }}>
        <p>{props.message}</p>
        <RaisedButton
            label='Try Again'
            onTouchTap={props.onTryAgain}
        />
    </div>
);

ImageLoadError.propTypes = {
    message: React.PropTypes.string,
    onTryAgain: React.PropTypes.func
};

export default ImageLoadError;