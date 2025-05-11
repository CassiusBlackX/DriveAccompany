const WebSocket = require('ws');
const fs = require('fs'); // 引入文件系统模块
const url = require('url'); // 引入 URL 解析模块

// 创建 WebSocket 服务器，监听 7979 端口
const wss = new WebSocket.Server({ port: 7979 });
    
// 定义 client1 和 client2 的 WebSocket 连接
let client1 = null;
let client2 = null;

wss.on('connection', (ws, req) => {
    const clientIp = req.socket.remoteAddress;  // 获取客户端的 IP 地址
    console.log(`New connection from IP ${clientIp}`);

    const query = url.parse(req.url, true).query;
    const clientId = query.client_id;
    //console.log(`New connection from IP ${clientId}`);

    // 判断是否已经连接了 client1 或 client2
    if (clientId=="client2") {
        client2 = ws;
        console.log('Client2 connected');

        client2.on('message', (message) => {
            console.log('Received message from Client2:', message);
        });

        client2.on('close', () => {
            console.log('Client2 disconnected');
            client2 = null;  // 清除 client2
        });

    } else if (clientId=="client1") {
        client1 = ws;
        console.log('Client1 connected');

        client1.on('message', (message) => {
            console.log('Received message from Client1:', message);

            // 如果是第一个消息，保存到本地
            if (message) {
                // fs.writeFile('C:\\Users\\10210\\Desktop\\Jetson\\my_note\\vue_node\\leanrVue\\websocket\\base64message.jpg', message, (err) => {
                //     if (err) {
                //         console.error('Error saving the image:', err);
                //     } else {
                //         console.log('Message saved successfully!');
                //     }
                // });
                message_char = message.toString('utf8'); // 将 Buffer 转为字符串

                const imageBuffer = Buffer.from(message_char, 'base64');
                //const buffer = Buffer.from(data, 'base64');


                // fs.writeFile('C:\\Users\\10210\\Desktop\\Jetson\\my_note\\vue_node\\leanrVue\\websocket\\received_image.jpg', imageBuffer, (err) => {
                //     if (err) {
                //         console.error('Error saving the image:', err);
                //     } else {
                //         console.log('Image saved successfully!');
                //     }
                // });

                // 发送解码后的 Buffer 给 Client2
                if (client2) {
                    client2.send(imageBuffer);
                }
            }
        });

        client1.on('close', () => {
            console.log('Client1 disconnected');
            if (client2) {//给前端发送-1代表后端断开，让前端有所处理以保证健壮性
                client2.send(-1);
                console.log('Send -1 to Client2');
            }
            client1 = null;  // 清除 client1
        });

    } else {
        console.log('A new client tried to connect but the limit is 2. Disconnecting...');
        ws.close(); // 超过限制的连接，直接关闭
    }
});

console.log('WebSocket server is listening on ws://0.0.0.0:7979');
