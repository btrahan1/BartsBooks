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

// Initialize
async function init() {
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
        
        // Populate selector
        bookSelector.innerHTML = '';
        booksData.forEach(book => {
            const option = document.createElement('option');
            option.value = book.id;
            option.textContent = book.title;
            bookSelector.appendChild(option);
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
    });

    // Theme Toggle
    themeDarkBtn.addEventListener('click', () => {
        document.body.classList.remove('light-theme');
        document.body.classList.add('dark-theme');
        themeDarkBtn.classList.add('active');
        themeLightBtn.classList.remove('active');
    });

    themeLightBtn.addEventListener('click', () => {
        document.body.classList.remove('dark-theme');
        document.body.classList.add('light-theme');
        themeLightBtn.classList.add('active');
        themeDarkBtn.classList.remove('active');
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

// Run
document.addEventListener('DOMContentLoaded', init);
