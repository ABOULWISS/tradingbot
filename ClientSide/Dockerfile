


FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# 👇 use preview (serves built app correctly)
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]