#!/bin/bash
test_number=$RANDOM
echo $test_number
echo "Creating new timeline post using POST route..."
curl --request POST http://127.0.0.1:5000/api/timeline_post -d "name=$test_number&email=test@gmail.com&content=Bash script test post"
echo "Confirming new post was created using GET route..." 
output=$(curl -s http://127.0.0.1:5000/api/timeline_post | jq ".timeline_posts[0].name")
echo $output
echo $test_number
if [ "$output" = "$test_number" ]; then
    echo "New post was successfully created!"
else
    echo "New post was not created successfully."
fi

