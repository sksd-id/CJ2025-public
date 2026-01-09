import DOMPurify from 'https://cdn.skypack.dev/dompurify/';
import showdown from 'https://cdn.skypack.dev/showdown/';
const params = new URLSearchParams(window.location.search);

function main() {
    const converter = new showdown.Converter();
    const noteInput = document.getElementById('noteInput');
    const saveNoteBtn = document.getElementById('saveNote');
    const noteList = document.getElementById('noteList');
    const name = params.get('name');

    
    function loadNotes() {
        let notes = window.notes ? Array.from(window.notes) : JSON.parse(localStorage.notes || '[]');
        noteList.innerHTML = '';

        notes.forEach((note, index) => {
            const sanitizedNote = DOMPurify.sanitize(note);
            const htmlNote = converter.makeHtml(sanitizedNote);
            console.log(htmlNote);
            const noteElement = document.createElement('div');
            noteElement.className = 'note-item';
            noteElement.innerHTML = `
                ${htmlNote}
                <span class="delete-btn" data-index="${parseInt(index)}">x</span>
            `;
            noteList.appendChild(noteElement);
        });

        // Add delete functionality
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const index = parseInt(e.target.getAttribute('data-index'));
                deleteNote(index);
            });
        });
    }

    // Save a new note
    function saveNote() {
        const noteText = noteInput.value.trim();
        if (!noteText) return;

        const notes = JSON.parse(localStorage.notes || '[]');
        notes.push(noteText);
        localStorage.setItem('notes', JSON.stringify(notes));
        
        noteInput.value = ''; 
        loadNotes(); 
    }

    // Delete a note
    function deleteNote(index) {
        const notes = JSON.parse(localStorage.notes || '[]');
        notes.splice(index, 1);
        localStorage.setItem('notes', JSON.stringify(notes));
        loadNotes();
    }

    // Event listeners
    saveNoteBtn.addEventListener('click', saveNote);
    noteInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            saveNote();
        }
    });

    if (name) {
        localStorage.setItem('name', name);
        document.title = `Notes for ${name}`;
        document.querySelector('h1').innerHTML = DOMPurify.sanitize(`Notes for ${name}`);
    } else {
        document.title = `Notes`;
        document.querySelector('h1').innerHTML = DOMPurify.sanitize(`Notes`);
    }

    // Initial load
    loadNotes();
}

main();