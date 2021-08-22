const path = require('path');

module.exports = {
    productionSourceMap: process.env.NODE_ENV === 'production'
        ? false
        : true,
    transpileDependencies: [
        'vuetify'
    ],
    disableAssetsSubdir: true,
    publicPath: process.env.NODE_ENV === 'production'
        ? '/2'
        : '/'
};
