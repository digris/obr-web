FROM savonet/liquidsoap:v2.3.1

WORKDIR /app

COPY devsupport/news/ ./

EXPOSE 8000

# CMD exec liquidsoap news.liq

CMD ["liquidsoap", "news.liq"]
