FROM node:20-bookworm-slim

ARG KOREA_WEBTOON_API_REF=main

WORKDIR /app

ADD https://github.com/HyeokjaeLee/korea-webtoon-api/archive/refs/heads/${KOREA_WEBTOON_API_REF}.tar.gz /tmp/korea-webtoon-api.tar.gz

RUN tar -xzf /tmp/korea-webtoon-api.tar.gz --strip-components=1 \
    && npm install --omit=dev --legacy-peer-deps \
    && rm /tmp/korea-webtoon-api.tar.gz

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

CMD ["npm", "start"]