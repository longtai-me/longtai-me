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
            const response = await fetch('/public/json/blogs.json');
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
            
            const link = document.createElement('a');
            link.href = `?post=${encodeURIComponent(blog.id)}`;
            link.className = 'btn';
            link.textContent = 'Read';
            link.style.marginTop = '1rem';
            
            card.appendChild(title);
            card.appendChild(preview);
            card.appendChild(link);
            
            // Make the whole card clickable except the button (which handles its own click)
            card.addEventListener('click', (e) => {
                if (e.target.tagName !== 'A') {
                    window.location.href = `?post=${encodeURIComponent(blog.id)}`;
                }
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
            const response = await fetch(`/public/blogs/${postId}.md`);
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
            postContent.innerHTML = html;
            
            // Update document title
            document.title = `${postId} | Blog`;
            
        } catch (error) {
            postContent.innerHTML = `<p>${error.message}</p>`;
        }
    }
});
