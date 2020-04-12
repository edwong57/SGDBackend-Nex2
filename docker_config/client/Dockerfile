FROM node:10.16.0

WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# copy package.json
COPY package.json /usr/src/app/package.json

RUN npm install

EXPOSE 3000
CMD ["npm", "run" "start"]
