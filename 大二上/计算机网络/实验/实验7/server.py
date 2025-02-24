import socket  # 导入 socket 模块，提供网络通信功能
import threading

SERVER_PORT = 5432  # 设置服务器端口
MAX_PENDING = 10  # 最大等待连接数
BUFFER_SIZE = 4096  # 每次接收的最大字节数

def handle_client(new_s, addr):
    """处理与客户端的通信"""
    print(f"Connection from {addr}")

    def server_send():
        """服务器主动发送消息给客户端"""
        try:
            while True:
                message = input()  # 服务器主动输入消息
                if message.lower() == "exit":
                    print("Exiting server send mode.")
                    break  # 输入 exit 退出发送模式
                new_s.sendall((message + "<END>").encode('utf-8'))  # 发送消息
        except socket.error as e:
            print(f"Server send error: {e}")

    # 创建并启动主动发送消息的线程
    send_thread = threading.Thread(target=server_send, daemon=True)
    send_thread.start()

    try:
        buffer = b''  # 用于拼接接收到的分块数据
        while True:
            data = new_s.recv(BUFFER_SIZE)
            if not data:
                break  # 客户端关闭连接时退出循环

            buffer += data
            # 检查是否接收到结束标志
            if b"<END>" in buffer:
                message = buffer.replace(b"<END>", b'').decode('utf-8')
                # print(f"Complete message from {addr}: {message}")
                print(message)
                buffer = b''  # 清空缓存区，准备接收下一条消息

                # 服务器回应
                response = f"Received: {message}"  # 构造回应消息
                new_s.sendall((response + "<END>").encode('utf-8'))  # 发送响应给客户端

    except socket.error as e:
        print(f"recv failed: {e}")
    finally:
        print(f"Client {addr} disconnected.")
        new_s.close()


def main():
    # 创建一个 socket 对象，使用 IPv4 地址和 TCP 协议
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"server: socket creation failed: {e}")  # 如果 socket 创建失败，打印错误信息
        return  # 退出程序

    # 设置地址结构，绑定到本地所有 IP 地址（'0.0.0.0'）和指定端口（SERVER_PORT）
    try:
        s.bind(('0.0.0.0', SERVER_PORT))  # 尝试绑定到指定的端口
        print(f"Server is listening on port {SERVER_PORT}...")
    except socket.error as e:
        # 如果绑定失败，打印错误信息并退出
        print(f"server: bind failed: {e}")
        s.close()  # 关闭套接字
        return  # 退出程序

    # 设置监听，最大等待连接数为 MAX_PENDING
    s.listen(MAX_PENDING)

    # 输出服务器正在监听的端口
    print(f"Listening on port {SERVER_PORT}...")

    while True:
        # 不断地等待并接受新的连接
        try:
            # 接受连接并获取新的套接字和客户端的地址信息
            new_s, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(new_s, addr))
            client_thread.start()

        except socket.error as e:
            # 如果 accept 失败，打印错误信息并继续等待其他连接
            print(f"server: accept failed: {e}")
            continue

    # 关闭服务器的监听套接字
    s.close()


if __name__ == "__main__":
    main()  # 启动服务器
