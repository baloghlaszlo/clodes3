import {IMAGE_DATA_LOADED, IMAGE_DATA_INVALIDATED, NEW_IMAGE_ENDPOINT_UPDATED} from './constants';

export default {
    nextImageEndpoint: (endpoint = '', action) => {
        switch (action.type) {
            case NEW_IMAGE_ENDPOINT_UPDATED:
                return action.payload;
            default:
                return endpoint;
        }
    },
    image: (image = {isValid: false}, action) => {
        switch (action.type) {
            case IMAGE_DATA_LOADED:
                return {...action.payload, isValid: true};
            case IMAGE_DATA_INVALIDATED:
                return {isValid: false};
            default:
                return image;
        }
    }
};