cd ../
docker image build -t sunalyzer .
docker container run sunalyzer -p 80:80
