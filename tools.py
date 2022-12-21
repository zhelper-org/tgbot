async def pybyte(size, dot=2):
    size = float(size)
    human_size = ''
    # 位 比特 bit
    if 0 <= size < 1:
        human_size = str(round(size / 0.125, dot)) + 'b'
    # 字节 字节 Byte
    elif 1 <= size < 1024:
        human_size = str(round(size, dot)) + 'B'
    # 千字节 千字节 Kilo Byte
    elif pow(1024, 1) <= size < pow(1024, 2):
        human_size = str(round(size / pow(1024, 1), dot)) + 'KB'
    # 兆字节 兆 Mega Byte
    elif pow(1024, 2) <= size < pow(1024, 3):
        human_size = str(round(size / pow(1024, 2), dot)) + 'MB'
    return human_size