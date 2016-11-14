import React from 'react';
import IconButton from 'material-ui/IconButton';
import ContentSend from 'material-ui/svg-icons/content/send';
import TextField from 'material-ui/TextField';
import Snackbar from 'material-ui/Snackbar';
import Paper from 'material-ui/Paper';

const _initialState = {canSubmit: false, valid: true, value: ''};

export default class LabelFrames extends React.Component {

    constructor(props) {
        super(props);
        this.state = _initialState;
    }

    componentDidMount() {
        // TODO
    }

    _parseLabel(text) {
        const newState = {...this.state, canSubmit: false, valid: true, value: text, label: undefined};
        if (text.match(/^\d+$/)) {
            this.setState({...newState, canSubmit: true, label: parseInt(text)});
        } else if (text === '') {
            this.setState(newState);
        } else {
            this.setState({...newState, canSubmit: false, valid: false, label: undefined});
        }
    }

    _submit = () => {
        if (this.state.canSubmit) {
            this.setState({confirmationOpen: true});
        }
    };

    _textFieldValueChange = (e) => {
        this._parseLabel(e.target.value);
    };

    _textFieldKeyPress = (e) => {
        if (e.which == 13 && this.state.canSubmit) {
            this._submit();
        }
    };

    render() {
        return (
            <div style={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
            }}>
                <Paper zDepth={3} style={{
                    height: '75%',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    padding: '25px',
                }}>
                    <img src="static/img.jpg" style={{
                        maxWidth: '100%',
                        maxHeight: '100%',
                        objectFit: 'contain',
                    }}/>
                </Paper>
                <div style={{
                    height: '20%',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                }}>
                    <p>How many people are on this picture?</p>
                    <div>
                        <TextField
                            id='countField'
                            ref='countField'
                            style={{maxWidth: 180}}
                            value={this.state.value}
                            type="tel"
                            onChange={this._textFieldValueChange}
                            onKeyPress={this._textFieldKeyPress}
                            errorText={this.state.valid ? null : 'Please enter a valid number'}
                        />
                        <IconButton
                            style={{verticalAlign: 'top'}}
                            disabled={!this.state.canSubmit}
                            onTouchTap={this._submit}
                        >
                            <ContentSend/>
                        </IconButton>
                    </div>
                </div>
                <Snackbar
                    open={this.state.confirmationOpen}
                    message="Thank you for your cooperation"
                    autoHideDuration={4000}
                    onRequestClose={this.handleRequestClose}
                />
            </div>
        );
    }
}