import React from 'react';
import IconButton from 'material-ui/IconButton';
import ContentSend from 'material-ui/svg-icons/content/send';
import TextField from 'material-ui/TextField';

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
            alert(this.state.label);
            this.setState(_initialState);
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
                justifyContent: 'flex-end',
                alignItems: 'center',
            }}>
                <div style={{
                    display: 'flex',
                    flexGrow: 0,
                    flexShrink: 1,
                    padding: 16,
                    boxSizing: 'border-box'
                }}>
                    <div>
                        <img src="static/img.png" style={{
                            width: '100%',
                            height: '100%',
                            objectFit: 'contain',
                            filter: 'drop-shadow(0px 3px 10px rgba(0,0,0,.39))',
                        }}/>
                    </div>
                </div>
                <div style={{
                    flexShrink: 0,
                    minHeight: '8em',

                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'flex-start',
                    alignItems: 'center',
                }}>
                    <p>
                        How many people are on this picture?
                    </p>
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
                            tooltip='Submit Label'
                            style={{verticalAlign: 'top'}}
                            disabled={!this.state.canSubmit}
                            onTouchTap={this._submit}
                        >
                            <ContentSend/>
                        </IconButton>
                    </div>
                </div>
            </div>
        );
    }
}