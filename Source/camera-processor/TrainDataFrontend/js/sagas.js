import {call, fork, put, race, select, spawn, take} from 'redux-saga/effects';
import * as Api from './api';
import {
    LABELER_OPENED, LABELER_CLOSED, LABEL_SUBMITTED, IMAGE_RELOAD_REQUESTED,
    IMAGE_DATA_LOADED, IMAGE_DATA_INVALIDATED, NEW_IMAGE_ENDPOINT_UPDATED
} from './constants';

function* loadNextImageSaga() {
    yield put({type: IMAGE_DATA_INVALIDATED});
    const endpoint = yield select(state => state.nextImageEndpoint);
    const nextImage = yield call(Api.getImageData, endpoint);
    yield put({
        type: IMAGE_DATA_LOADED,
        payload: nextImage
    });
}

function* submitLabelSaga(labelAction) {
    const labelEndpoint = yield select(state => state.image.labels.uri);
    yield put({type: IMAGE_DATA_INVALIDATED});
    yield spawn(Api.submitLabel, labelEndpoint, labelAction.payload);
}

function* labelerSaga(labelerOpenedAction) {
    yield put({
        type: NEW_IMAGE_ENDPOINT_UPDATED,
        payload: labelerOpenedAction.payload
    });
    yield call(loadNextImageSaga);
    //noinspection InfiniteLoopJS
    while (true) {
        let actions = yield race({
            submitted: take(LABEL_SUBMITTED),
            reload: take(IMAGE_RELOAD_REQUESTED)
        });
        if (actions.submitted) {
            yield call(submitLabelSaga, actions.submitted);
        }
        yield call(loadNextImageSaga);
    }
}

function* openLabelerSaga() {
    //noinspection InfiniteLoopJS
    while (true) {
        let labelerOpenedAction = yield take(LABELER_OPENED);
        yield race({
            submitLabels: call(labelerSaga, labelerOpenedAction),
            stop: take(LABELER_CLOSED)
        });
        yield put({type: IMAGE_DATA_INVALIDATED});
    }
}

export default function* trainDataFrontendSaga() {
    yield fork(openLabelerSaga);
}
