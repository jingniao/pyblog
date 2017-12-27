FROM centos

WORKDIR /blog_new/
RUN yum install -y epel-release && \
    yum update -y && \
    yum install -y python-pip
RUN mkdir ~/.pip && \ 
cd ~/.pip/ && \
echo -e "[global]\nindex-url = https://mirrors.ustc.edu.cn/pypi/web/simple\nformat = columns" >  pip.conf

COPY requirements.txt ./
RUN pip install -r requirements.txt

ADD ./ ./
ENTRYPOINT '/blog_new/entrypoint.py'
