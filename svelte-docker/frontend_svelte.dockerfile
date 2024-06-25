FROM node:22.3.0-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get -y install 

WORKDIR /frontend-svelte

COPY ./frontend-svelte /frontend-svelte

RUN ls -la /frontend-svelte

RUN npm install
RUN npm run build

EXPOSE 5173

CMD [ "npm", "run", "preview" , "--", "--host", "0.0.0.0"]
