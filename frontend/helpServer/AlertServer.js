const WebSocket = require('ws');
const fs = require('fs'); // 引入文件系统模块
const url = require('url'); // 引入 URL 解析模块

// 创建 WebSocket 服务器，监听 6868 端口
const wss = new WebSocket.Server({ port:6868 });
    
// 定义 client1 和 client2 的 WebSocket 连接
let client1 = null;
let client2 = null;

wss.on('connection', (ws, req) => {
    const clientIp = req.socket.remoteAddress;  // 获取客户端的 IP 地址
    console.log(`New connection from IP ${clientIp}`);

    const query = url.parse(req.url, true).query;
    const clientId = query.client_id;
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

            console.log('Received buffer from Client1:', message);

            // 将 buffer 转换为整数
            const intValue = message.readInt8(); // 使用合适的方法，如 readInt8, readInt16BE, readInt32BE，根据你的数据格式

            console.log(`Converted int value: ${intValue-48}`);

            // 将整数转发给 client2
            if (client2) {
                client2.send(intValue-48); // 转发整数
                //console.log('Send message to front-end :',imageBuffer);
            }


        });

        client1.on('close', () => {
            console.log('Client1 disconnected');
            client1 = null;  // 清除 client1
        });

    } else {
        console.log('A new client tried to connect but the limit is 2. Disconnecting...');
        ws.close(); // 超过限制的连接，直接关闭
    }
});

console.log('WebSocket server is listening on ws://0.0.0.0:6868');
