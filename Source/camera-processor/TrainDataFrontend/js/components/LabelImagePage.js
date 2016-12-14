import React from 'react';
import {connect} from 'react-redux';
import LabelImage from './LabelImage';
import ImageLoadError from './ImageLoadError';
import FullPageSpinner from './FullPageSpinner';
import {LABEL_SUBMITTED, IMAGE_RELOAD_REQUESTED} from '../constants';

class LabelImagePage extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        if (this.props.image.isValid) {
            if (this.props.image.isError) {
                return (
                    <ImageLoadError
                        message={this.props.image.message}
                        onTryAgain={this.props.onTryAgain}
                    />
                );
            } else {
                return (
                    <LabelImage
                        src={this.props.image.src}
                        type={this.props.image.labels.type}
                        onLabeled={this.props.onLabeled}
                    />
                );
            }
        } else {
            return (
                <FullPageSpinner/>
            );
        }
    }
}

LabelImagePage.propTypes = {
    image: React.PropTypes.object,
    onLabeled: React.PropTypes.func,
    onTryAgain: React.PropTypes.func
};

export default connect(
    state => ({image: state.image}),
    dispatch => ({
        onLabeled: label => dispatch({
            type: LABEL_SUBMITTED,
            payload: label
        }),
        onTryAgain: () => dispatch({
            type: IMAGE_RELOAD_REQUESTED
        })
    })
)(LabelImagePage);