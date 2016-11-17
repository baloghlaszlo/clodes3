import React from 'react';
import IconButton from 'material-ui/IconButton';
import SendIcon from 'material-ui/svg-icons/content/send';
import IncrementIcon from 'material-ui/svg-icons/hardware/keyboard-arrow-up';
import DecrementIcon from 'material-ui/svg-icons/hardware/keyboard-arrow-down';
import TextField from 'material-ui/TextField';

const _emptyLabelState = {canSubmit: false, showValidationError: false, value: '', label: 0};
const _validLabelState = {..._emptyLabelState, canSubmit: true};
const _invalidLabelState = {..._emptyLabelState, showValidationError: true};

export default class PeopleCountLabeler extends React.Component {

    constructor(props) {
        super(props);
        this.state = _emptyLabelState;
    }

    _parseLabel(text) {
        if (text.match(/^\d+$/)) {
            this.setState({..._validLabelState, value: text, label: parseInt(text)});
        } else if (text === '') {
            this.setState(_emptyLabelState);
        } else {
            this.setState({..._invalidLabelState, value: text});
        }
    }

    _add(increment) {
        let nextLabel = Math.max(0, (this.state.label || 0) + increment);
        this.setState({..._validLabelState, value: nextLabel.toString(), label: nextLabel});
    }

    _submit = () => {
        if (this.state.canSubmit) {
            if (this.props.onLabeled) {
                this.props.onLabeled(this.state.label);
            }
            this.setState(_emptyLabelState);
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
            <div style={this.props.style || {}}>
                <div style={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'flex-start',
                    alignItems: 'center'
                }}>
                    <p>How many people are on this picture?</p>
                    <div>
                        <TextField
                            id='countField'
                            ref='countField'
                            style={{maxWidth: 150}}
                            value={this.state.value}
                            type="tel"
                            onChange={this._textFieldValueChange}
                            onKeyPress={this._textFieldKeyPress}
                            errorText={this.state.showValidationError ? 'Please enter a valid number' : null}
                        />
                        <IconButton
                            style={{verticalAlign: 'top'}}
                            onTouchTap={() => this._add(1)}
                        >
                            <IncrementIcon/>
                        </IconButton>
                        <IconButton
                            style={{verticalAlign: 'top'}}
                            disabled={this.state.canSubmit && this.state.label <= 0}
                            onTouchTap={() => this._add(-1)}
                        >
                            <DecrementIcon/>
                        </IconButton>
                        <IconButton
                            style={{verticalAlign: 'top'}}
                            disabled={!this.state.canSubmit}
                            onTouchTap={this._submit}
                        >
                            <SendIcon/>
                        </IconButton>
                    </div>
                </div>
            </div>
        );
    }
}

PeopleCountLabeler.propTypes = {
    onLabeled: React.PropTypes.func
};