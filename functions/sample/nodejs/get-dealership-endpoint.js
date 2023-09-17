const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

const authenticator = new IamAuthenticator({ apikey: "YOUR_API_KEY" });
const cloudant = CloudantV1.newInstance({ authenticator });

async function fetchDealerships(params) {
    const db = 'dealerships';
    if (params.st) {
        return cloudant.postFind({ db, selector: { st: params.st } });
    } else if (params.id) {
        return cloudant.postFind({ db, selector: { id: parseInt(params.id) } });
    } else {
        return cloudant.postAllDocs({ db, includeDocs: true, limit: 10 });
    }
}

async function main(params) {
    try {
        const result = await fetchDealerships(params);
        let code = result.result.docs.length ? 200 : 404;
        return {
            statusCode: code,
            headers: { 'Content-Type': 'application/json' },
            body: result.result.docs
        };
    } catch (error) {
        console.error('Error:', error);
        return { statusCode: 500, body: 'Internal Server Error' };
    }
}

exports.main = main;
