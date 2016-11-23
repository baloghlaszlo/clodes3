
import {RANDOM_FRAME_ENDPOINT, RANDOM_RECT_ENDPOINT} from './constants';

const _frames = [
    {
        isError: false,
        src: '/static/img.jpg',
        labels: {
            uri: '/api/frames/1',
            type: 'count'
        }
    },
    {
        isError: false,
        src: '/static/image.jpg',
        labels: {
            uri: '/api/frames/2',
            type: 'count'
        }
    }
];

const _rects = [
    {
        isError: false,
        src: '/static/face.png',
        labels: {
            uri: '/api/rects/1',
            type: 'face'
        }
    },
    {
        isError: true,
        message: 'Failed to load image.'
    }
];

export function getImageData(endpoint) {
    console.log('Loading image from ' + endpoint);
    return new Promise(resolve => {
        setTimeout(() => {
            switch (endpoint) {
                case RANDOM_FRAME_ENDPOINT:
                    resolve(_frames[Math.floor(Math.random() * _frames.length)]);
                    break;
                case RANDOM_RECT_ENDPOINT:
                    resolve(_rects[Math.floor(Math.random() * _rects.length)]);
                    break;
                default:
                    resolve({
                        isError: true,
                        message: 'Unknown endpoint ' + endpoint
                    });
                    break;
            }
        }, 1000);
    });
}

export function submitLabel(endpoint, label) {
    console.log('Sending label ' + label + ' to ' + endpoint);
    return new Promise(resolve => resolve(null));
}