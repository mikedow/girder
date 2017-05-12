girderTest.addCoveredScripts([
    '/clients/web/static/built/plugins/{{ cookiecutter.plugin_name }}/plugin.min.js'
]);

girderTest.startApp();

$(function () {
    describe('Test creating an item', function () {
        it('registers admin user',
           girderTest.createUser('admin',
                                 'admin@email.com',
                                 'admin',
                                 'admin',
                                 'admin'));

        it('display the public folder of the user', function () {
            waitsFor(function () {
                return $('a.g-folder-list-link:contains(Public):visible').length === 1;
            }, 'the public folder to be clickable');

            runs(function () {
                $('a.g-folder-list-link:contains(Public)').click();
            });

            waitsFor(function () {
                return $('.g-empty-parent-message:visible').length === 1 &&
                    $('.g-folder-actions-button:visible').length === 1;
            }, 'message that the folder is empty');
        });
    });
});
