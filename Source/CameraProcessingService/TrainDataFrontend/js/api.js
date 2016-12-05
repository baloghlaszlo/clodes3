import 'whatwg-fetch';

export function getImageData(endpoint) {
    console.log('Loading image from ' + endpoint);
    return fetch(endpoint).then(result => result.json().then(body => ({
        ...body,
        isError: result.status < 200 || result.status >= 300
    })));
}

export function submitLabel(endpoint, label) {
    console.log('Sending label ' + label + ' to ' + endpoint);
    return fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'label': label
        })
    });
}