import requests
import json
import os
import re
import shutil
from notion_exporter import NotionExporter
from dotenv import load_dotenv
from openai import OpenAI

def fetch_upload_notion_files(open_ai_wrapper, vector_store_id):
    #delete all md files in the markdown folder
    cwd = os.getcwd()  # get current working directory
    folder_name = os.path.join(cwd, "themis", "functions", "notion", "markdown")

    # check if folder exists
    file_paths = [os.path.join(folder_name, file) for file in os.listdir(folder_name) if file.endswith(".md")]
    for file in file_paths:
        os.remove(file)

    load_dotenv()
    NOTION_API_KEY = str(os.getenv("notion_api_key"))
   # print(NOTION_API_KEY)
        
    def make_filename_safe(filename):
        return ''.join(c if c not in '\\/:*?"<>|' else '_' for c in filename.strip()).rstrip('.')

        
    def get_page_title(page_id):
        try:
            response = requests.get(
                f'https://api.notion.com/v1/pages/{page_id}',
                headers={
                    'Notion-Version': '2022-06-28',
                    'Authorization': f'Bearer {NOTION_API_KEY}'
                }
            )
            
            return response.json()["properties"]["title"]["title"][0]["text"]["content"]
        except:
            response = requests.get(
            f'https://api.notion.com/v1/blocks/{page_id}',
            headers={
                'Authorization': f'Bearer {NOTION_API_KEY}',
                'Notion-Version': '2022-06-28'
            }
        )
        
            type = response.json()["type"]
            return response.json()[type]["title"]

        

    exporter = NotionExporter(notion_token=NOTION_API_KEY, export_child_pages=True)

    exported_pages = exporter.export_pages(page_ids=json.loads(os.getenv("notion_pages")["pages"]))

    def save_string_to_file(filename, text):
        try:
            with open(filename, 'w') as file:
                file.write(text)
        except:
            with open(make_filename_safe(filename), 'w') as file:
                file.write(text)
                
            print("Skipped:", filename)
            
    # Function to extract links with the specified format
    def extract_notion_links(text):
        # Define the regex pattern to match links with the format "www.notion.so/"
        pattern = r'(www\.notion\.so\/[^\s\)|\|]+)'
        
        # Find all matches in the text
        matches = re.findall(pattern, text)
        
        # Extract the part of the link following "www.notion.so/"
        extracted_links = [link.split("www.notion.so/")[-1].rstrip(')|\n') for link in matches]
        print(extracted_links)
        return extracted_links

    for page_id, page_content in exported_pages.items():
        
        try:
            title = get_page_title(page_id)
        except:
            title = "NF: " + page_id
        
        file_path = title + ".md"
        
        save_string_to_file(file_path, page_content)
        
                
                
    current_dir = os.getcwd()
    print(current_dir)

    def replace_match(match):
        key = match.group(1)
        print("Match", match.group(0).split("/")[1].title)
        try:
            result = get_page_title(match.group(0).split("/")[1])#search_query_results[match.group(0).split("/")[1]].title
        except:
            result = "Not Found"
        return "This is a link to the subpage: " + result



    def write_lines_to_file(file_path, lines):
        try:
            with open(file_path, 'w') as file:
                for line in lines:
                    file.write(line + '\n')
            print("Lines have been written to the file successfully.")
        except IOError:
            print("An error occurred while writing to the file.")
            
            
            
    new_lines = []
    pattern = r'(www\.)?notion\.so/([^)\|\n\s,]+)'
    # Loop through each file in the directory

    for filename in os.listdir(current_dir):
        
        if filename.endswith(".md"):
            new_lines = []
            file_path = os.path.join(current_dir, filename)
            with open(file_path, "r+", encoding="utf-8") as file:
                
                lines = file.readlines()
                
                
                for line in lines:
                    line = re.sub(pattern, replace_match, line)
                    #print("The line would be changed to:", line)
                    new_lines.append(line)
                    
                    
                # Go back to the beginning of the file and write the updated content
                write_lines_to_file(file_path, new_lines)     
                
                
                # Truncate the remaining content if the updated content is shorter
                file.truncate()
                

    # Create a folder named "markdown" if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        
    # Get a list of all files in the current directory
    files = os.listdir()

    # Move .md files to the "markdown" folder
    for file in files:
        if file.endswith(".md"):
            shutil.move(file, os.path.join(folder_name, file))
            print(f"Moved {file} to {folder_name}")

    file_paths = [os.path.join(folder_name, file) for file in os.listdir(folder_name) if file.endswith(".md") and not file.startswith(".md")]
    print(file_paths)
    open_ai_wrapper.upload_files(vector_store_id, file_paths)
    
        
