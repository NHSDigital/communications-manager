
const request = require("supertest");
const assert = require("chai").assert;

describe("app handler tests", function () {
    let server;
    let env;
    const version_info = {
        build_label:"1233-shaacdef1",
        releaseId:"1234",
        commitId:"acdef12341ccc"
    };

    before(function () {
        env = process.env;
        let app = require("./app");
        app.setup({
            VERSION_INFO: JSON.stringify(version_info),
            LOG_LEVEL: (process.env.NODE_ENV === "test" ? "warn": "debug")
        });
        server = app.start();
    });

    beforeEach(function () {

    });
    afterEach(function () {

    });
    after(function () {
        process.env = env;
        server.close();
    });

    it("responds to /_ping", (done) => {
        request(server)
            .get("/_ping")
            .expect(200, {
                status: "pass",
                ping: "pong",
                service: "communications-manager",
                version: version_info
            })
            .expect("Content-Type", /json/, done);
    });

    it("responds to /_status", (done) => {
        request(server)
            .get("/_status")
            .expect(200, {
                status: "pass",
                ping: "pong",
                service: "communications-manager",
                version: version_info
            })
            .expect("Content-Type", /json/, done);
    });

    describe('/api/v1/send', () => {
        it('returns a 400 when body doesnt exist', (done) => {
            request(server)
                .post('/api/v1/send')
                .expect(400, {
                    message: 'Missing request body'
                })
                .expect("Content-Type", /json/, done);
        });

        it('returns a 400 when the sendingGroupId doesnt exist', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({})
                .expect(400, {
                    message: 'Missing sendingGroupId'
                })
                .expect("Content-Type", /json/, done);
        });

        it('returns a 400 when the sendingGroupId is null', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: null
                })
                .expect(400, {
                    message: 'Missing sendingGroupId'
                })
                .expect("Content-Type", /json/, done);
        });

        it('returns a 400 when the requestRefId doesnt exist', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: 'sending-group-id'
                })
                .expect(400, {
                    message: 'Missing requestRefId'
                })
                .expect("Content-Type", /json/, done);
        });

        it('returns a 400 when the requestRefId is null', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: 'sending-group-id',
                    requestRefId: null
                })
                .expect(400, {
                    message: 'Missing requestRefId'
                })
                .expect("Content-Type", /json/, done);
        });

        it('returns a 400 when the data doesnt exist', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: 'sending-group-id',
                    requestRefId: 'request-ref-id'
                })
                .expect(400, {
                    message: 'Missing data array'
                })
                .expect("Content-Type", /json/, done);
        });

        it('returns a 400 when the data is null', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: 'sending-group-id',
                    requestRefId: 'request-ref-id',
                    data: null
                })
                .expect(400, {
                    message: 'Missing data array'
                })
                .expect("Content-Type", /json/, done);
        });

        it('returns a 400 when the data is not an array', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: 'sending-group-id',
                    requestRefId: 'request-ref-id',
                    data: 'invalid'
                })
                .expect(400, {
                    message: 'Missing data array'
                })
                .expect("Content-Type", /json/, done);
        });

        it('returns a 400 when the data does not contain items with requestItemRefId', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: 'sending-group-id',
                    requestRefId: 'request-ref-id',
                    data: [
                        {
                            notARequestItemRefId : '1'
                        }
                    ]
                })
                .expect(400, {
                    message: 'Missing requestItemRefIds'
                })
                .expect("Content-Type", /json/, done);
        });

        it('returns a 400 when the data contains duplicate requestItemRefIds', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: 'sending-group-id',
                    requestRefId: 'request-ref-id',
                    data: [
                        {
                            requestItemRefId : '1'
                        },
                        {
                            requestItemRefId : '1'
                        }
                    ]
                })
                .expect(400, {
                    message: 'Duplicate requestItemRefIds'
                })
                .expect("Content-Type", /json/, done);
        });

        it('returns a 404 when sendingGroupId is not found', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: 'sending-group-id',
                    requestRefId: 'request-ref-id',
                    data: [
                        {
                            requestItemRefId : '1'
                        },
                        {
                            requestItemRefId : '2'
                        }
                    ]
                })
                .expect(404, {
                    message: 'Routing Config does not exist for clientId "sandbox_client_id" and sendingGroupId "sending-group-id"'
                })
                .expect("Content-Type", /json/, done);
        });

        it('returns a 400 when the sending group has missing templates', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: 'c8857ccf-06ec-483f-9b3a-7fc732d9ad48',
                    requestRefId: 'request-ref-id',
                    data: [
                        {
                            requestItemRefId : '1'
                        },
                        {
                            requestItemRefId : '2'
                        }
                    ]
                })
                .expect(400, {
                    message: 'Templates required in "c8857ccf-06ec-483f-9b3a-7fc732d9ad48" routing config not found'
                })
                .expect("Content-Type", /json/, done);
        });

        it('returns a 400 when the sending group has duplicate templates', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: 'a3a4e55d-7a21-45a6-9286-8eb595c872a8',
                    requestRefId: 'request-ref-id',
                    data: [
                        {
                            requestItemRefId : '1'
                        },
                        {
                            requestItemRefId : '2'
                        }
                    ]
                })
                .expect(400, {
                    message: 'Duplicate templates found: [{\"name\":\"EMAIL_TEMPLATE\",\"type\":\"EMAIL\"},{\"name\":\"SMS_TEMPLATE\",\"type\":\"SMS\"},{\"name\":\"LETTER_TEMPLATE\",\"type\":\"LETTER\"},{\"name\":\"LETTER_PDF_TEMPLATE\",\"type\":\"LETTER_PDF\"},{\"name\":\"NHSAPP_TEMPLATE\",\"type\":\"NHSAPP\"}]'
                })
                .expect("Content-Type", /json/, done);
        });

        it('can simulate a 500 error', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: 'b838b13c-f98c-4def-93f0-515d4e4f4ee1',
                    requestRefId: 'simulate-500',
                    data: [
                        {
                            requestItemRefId : '1'
                        },
                        {
                            requestItemRefId : '2'
                        }
                    ]
                })
                .expect(500, {
                    message: 'Error writing request items to DynamoDB'
                })
                .expect("Content-Type", /json/, done);
        });

        it('responds with a 200 when the request is correctly formatted', (done) => {
           request(server)
                .post('/api/v1/send')
                .send({
                    sendingGroupId: 'b838b13c-f98c-4def-93f0-515d4e4f4ee1',
                    requestRefId: 'request-id',
                    data: [
                        {
                            requestItemRefId : '1'
                        },
                        {
                            requestItemRefId : '2'
                        }
                    ]
                })
                .expect(200)
                .expect((res) => {
                    assert.notEqual(res.body.requestId, undefined);
                    assert.notEqual(res.body.requestId, null);
                })
                .expect("Content-Type", /json/, done);
        });
    });
});

