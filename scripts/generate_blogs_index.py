import os
import json
import re

def generate_index():
    blogs_dir = 'public/blogs'
    output_file = 'public/json/blogs.json'
    
    if not os.path.exists(blogs_dir):
        print(f"Directory {blogs_dir} does not exist.")
        return
        
    blogs = []
    
    for filename in os.listdir(blogs_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(blogs_dir, filename)
            
            # The title is the filename without extension
            title = os.path.splitext(filename)[0]
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract index content from HTML comments <!-- ... -->
            # Using re.DOTALL to match across newlines if any
            comments = re.findall(r'<!--(.*?)-->', content, re.DOTALL)
            
            # Join all comments to serve as the searchable index string
            index_content = ' '.join(c.strip() for c in comments)
            
            blogs.append({
                'id': title,
                'title': title,
                'filename': filename,
                'index_content': index_content
            })
            
    # Write to blogs.json
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(blogs, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated index for {len(blogs)} blogs.")

if __name__ == "__main__":
    generate_index()
