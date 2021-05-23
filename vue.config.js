module.exports = {
    devServer: {
        proxy: {
            '/socket.io': {
                target: 'http://127.0.0.1:5000',
                ws: true,
                changeOrigin: true
            },
            'sockjs-node': {
                target: 'http://127.0.0.1:5000',
                ws: false,
                changeOrigin: true
            },
            '/api': {
                target: 'http://127.0.0.1:5000',
                changeOrigin: true
            }
        }

    }
}