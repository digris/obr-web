FROM savonet/liquidsoap:v2.3.1

WORKDIR /app

#COPY devsupport/news/rfi/ ./
COPY devsupport/news/srf/ ./

EXPOSE 8000

CMD ["liquidsoap", "news.liq"]
