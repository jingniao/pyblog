FROM centos

WORKDIR /blog_new/
RUN yum install -y epel-release && \
    yum update -y && \
    yum install -y python-pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

ADD ./ ./
ENTRYPOINT '/blog_new/entrypoint.py'
