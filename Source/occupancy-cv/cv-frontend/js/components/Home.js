import React from 'react';
import {withRouter} from 'react-router';
import RaisedButton from 'material-ui/RaisedButton';

const _buttonStyle = {
    margin: 12
};

class Home extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div style={{textAlign: 'center'}}>
                <h1>Welcome</h1>
                <p>
                    Select below which task do you want to perform or select additional options from the menu
                </p>
                <div>
                    <RaisedButton
                        label='Label Rectangles'
                        primary={true}
                        style={_buttonStyle}
                        onTouchTap={() => this.props.router.push('/label-rects')}
                    />
                    <RaisedButton
                        label='Label Frames'
                        secondary={true}
                        style={_buttonStyle}
                        onTouchTap={() => this.props.router.push('/label-frames')}
                    />
                </div>
            </div>
        );
    }
}

export default withRouter(Home);