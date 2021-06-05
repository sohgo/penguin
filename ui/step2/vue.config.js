const path = require('path');

module.exports = {
    transpileDependencies: [
        'vuetify'
    ],
    disableAssetsSubdir: true,
    publicPath: process.env.NODE_ENV === 'production'
        ? '/2'
        : '/'
};
