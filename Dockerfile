FROM python:3

RUN pip3 install Scrapy && \
    pip3 install BeautifulSoup4 

#COPY finance /usr/local/scandai/finance
#WORKDIR /usr/local/scandai/finance

CMD ["/bin/bash"]
