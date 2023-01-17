npm run build
cd build
echo "FROM node:16.13.2
WORKDIR /usr/src/app
RUN npm install -g serve
COPY . .
CMD [ \"serve\", \"-s\", \".\", \"-p\", \"8080\"]
" > Dockerfile

docker build -t cloud-cw-team-client .
docker tag cloud-cw-team-client gcr.io/cloud-cw-team/cloud-cw-team-client
docker push gcr.io/cloud-cw-team/cloud-cw-team-client
gcloud run deploy cloud-cw-team-client --image gcr.io/cloud-cw-team/cloud-cw-team-client --region europe-west1 --allow-unauthenticated --project=cloud-cw-team

rm -rf Dockerfile

