#!/usr/bin/env bash

# Clear the terminal screen
clear

# Get the current date and format it
formatted_date=$(date +"%A, %B %d, %Y %I:%M:%S %p")

# Function to check file size
check_file_size() {
    local file="$1"
    local size=$(du -m "$file" | awk '{print $1}')
    if [ "$size" -gt 50 ]; then
        echo "Skipping file: $file (size exceeds 50MB)"
        return 1
    else
        return 0
    fi
}

# Pull the latest changes from the Git repository
git pull
if [ $? -ne 0 ]; then
    echo "Error: Git pull failed"
    exit 1
fi

# # Add all changes to the Git staging area, excluding files larger than 50MB
# echo "Checking for files over 50MB..."
# while IFS= read -r -d '' file; do
#     # Check if the file path contains 'venv' or 'NONI'; if so, skip processing
#     if [[ "$file" == *"/venv/"* || "$file" == *"/NONI/"* ]]; then
#         echo "Skipping folder: $file"
#         continue
#     fi
    
#     check_file_size "$file"
#     if [ $? -eq 0 ]; then
#         echo "Adding file: $file"
#         git add "$file"
#     else
#         echo "$file" >> .gitignore
#     fi
# done < <(find . -type f -not \( -path "./venv/*" -o -path "./NONI/*" \) -print0)

# Prompt user to continue
git add .
echo "Press Enter to continue..."
read -r

# Commit the changes with a timestamp
git commit -m "Committed at: $formatted_date"
if [ $? -ne 0 ]; then
    echo "Error: Git commit failed"
    exit 1
fi

# Push the changes to the remote repository
git push
if [ $? -ne 0 ]; then
    echo "Error: Git push failed"
    exit 1
fi

# Display a success message
echo "Script executed successfully!"

# Pause execution for 3 seconds
sleep 3
