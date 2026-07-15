FROM node:20-bookworm-slim

ARG KOREA_WEBTOON_API_REF=main

WORKDIR /app

ADD https://github.com/HyeokjaeLee/korea-webtoon-api/archive/refs/heads/${KOREA_WEBTOON_API_REF}.tar.gz /tmp/korea-webtoon-api.tar.gz

# The upstream start command runs TypeScript through ts-node, so its
# development dependencies (including @types/node) are required at runtime.
RUN tar -xzf /tmp/korea-webtoon-api.tar.gz --strip-components=1 \
    && npm install --legacy-peer-deps \
    && rm /tmp/korea-webtoon-api.tar.gz

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

CMD ["npm", "start"]
