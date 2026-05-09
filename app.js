// State Management
let booksData = [];
let currentBook = '';
let currentChapter = 1;
let totalChapters = 1;
let currentFontSize = 18;

// DOM Elements
const sidebar = document.getElementById('sidebar');
const openSidebarBtn = document.getElementById('open-sidebar');
const closeSidebarBtn = document.getElementById('close-sidebar');
const readerOutput = document.getElementById('reader-output');
const chapterList = document.getElementById('chapter-list');
const bookTitleEl = document.getElementById('book-title');
const chapterTitleEl = document.getElementById('chapter-title');
const prevBtn = document.getElementById('prev-chapter');
const nextBtn = document.getElementById('next-chapter');
const progressIndicator = document.getElementById('progress-indicator');
const fontSizeSlider = document.getElementById('font-size');
const themeDarkBtn = document.getElementById('theme-dark');
const themeLightBtn = document.getElementById('theme-light');
const bookSelector = document.getElementById('book-selector');
const viewLibraryBtn = document.getElementById('view-library');
const viewAdminBtn = document.getElementById('view-admin');
const readerView = document.getElementById('reader-view');
const libraryView = document.getElementById('library-view');
const adminView = document.getElementById('admin-view');
const libraryGrid = document.getElementById('library-grid');
const adminBookSelector = document.getElementById('admin-book-selector');
const formatKindleBtn = document.getElementById('format-kindle-btn');
const adminMessage = document.getElementById('admin-message');

// Initialize
async function init() {
    // Load settings from localStorage
    const savedFontSize = localStorage.getItem('fontSize');
    if (savedFontSize) {
        currentFontSize = parseInt(savedFontSize);
        fontSizeSlider.value = currentFontSize;
    }
    
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.remove('light-theme');
        document.body.classList.add('dark-theme');
        themeDarkBtn.classList.add('active');
        themeLightBtn.classList.remove('active');
    } else if (savedTheme === 'light') {
        document.body.classList.remove('dark-theme');
        document.body.classList.add('light-theme');
        themeLightBtn.classList.add('active');
        themeDarkBtn.classList.remove('active');
    }

    if (typeof marked !== 'undefined') {
        marked.setOptions({
            xhtml: true
        });
    }

    setupEventListeners();
    await loadBooksManifest();
    updateUI();
}

// Load Books Manifest
async function loadBooksManifest() {
    try {
        const response = await fetch('books.json');
        if (!response.ok) throw new Error('Failed to load books manifest');
        booksData = await response.json();
        
        // Sort alphabetically by title
        booksData.sort((a, b) => a.title.localeCompare(b.title));
        
        // Populate selector
        bookSelector.innerHTML = '';
        adminBookSelector.innerHTML = '';
        booksData.forEach(book => {
            const option = document.createElement('option');
            option.value = book.id;
            option.textContent = book.title;
            bookSelector.appendChild(option);
            
            const adminOption = option.cloneNode(true);
            adminBookSelector.appendChild(adminOption);
        });
        
        // Set default book
        if (booksData.length > 0) {
            currentBook = booksData[0].id;
            totalChapters = booksData[0].chapters;
            bookTitleEl.textContent = booksData[0].title;
            
            generateChapterList();
            loadChapter(1);
        }
        
    } catch (error) {
        console.error(error);
        readerOutput.innerHTML = `<p class="error">Failed to load library: ${error.message}</p>`;
    }
}

// Event Listeners
function setupEventListeners() {
    // Sidebar Toggle
    openSidebarBtn.addEventListener('click', () => sidebar.classList.add('open'));
    closeSidebarBtn.addEventListener('click', () => sidebar.classList.remove('open'));

    // Library Toggle
    viewLibraryBtn.addEventListener('click', () => {
        toggleLibraryView();
    });

    // Admin Toggle
    viewAdminBtn.addEventListener('click', () => {
        toggleAdminView();
    });

    // Format Kindle
    formatKindleBtn.addEventListener('click', () => {
        formatForKindle();
    });

    // Navigation
    prevBtn.addEventListener('click', () => {
        if (currentChapter > 1) {
            loadChapter(currentChapter - 1);
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentChapter < totalChapters) {
            loadChapter(currentChapter + 1);
        }
    });

    // Font Size
    fontSizeSlider.addEventListener('input', (e) => {
        currentFontSize = e.target.value;
        document.documentElement.style.fontSize = `${currentFontSize}px`;
        localStorage.setItem('fontSize', currentFontSize);
    });

    // Theme Toggle
    themeDarkBtn.addEventListener('click', () => {
        document.body.classList.remove('light-theme');
        document.body.classList.add('dark-theme');
        themeDarkBtn.classList.add('active');
        themeLightBtn.classList.remove('active');
        localStorage.setItem('theme', 'dark');
    });

    themeLightBtn.addEventListener('click', () => {
        document.body.classList.remove('dark-theme');
        document.body.classList.add('light-theme');
        themeLightBtn.classList.add('active');
        themeDarkBtn.classList.remove('active');
        localStorage.setItem('theme', 'light');
    });

    // Book Selector
    bookSelector.addEventListener('change', (e) => {
        currentBook = e.target.value;
        const selectedBook = booksData.find(b => b.id === currentBook);
        totalChapters = selectedBook.chapters;
        
        bookTitleEl.textContent = selectedBook.title;
        
        generateChapterList();
        loadChapter(1);
    });
}

// Helper to get read chapters from localStorage
function getReadChapters() {
    const read = localStorage.getItem(`read_${currentBook}`);
    return read ? JSON.parse(read) : [];
}

// Helper to mark a chapter as read
function markAsRead(chapterNum) {
    let read = getReadChapters();
    if (!read.includes(chapterNum)) {
        read.push(chapterNum);
        localStorage.setItem(`read_${currentBook}`, JSON.stringify(read));
        generateChapterList(); // Refresh list to show checkmark
    }
}

// Generate Chapter List in Sidebar
function generateChapterList() {
    chapterList.innerHTML = '';
    const readChapters = getReadChapters();
    
    for (let i = 1; i <= totalChapters; i++) {
        const li = document.createElement('li');
        li.textContent = `Chapter ${i}`;
        if (readChapters.includes(i)) {
            li.textContent += ' ✓';
            li.classList.add('read');
        }
        li.dataset.chapter = i;
        if (i === currentChapter) li.classList.add('active');
        
        li.addEventListener('click', () => {
            loadChapter(i);
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('open');
            }
        });
        
        chapterList.appendChild(li);
    }
}

// Load Chapter Content
async function loadChapter(chapterNum) {
    currentChapter = chapterNum;
    
    // Update Sidebar Active State
    const items = chapterList.querySelectorAll('li');
    items.forEach(item => {
        item.classList.remove('active');
        if (parseInt(item.dataset.chapter) === chapterNum) {
            item.classList.add('active');
        }
    });

    // Update Header and Footer
    chapterTitleEl.textContent = `Chapter ${chapterNum}`;
    progressIndicator.textContent = `${chapterNum} / ${totalChapters}`;
    
    // Disable/Enable buttons
    prevBtn.disabled = chapterNum === 1;
    nextBtn.disabled = chapterNum === totalChapters;

    // Show Loading
    readerOutput.innerHTML = '<p class="loading">Loading chapter content...</p>';

    // Fetch and Render
    try {
        const paddedNum = chapterNum.toString().padStart(2, '0');
        const url = `books/${currentBook}/chapter_${paddedNum}.md`;
        
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Failed to load chapter: ${response.statusText}`);
        
        const markdown = await response.text();
        
        if (typeof marked !== 'undefined') {
            readerOutput.innerHTML = marked.parse(markdown);
        } else {
            readerOutput.innerHTML = `<pre>${markdown}</pre>`;
        }
        
        // Mark as read after successful load
        markAsRead(chapterNum);
        
        // Scroll to top
        document.querySelector('.reader-container').scrollTop = 0;
        
    } catch (error) {
        console.error(error);
        readerOutput.innerHTML = `
            <div class="error-message">
                <h3>Oops! Could not load the chapter.</h3>
                <p>${error.message}</p>
                <p>Make sure the file exists at <code>books/${currentBook}/chapter_${chapterNum.toString().padStart(2, '0')}.md</code></p>
            </div>
        `;
    }
}

// Update UI state (font size, etc.)
function updateUI() {
    document.documentElement.style.fontSize = `${currentFontSize}px`;
}

// Toggle Library View
function toggleLibraryView() {
    if (libraryView.classList.contains('hidden')) {
        libraryView.classList.remove('hidden');
        readerView.classList.add('hidden');
        adminView.classList.add('hidden');
        viewLibraryBtn.textContent = '📖 Reader';
        viewAdminBtn.textContent = '⚙️ Admin';
        renderLibrary();
    } else {
        libraryView.classList.add('hidden');
        readerView.classList.remove('hidden');
        viewLibraryBtn.textContent = '📚 Library';
    }
}

// Toggle Admin View
function toggleAdminView() {
    if (adminView.classList.contains('hidden')) {
        adminView.classList.remove('hidden');
        readerView.classList.add('hidden');
        libraryView.classList.add('hidden');
        viewAdminBtn.textContent = '📖 Reader';
        viewLibraryBtn.textContent = '📚 Library';
    } else {
        adminView.classList.add('hidden');
        readerView.classList.remove('hidden');
        viewAdminBtn.textContent = '⚙️ Admin';
    }
}

// Format For Kindle (EPUB Generation)
async function formatForKindle() {
    const bookId = adminBookSelector.value;
    const book = booksData.find(b => b.id === bookId);
    
    if (!book) {
        adminMessage.innerHTML = '<p class="error">Book not found.</p>';
        return;
    }
    
    adminMessage.innerHTML = '<p class="loading">Generating EPUB... 0%</p>';
    formatKindleBtn.disabled = true;
    
    try {
        const zip = new JSZip();
        
        // 1. mimetype (MUST be first and uncompressed)
        zip.file("mimetype", "application/epub+zip", { compression: "STORE" });
        
        // 2. META-INF/container.xml
        const containerXml = `<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>`;
        zip.folder("META-INF").file("container.xml", containerXml);
        
        // 3. OEBPS files
        const oebps = zip.folder("OEBPS");
        
        // Check if cover exists
        let hasCover = false;
        try {
            const coverResponse = await fetch(`books/${bookId}/cover.jpg`);
            if (coverResponse.ok) {
                const coverBlob = await coverResponse.blob();
                oebps.file("cover.jpg", coverBlob);
                hasCover = true;
            }
        } catch (e) {
            console.log("No cover.jpg found or failed to fetch.");
        }
        
        // Generate UUID for book
        const bookUuid = uuidv4();
        
        // Start OPF (Manifest)
        let opfContent = `<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>${book.title}</dc:title>
    <dc:creator>Bart Trahan</dc:creator>
    <dc:identifier id="bookid">urn:uuid:${bookUuid}</dc:identifier>
    <dc:language>en</dc:language>
`;
        if (hasCover) {
            opfContent += `    <meta name="cover" content="cover-image" />\n`;
        }
        opfContent += `  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
`;
        
        let spineContent = `  <spine toc="ncx">\n`;
        
        let ncxContent = `<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD NCX 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:uuid:${bookUuid}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>${book.title}</text></docTitle>
  <navMap>
`;
        
        let playOrder = 1;
        
        if (hasCover) {
            // Add cover.html
            const coverHtml = `<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>Cover</title></head>
<body style="text-align: center; margin: 0; padding: 0;">
  <img src="cover.jpg" alt="Cover" style="max-width: 100%; height: auto;" />
</body>
</html>`;
            oebps.file("cover.html", coverHtml);
            
            opfContent += `    <item id="cover" href="cover.html" media-type="application/xhtml+xml"/>\n`;
            opfContent += `    <item id="cover-image" href="cover.jpg" media-type="image/jpeg"/>\n`;
            
            spineContent += `    <itemref idref="cover" />\n`;
            
            ncxContent += `    <navPoint id="navPoint-0" playOrder="${playOrder++}">
      <navLabel><text>Cover</text></navLabel>
      <content src="cover.html"/>
    </navPoint>\n`;
        }
        
        // Loop through chapters
        for (let i = 1; i <= book.chapters; i++) {
            const percent = Math.round((i / book.chapters) * 100);
            adminMessage.innerHTML = `<p class="loading">Processing chapters... ${percent}%</p>`;
            
            const paddedNum = i.toString().padStart(2, '0');
            const url = `books/${bookId}/chapter_${paddedNum}.md`;
            
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Failed to load chapter ${i}`);
            
            const markdown = await response.text();
            let html = '';
            
            if (typeof marked !== 'undefined') {
                html = marked.parse(markdown);
                // Force self-closing tags for XHTML compliance
                html = html.replace(/<hr>/g, '<hr />');
                html = html.replace(/<br>/g, '<br />');
            } else {
                html = `<pre>${markdown}</pre>`;
            }
            
            const chapterHtml = `<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Chapter ${i}</title>
  <style>
    body { font-family: serif; line-height: 1.6; margin: 1em; }
    h1 { text-align: center; color: #3b82f6; }
  </style>
</head>
<body>
  <h1>Chapter ${i}</h1>
  ${html}
</body>
</html>`;
            
            const fileName = `chapter_${paddedNum}.html`;
            oebps.file(fileName, chapterHtml);
            
            opfContent += `    <item id="chapter_${i}" href="${fileName}" media-type="application/xhtml+xml"/>\n`;
            spineContent += `    <itemref idref="chapter_${i}" />\n`;
            
            ncxContent += `    <navPoint id="navPoint-${i}" playOrder="${playOrder++}">
      <navLabel><text>Chapter ${i}</text></navLabel>
      <content src="${fileName}"/>
    </navPoint>\n`;
        }
        
        // Close manifest, spine, ncx
        opfContent += `  </manifest>\n${spineContent}  </spine>\n</package>`;
        ncxContent += `  </navMap>\n</ncx>`;
        
        oebps.file("content.opf", opfContent);
        oebps.file("toc.ncx", ncxContent);
        
        adminMessage.innerHTML = '<p class="loading">Zipping files...</p>';
        
        const content = await zip.generateAsync({ type: "blob" });
        
        adminMessage.innerHTML = '<p class="success">Generation complete! Downloading...</p>';
        
        // Trigger download
        const url = URL.createObjectURL(content);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${book.title}.epub`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
    } catch (error) {
        console.error(error);
        adminMessage.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    } finally {
        formatKindleBtn.disabled = false;
    }
}

// Helper to generate UUID
function uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Render Library Grid
function renderLibrary() {
    libraryGrid.innerHTML = '';
    
    booksData.forEach(book => {
        const card = document.createElement('div');
        card.className = 'book-card';
        
        const title = document.createElement('h3');
        title.textContent = book.title;
        
        const synopsis = document.createElement('p');
        synopsis.textContent = book.synopsis || 'No synopsis available.';
        
        const footer = document.createElement('div');
        footer.className = 'card-footer';
        
        const count = document.createElement('span');
        count.className = 'chapter-count';
        count.textContent = `${book.chapters} Chapters`;
        
        const readBtn = document.createElement('button');
        readBtn.className = 'nav-btn';
        readBtn.textContent = 'Read';
        readBtn.addEventListener('click', () => {
            selectBook(book.id);
        });
        
        footer.appendChild(count);
        footer.appendChild(readBtn);
        
        card.appendChild(title);
        card.appendChild(synopsis);
        card.appendChild(footer);
        
        libraryGrid.appendChild(card);
    });
}

// Helper to select a book from library
function selectBook(bookId) {
    currentBook = bookId;
    bookSelector.value = bookId;
    
    const selectedBook = booksData.find(b => b.id === currentBook);
    totalChapters = selectedBook.chapters;
    
    bookTitleEl.textContent = selectedBook.title;
    
    generateChapterList();
    loadChapter(1);
    
    // Switch back to reader view
    libraryView.classList.add('hidden');
    readerView.classList.remove('hidden');
    viewLibraryBtn.textContent = '📚 Library';
}

// Run
document.addEventListener('DOMContentLoaded', init);
