cd ../
docker image build -t sunalyzer .
docker container run -p 8020:5000 -v $(pwd)/local_testing/test_data:/data sunalyzer
