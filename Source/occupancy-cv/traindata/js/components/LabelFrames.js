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
            <div style={{textAlign: 'center'}}>
                <div>
                    <img src="static/img.png" style={{width: '100%'}} className='paper-image'/>
                </div>
                <p style={{marginTop: 48}}>
                    How many people are on this picture?
                </p>
                <div>
                    <TextField
                        id='countField'
                        ref='countField'
                        style={{maxWidth: 180}}
                        value={this.state.value}
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
        );
    }
}