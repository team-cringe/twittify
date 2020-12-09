# FROM node:14 as build-deps
FROM node:14
WORKDIR /usr/src/app
COPY package.json tsconfig.json ./
RUN yarn
COPY src ./src
COPY public ./public
ENV PORT 8080
EXPOSE $PORT
CMD ["yarn", "start"]
# RUN yarn build

# FROM nginx
# # COPY --from=build-deps /usr/src/app/build /data/client
# COPY --from=build-deps /usr/src/app/build /usr/share/nginx/html
# # COPY nginx.conf /etc/nginx/nginx.conf
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]