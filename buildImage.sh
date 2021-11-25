docker stop website-screenshot-tool
docker container rm website-screenshot-tool

#cd angular/siteScreenShot
#ng build --prod --build-optimizer --baseHref="/static/"
#cd ../..

docker build . --tag "website-screenshot" --no-cache
#docker build . --tag "website-screenshot"

#docker run -dit --name website-screenshot-tool \
#-p 1234:1111 \
#--restart unless-stopped \
#website-screenshot