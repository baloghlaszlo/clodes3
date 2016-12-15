import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';

const _buttonStyle = {
    margin: 12
};

export default class IsAFaceLabeler extends React.Component {

    constructor(props) {
        super(props);
    }

    _label(label) {
        if (this.props.onLabeled) {
            this.props.onLabeled(label);
        }
    }

    _handle_key(e) {
        e = e || window.event;

        if (e.keyCode == '37') {
            this._label(1)
        } else if (e.keyCode == '39') {
            this._label(0)
        }
    }

    render() {
        return ( <
            div style = {
                this.props.style
            } >
            <
            div style = {
                {
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'flex-start',
                    alignItems: 'center'

                }
            }
            onkeydown = {
                (e) => this._handle_key(e)
            } >
            <
            p > Is this a face ? < /p> <
            div >
            <
            RaisedButton label = 'Yes'
            primary = {
                true
            }
            style = {
                _buttonStyle
            }
            onTouchTap = {
                () => this._label(1)
            }
            /> <
            RaisedButton label = 'No'
            secondary = {
                true
            }
            style = {
                _buttonStyle
            }
            onTouchTap = {
                () => this._label(0)
            }
            /> <
            /div> <
            /div> <
            /div>
        );
    }
}

IsAFaceLabeler.propTypes = {
    onLabeled: React.PropTypes.func
};
