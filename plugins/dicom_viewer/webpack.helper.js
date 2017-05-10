module.exports = function (config) {
    config.module.rules.push({
        test: /\.glsl$/,
        loader: 'shader-loader',
        include: [/node_modules(\/|\\)vtk\.js(\/|\\)/],
    });
    config.module.rules.push({
        test: /\.js$/,
        include: [/node_modules(\/|\\)vtk\.js(\/|\\)/],
        loaders: [{
            loader: 'babel-loader',
            query: {
                presets: ['es2015', 'react']
            }
        }, {
            loader: 'string-replace-loader',
            query: {
                multiple: [
                    {search: /test\.onlyIfWebGL/g, replace: 'test'}
                ]
            }
        }]
    });
    return config;
};
