import socket  # 导入 socket 模块，提供网络通信功能
import threading

SERVER_PORT = 5432  # 设置服务器端口
MAX_PENDING = 10  # 最大等待连接数
MAX_LINE = 256  # 每次接收的最大字节数

def handle_client(new_s, addr):
    """处理与客户端的通信"""
    print(f"Connection from {addr}")  # 输出客户端的地址信息

    try:
        while True:
            # 接收来自客户端的数据，最多接收 MAX_LINE 字节
            data = new_s.recv(MAX_LINE)

            if not data:
                # 如果接收到的数据为空，表示连接已关闭
                print("Connection closed")
                break  # 退出循环，关闭当前连接

            # 打印接收到的数据
            print(f"Received from {addr}: {data.decode('utf-8')}")
    except socket.error as e:
        print(f"recv failed: {e}")
    finally:
        # 关闭当前与客户端的连接
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
