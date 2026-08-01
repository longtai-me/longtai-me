document.addEventListener('DOMContentLoaded', () => {
    const blogListContainer = document.getElementById('blog-list');
    const blogPostContainer = document.getElementById('blog-post');
    const blogContainer = document.getElementById('blog-container');
    const postContent = document.getElementById('post-content');
    const searchInput = document.getElementById('blog-search');
    const backBtn = document.getElementById('back-btn');

    let allBlogs = [];

    // Check URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const postFile = urlParams.get('post');

    if (postFile) {
        loadPost(postFile);
    } else {
        loadBlogList();
    }

    backBtn.addEventListener('click', () => {
        // Remove 'post' param from URL and go back to list
        const url = new URL(window.location);
        url.searchParams.delete('post');
        window.history.pushState({}, '', url);
        
        blogPostContainer.style.display = 'none';
        blogContainer.style.display = 'block';
        if (allBlogs.length === 0) {
            loadBlogList();
        }
    });

    async function loadBlogList() {
        try {
            const response = await fetch('/public/json/blogs.json', { cache: 'no-cache' });
            if (!response.ok) throw new Error('Cannot fetch blogs.json');
            
            allBlogs = await response.json();
            renderBlogList(allBlogs);
        } catch (error) {
            blogListContainer.innerHTML = '<p>目前沒有文章或發生錯誤。</p>';
            console.error(error);
        }
    }

    function renderBlogList(blogs) {
        blogListContainer.innerHTML = '';
        
        if (blogs.length === 0) {
            blogListContainer.innerHTML = '<p>找不到相符的文章。</p>';
            return;
        }

        blogs.forEach(blog => {
            const card = document.createElement('div');
            card.className = 'blog-card card'; // reusing global card styles
            
            const title = document.createElement('h3');
            title.textContent = blog.title;
            
            // Generate a short preview from index_content or standard text
            const previewText = blog.index_content 
                ? blog.index_content.substring(0, 100) + '...'
                : '閱讀更多...';
                
            const preview = document.createElement('p');
            preview.textContent = previewText;
            
            const link = document.createElement('div');
            link.className = 'read-more';
            link.textContent = '閱讀文章';
            
            card.appendChild(title);
            card.appendChild(preview);
            card.appendChild(link);
            
            // Make the whole card clickable
            card.addEventListener('click', () => {
                window.location.href = `?post=${encodeURIComponent(blog.id)}`;
            });
            card.style.cursor = 'pointer';
            
            blogListContainer.appendChild(card);
        });
    }

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        if (!query) {
            renderBlogList(allBlogs);
            return;
        }
        
        const filtered = allBlogs.filter(blog => {
            const titleMatch = blog.title.toLowerCase().includes(query);
            const contentMatch = (blog.index_content || '').toLowerCase().includes(query);
            return titleMatch || contentMatch;
        });
        
        renderBlogList(filtered);
    });

    async function loadPost(postId) {
        blogContainer.style.display = 'none';
        blogPostContainer.style.display = 'block';
        postContent.innerHTML = '<p>載入文章中...</p>';
        
        try {
            const response = await fetch(`/public/blogs/${postId}.md`, { cache: 'no-cache' });
            if (!response.ok) {
                if (response.status === 404) {
                    throw new Error('找不到該文章。');
                }
                throw new Error('無法載入文章。');
            }
            
            const text = await response.text();
            
            // Set marked options if needed (e.g. allow HTML)
            // By default marked.js allows HTML.
            
            // Parse Markdown to HTML
            const html = marked.parse(text);
            postContent.innerHTML = `<h1>${postId}</h1>\n${html}`;
            
            // Add copy buttons to code blocks
            const codeBlocks = postContent.querySelectorAll('pre');
            codeBlocks.forEach((pre) => {
                const code = pre.querySelector('code');
                if (!code) return;
                
                // Ensure pre is relatively positioned for the absolute button
                pre.style.position = 'relative';
                
                const copyBtn = document.createElement('button');
                copyBtn.className = 'copy-code-btn';
                copyBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zm2-1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1zM2 5a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1v-1h1v1a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h1v1z"/></svg>';
                copyBtn.title = '複製程式碼';
                
                copyBtn.addEventListener('click', async () => {
                    try {
                        await navigator.clipboard.writeText(code.innerText);
                        
                        // Show success state
                        const originalHtml = copyBtn.innerHTML;
                        copyBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"/></svg>';
                        copyBtn.classList.add('copied');
                        
                        setTimeout(() => {
                            copyBtn.innerHTML = originalHtml;
                            copyBtn.classList.remove('copied');
                        }, 2000);
                    } catch (err) {
                        console.error('Failed to copy text: ', err);
                    }
                });
                
                pre.appendChild(copyBtn);
            });
            
            // Update document title
            document.title = `${postId} | Blog`;
            
        } catch (error) {
            postContent.innerHTML = `<p>${error.message}</p>`;
        }
    }
});
