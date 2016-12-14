import React from 'react';
import Paper from 'material-ui/Paper';
import IsAFaceLabeler from './IsAFaceLabeler';
import PeopleCountLabeler from './PeopleCountLabeler';

const _labelerStyle = {paddingTop: 32, flexGrow: 1};

export default class LabelImage extends React.Component {

    constructor(props) {
        super(props);
    }

    _getLabeler() {
        switch (this.props.type) {
            case 'face':
                return (
                    <IsAFaceLabeler
                        style={_labelerStyle}
                        onLabeled={this.props.onLabeled}
                    />
                );
                break;
            case 'count':
                return (
                    <PeopleCountLabeler
                        style={_labelerStyle}
                        onLabeled={this.props.onLabeled}
                    />
                );
                break;
        }
    }

    render() {
        return (
            <div style={{
                height: '100%',
                paddingTop: 32,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-start',
                alignItems: 'center'
            }}>
                <Paper zDepth={3} style={{padding: 15, paddingBottom: 12}}>
                    <img src={this.props.src} style={{
                        maxHeight: 'calc(100vh - 315px)',
                        minHeight: 64,
                        maxWidth: '100%'
                    }}/>
                </Paper>
                {this._getLabeler()}
            </div>
        );
    }
}

LabelImage.propTypes = {
    onLabeled: React.PropTypes.func
};
