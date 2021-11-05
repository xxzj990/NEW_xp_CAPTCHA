FROM centos:7

WORKDIR /usr/src/app

# Aliyun
RUN set -ex \
 && yum -y install wget \
 && wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-7.repo \
 && yum clean all && yum makecache

# Python
RUN set -ex \
 && yum -y groupinstall "Development tools" \
 && yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel \
 && wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz \
 && tar -zxvf Python-3.7.0.tgz \
 && cd Python-3.7.0 \
 && ./configure --prefix=/usr/local/python3 \
 && make \
 && make install \
 && cd .. \
 && rm -rf Python-3.7.0* \
 && ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3 \
 && ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip

# OCR
RUN set -ex \
 && pip install --upgrade pip \
 && python3 -m pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com muggle-ocr \
 && yum -y install libglvnd-glx-1.0.1-0.8.git5baa1e5.el7.x86_64

COPY . .

# Start server.
EXPOSE 8899
CMD ["python3", "server.py"]