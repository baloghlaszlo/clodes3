import {RANDOM_RECT_ENDPOINT, RANDOM_FRAME_ENDPOINT, LABELER_OPENED, LABELER_CLOSED} from './constants';

function labelerOpened(endpoint) {
    return {
        type: LABELER_OPENED,
        payload: endpoint
    };
}

export function rectLabelerOpened() {
    return labelerOpened(RANDOM_RECT_ENDPOINT);
}

export function frameLabelerOpened() {
    return labelerOpened(RANDOM_FRAME_ENDPOINT);
}

export function labelerClosed() {
    return {
        type: LABELER_CLOSED
    };
}