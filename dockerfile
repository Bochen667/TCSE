FROM python:3.10.6

# 安裝系統工具與編譯 SQLite 依賴
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    ca-certificates \
    libssl-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 安裝 SQLite 3.45.2（也可以換其他版本 >= 3.35）
RUN curl -O https://www.sqlite.org/2024/sqlite-autoconf-3450200.tar.gz && \
    tar xzf sqlite-autoconf-3450200.tar.gz && \
    cd sqlite-autoconf-3450200 && \
    ./configure --prefix=/usr/local && \
    make && make install && \
    cd .. && rm -rf sqlite-autoconf-3450200*

# 確保 Python 用到新版 SQLite
ENV LD_LIBRARY_PATH="/usr/local/lib"
ENV PKG_CONFIG_PATH="/usr/local/lib/pkgconfig"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
