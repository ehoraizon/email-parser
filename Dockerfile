FROM python:3.7-alpine3.15
WORKDIR /app
COPY . .
RUN apk update && apk add npm mariadb-dev build-base bash
RUN pip install -r requirements.txt
RUN cd ./email_parser/frontend && npm i && npm run build
RUN chmod +x /app/start.sh
RUN chmod +x /app/wait-for-it.sh
ENTRYPOINT ["/app/start.sh"]
CMD ["default"]
