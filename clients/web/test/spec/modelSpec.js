/**
 * Intercept window.location.assign calls so we can test the behavior of,
 * e.g. download directives that occur from js.
 */
(function () {
    window.location.assign = function (url) {
        girderTest._redirect = url;
    };
}());

/**
 * Start the girder backbone app.
 */
girderTest.startApp();

describe('Test the model class', function () {
    var lastRequest, triggerRestError = false, requestCount = 0;

    beforeEach(function () {
        girder.rest.mockRestRequest(function (opts) {
            requestCount += 1;
            lastRequest = opts;
            var resp = $.Deferred();
            if (triggerRestError) {
                resp.reject('err');
            } else {
                resp.resolve({});
            }
            // The jqXHR response of a rest request needs an error function
            resp.error = resp.fail;
            return resp;
        });
    });

    afterEach(function () {
        girder.rest.unmockRestRequest();
    });

    it('test the base model', function () {
        var SampleModel = girder.models.Model.extend({
            resourceName: 'sampleResource'
        });
        var id = '012345678901234567890123';

        var model = new SampleModel({});
        // test name
        model.set('name', 'sample');
        expect(model.name()).toBe('sample');
        // test increment
        expect(model.get('count')).toBe(undefined);
        model.set('count', 0);
        model.increment('count');
        expect(model.get('count')).toBe(1);
        model.increment('count');
        expect(model.get('count')).toBe(2);
        model.increment('count', 10);
        expect(model.get('count')).toBe(12);
        model.increment('count', 0);
        expect(model.get('count')).toBe(12);
        // test save
        model.resourceName = null;
        model.save();
        model.resourceName = 'sampleResource';
        expect(requestCount).toBe(0);
        model.save();
        expect(requestCount).toBe(1);
        expect(lastRequest.type).toBe('POST');
        expect(lastRequest.data).toEqual({count: 12, name: 'sample'});
        model.set('_id', '012345678901234567890123');
        model.save();
        expect(requestCount).toBe(2);
        expect(lastRequest.type).toBe('PUT');
        expect(lastRequest.data).toEqual({
            count: 12, name: 'sample', _id: id});
        triggerRestError = true;
        model.save();
        expect(requestCount).toBe(3);
        triggerRestError = false;
        // test fetch
        requestCount = 0;
        model.resourceName = null;
        model.fetch();
        model.resourceName = 'sampleResource';
        expect(requestCount).toBe(0);
        model.fetch();
        expect(requestCount).toBe(1);
        expect(lastRequest.type).toBe(undefined);
        expect(lastRequest.path).toBe('sampleResource/' + id);
        expect(lastRequest.error).toBe(undefined);
        expect(lastRequest.data).toBe(undefined);
        model.fetch({extraPath: 'abc'});
        expect(requestCount).toBe(2);
        expect(lastRequest.path).toBe('sampleResource/' + id + '/abc');
        expect(lastRequest.error).toBe(undefined);
        expect(lastRequest.data).toBe(undefined);
        model.fetch({ignoreError: true});
        expect(requestCount).toBe(3);
        expect(lastRequest.path).toBe('sampleResource/' + id);
        expect(lastRequest.error).toBe(null);
        expect(lastRequest.data).toBe(undefined);
        model.fetch({data: {param1: 'value1'}});
        expect(requestCount).toBe(4);
        expect(lastRequest.path).toBe('sampleResource/' + id);
        expect(lastRequest.error).toBe(undefined);
        expect(lastRequest.data).toEqual({param1: 'value1'});
        triggerRestError = true;
        model.fetch();
        expect(requestCount).toBe(5);
        triggerRestError = false;
        // test downloadUrl
        expect(model.downloadUrl()).toBe(girder.rest.apiRoot + '/sampleResource/' + id + '/download');
        expect(model.downloadUrl({foo: 'bar'})).toBe(girder.rest.apiRoot + '/sampleResource/' + id + '/download?foo=bar');
        // test download
        model.download();
        waitsFor(function () {
            return girderTest._redirect !== null;
        }, 'redirect to the resource download URL');
        runs(function () {
            expect(/^http:\/\/.*\/api\/v1\/sampleResource\/.+\/download$/.test(
                girderTest._redirect)).toBe(true);
        });
        // destroy
        requestCount = 0;
        model.resourceName = null;
        model.destroy();
        model.resourceName = 'sampleResource';
        expect(requestCount).toBe(0);
        model.destroy();
        expect(requestCount).toBe(1);
        expect(lastRequest.type).toBe('DELETE');
        expect(/progress=true/.test(lastRequest.path)).toBe(false);
        expect(lastRequest.error).toBe(null);
        model.destroy({progress: true});
        expect(requestCount).toBe(2);
        expect(lastRequest.type).toBe('DELETE');
        expect(/progress=true/.test(lastRequest.path)).toBe(true);
        expect(lastRequest.error).toBe(null);
        model.destroy({throwError: false});
        expect(requestCount).toBe(3);
        expect(lastRequest.type).toBe('DELETE');
        expect(/progress=true/.test(lastRequest.path)).toBe(false);
        expect(lastRequest.error).toBe(undefined);
        triggerRestError = true;
        model.destroy();
        expect(requestCount).toBe(4);
        triggerRestError = false;
        // getAccessLevel
        expect(model.getAccessLevel()).toBe(undefined);
        model.set('_accessLevel', 'abc');
        expect(model.getAccessLevel()).toBe('abc');
    });
});
