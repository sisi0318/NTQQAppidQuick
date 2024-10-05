apt-get install -y \
    openbox \
    xorg \
    dbus-user-session \
    curl \
    unzip \
    xvfb \
    supervisor \
    libnotify4 \
    libnss3 \
    xdg-utils \
    libsecret-1-0 \
    ffmpeg \
    libgbm1 \
    libasound2 \
    fonts-wqy-zenhei \
    gnutls-bin \
    tzdata

# 安装关键依赖
apt-get install fluxbox -y
apt-get install x11vnc -y

# 安装QQ
curl -o linuxqq.deb $1
dpkg -i linuxqq.deb
apt-get -f install -y
rm linuxqq.deb
chmod 777 /opt/QQ/

# 启动QQ
dbus-daemon --config-file=/usr/share/dbus-1/system.conf --print-address &
Xvfb :1 -screen 0 1080x760x16 &
sleep 5  # 等待 Xvfb 启动
export DISPLAY=:1
fluxbox &
sleep 5  # 等待 fluxbox 启动
x11vnc -display :1 -noxrecord -noxfixes -noxdamage -forever -rfbauth ~/.vnc/passwd &
python -m pip install frida
python -m pip install requests

# 导出环境变量
export API=${API}
export SEND_KEY=${SEND_KEY}

# 运行 Python 脚本
sudo python GetAppid.py $1 $2

# 输出所有名为qq的进程
ps -ef | grep qq