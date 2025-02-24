import socket
import sys
import threading

SERVER_PORT = 5432  # 设置服务器端口
MAX_LINE = 256  # 设置最大消息长度
BUFFER_SIZE = 4096


def send_message(s, file_or_input):
    """发送消息到服务器"""
    if isinstance(file_or_input, str):  # 如果是文件名
        while True:
            try:
                with open(file_or_input, 'r', encoding='utf-8') as file:
                    for line in file:
                        send_in_blocks(s, line.strip())  # 按行读取文件内容并分块发送
                break  # 文件发送成功后退出循环
            except FileNotFoundError:
                print(f"File '{file_or_input}' not found.")
                file_or_input = input("Please enter a valid file path or type 'exit' to quit: ")
                if file_or_input.lower() == 'exit':
                    print("Exiting file sending process.")
                    return
            except Exception as e:
                print(f"Error reading file '{file_or_input}': {e}")
                return
    else:  # 如果是标准输入
        last_input = ''
        while True:
            try:
                buf = input()  # 获取用户的输入数据
                if buf == "":  # 检查是否输入空行
                    if last_input == "":  # 连续两次输入空行，退出
                        print("Exiting client...")
                        s.close()  # 关闭套接字
                        sys.exit(0)  # 退出程序
                    else:
                        last_input = ""  # 记录第一次空行输入
                else:
                    last_input = buf  # 更新 last_input
                send_in_blocks(s, buf)  # 调用分块发送函数
            except KeyboardInterrupt:
                print("Exiting client due to KeyboardInterrupt.")
                s.close()  # 关闭套接字
                sys.exit(0)  # 退出程序


def send_in_blocks(sock, data):
    """将数据分块发送，并附加结束标志"""
    try:
        encoded_data = data.encode('utf-8')  # 将数据编码为字节
        # 分块发送数据
        for i in range(0, len(encoded_data), BUFFER_SIZE):
            block = encoded_data[i:i + BUFFER_SIZE]
            sock.sendall(block)  # 发送单个数据块
        sock.sendall(b"<END>")  # 消息结束标志
    except ConnectionResetError:
        print("Error: Connection was reset by the server.")
    except Exception as e:
        print(f"Unexpected error: {e}")


def receive_message(sock):
    """接收来自服务器的消息"""
    buffer = b''  # 用于拼接接收到的分块数据
    while True:
        try:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                print("Server closed the connection.")
                break  # 如果没有收到数据，服务器关闭了连接

            buffer += data
            while b"<END>" in buffer:  # 检查是否接收到结束标志
                message, buffer = buffer.split(b"<END>", 1)
                clean_message = message.decode('utf-8').strip()  # 解码并移除多余的空白
                print(f"Server: {clean_message}")  # 仅输出消息内容
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


def main():
    # 检查命令行参数是否正确
    if len(sys.argv) < 2:
        print("usage: server host [filename]")  # 提供正确的使用方式
        sys.exit(1)  # 退出程序

    host = sys.argv[1]  # 获取命令行输入的目标主机地址（即服务器的 IP 地址）

    # 如果提供了文件路径，获取文件路径
    filename = sys.argv[2] if len(sys.argv) == 3 else None

    # 创建一个 socket 对象，使用 IPv4 地址族和 TCP 协议
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"client: socket creation failed: {e}")  # 如果创建套接字失败，打印错误信息
        sys.exit(1)  # 退出程序

    # 获取目标主机的 IP 地址
    try:
        ip_address = socket.gethostbyname(host)  # 通过域名解析得到目标主机的 IP 地址
    except socket.gaierror as e:
        print(f"client: unknown host: {host}")  # 如果主机名解析失败，打印错误信息
        sys.exit(1)  # 退出程序

    # 连接到目标服务器
    try:
        s.connect((ip_address, SERVER_PORT))  # 使用获取到的 IP 地址和指定端口连接到服务器
    except socket.error as e:
        print(f"client: connect failed: {e}")  # 如果连接失败，打印错误信息
        s.close()  # 关闭套接字
        sys.exit(1)  # 退出程序

    # 启动接收线程
    receive_thread = threading.Thread(target=receive_message, args=(s,), daemon=True)
    receive_thread.start()

    # 启动发送线程
    send_thread = threading.Thread(target=send_message, args=(s, filename if filename else sys.stdin), daemon=True)
    send_thread.start()

    # 等待接收线程结束
    receive_thread.join()
    # 关闭套接字，结束连接
    s.close()


# 程序入口
if __name__ == "__main__":
    main()  # 调用 main 函数执行程序
