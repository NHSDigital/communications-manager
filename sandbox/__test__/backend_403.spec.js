import request from "supertest";
import { setup } from './helpers.js';
import * as uuid from 'uuid';

describe('backend_403', () => {
  let env;
  let server;

  before(function () {
    env = process.env;
    server = setup()
  });

  after(function () {
    process.env = env;
    server.close();
  });

  it('can mock a 403 response type for invalid certificates', (done) => {
    request(server)
      .get('/_invalid_certificate')
      .expect(403, '{"message":"Forbidden"}', done);
  });

  it("returns a X-Correlation-Id when provided", (done) => {
    const correlation_id = uuid.v4();
    request(server)
      .get('/_invalid_certificate')
      .set('X-Correlation-Id', correlation_id)
      .expect(403, '{"message":"Forbidden"}')
      .expect("X-Correlation-Id", correlation_id, done);
  });
})
