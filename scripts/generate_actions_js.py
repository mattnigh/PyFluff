#!/usr/bin/env python3
"""
Generate actions.js from actionlist.md
Parses the markdown file and creates a JavaScript array of all Furby actions
"""

import re
import json
from pathlib import Path

def parse_actionlist(md_file: Path) -> list[dict]:
    """Parse actionlist.md and extract all actions"""
    actions = []
    current_category = "Unknown"
    
    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check for category headers (## format)
        if line.startswith('##'):
            # Extract category name, removing the "##" and cleaning up
            category = line[2:].strip()
            # Remove markdown anchors
            category = re.sub(r'\s*\{#.*?\}\s*$', '', category)
            # Remove leading numbers (both single "71 -" and ranges "1-6 -")
            category = re.sub(r'^\d+(-\d+)?\s*-\s*', '', category)
            current_category = category.strip()
            i += 1
            continue
        
        # Check for table rows with action data
        # Format: |71 | 0 | 0 | 0 | "Do" |
        table_match = re.match(r'\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.+?)\s*\|', line)
        if table_match:
            input_val, index, subindex, specific, description = table_match.groups()
            
            # Clean up description - remove quotes and extra whitespace
            description = description.strip()
            if description.startswith('"') and description.endswith('"'):
                description = description[1:-1]
            
            actions.append({
                'input': int(input_val),
                'index': int(index),
                'subindex': int(subindex),
                'specific': int(specific),
                'category': current_category,
                'description': description
            })
        
        i += 1
    
    return actions

def generate_js_file(actions: list[dict], output_file: Path):
    """Generate the actions.js file"""
    
    # Start of the file
    js_content = """// Furby Connect Action Database and Helper
// This file is auto-generated from docs/actionlist.md
// DO NOT EDIT MANUALLY - Run scripts/generate_actions_js.py to regenerate

const FURBY_ACTIONS = [
"""
    
    # Add each action
    for action in actions:
        # Escape quotes in description
        desc = action['description'].replace("'", "\\'").replace('"', '\\"')
        js_content += f"    {{ input: {action['input']}, index: {action['index']}, subindex: {action['subindex']}, specific: {action['specific']}, category: \"{action['category']}\", description: \"{desc}\" }},\n"
    
    # Add quick actions that might not be in the list
    quick_actions = [
        {'input': 55, 'index': 2, 'subindex': 14, 'specific': 0, 'category': 'Quick Actions', 'description': 'Giggle'},
        {'input': 56, 'index': 3, 'subindex': 15, 'specific': 1, 'category': 'Quick Actions', 'description': 'Puke'},
    ]
    
    for action in quick_actions:
        # Check if action already exists
        exists = any(
            a['input'] == action['input'] and 
            a['index'] == action['index'] and 
            a['subindex'] == action['subindex'] and 
            a['specific'] == action['specific'] 
            for a in actions
        )
        if not exists:
            desc = action['description'].replace("'", "\\'").replace('"', '\\"')
            js_content += f"    {{ input: {action['input']}, index: {action['index']}, subindex: {action['subindex']}, specific: {action['specific']}, category: \"{action['category']}\", description: \"{desc}\" }},\n"
    
    # Close the array
    js_content += """];

// Cookie helpers
function setCookie(name, value, days = 365) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    const expires = "expires=" + date.toUTCString();
    document.cookie = name + "=" + JSON.stringify(value) + ";" + expires + ";path=/";
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) {
            try {
                return JSON.parse(c.substring(nameEQ.length, c.length));
            } catch (e) {
                return null;
            }
        }
    }
    return null;
}

// Recent actions management
class RecentActions {
    constructor() {
        this.maxRecent = 10;
        this.recent = getCookie('furby_recent_actions') || [];
    }
    
    add(action) {
        // Create a unique key for the action
        const key = `${action.input},${action.index},${action.subindex},${action.specific}`;
        
        // Remove if already exists
        this.recent = this.recent.filter(a => 
            `${a.input},${a.index},${a.subindex},${a.specific}` !== key
        );
        
        // Add to front
        this.recent.unshift(action);
        
        // Keep only max recent
        if (this.recent.length > this.maxRecent) {
            this.recent = this.recent.slice(0, this.maxRecent);
        }
        
        // Save to cookie
        setCookie('furby_recent_actions', this.recent);
    }
    
    get() {
        return this.recent;
    }
}

const recentActions = new RecentActions();

// Action search and display
function initActionHelper() {
    const searchInput = document.getElementById('action-search');
    const dropdown = document.getElementById('action-dropdown');
    const recentActionsDiv = document.getElementById('recent-actions');
    const actionListDiv = document.getElementById('action-list');
    
    const inputField = document.getElementById('action-input');
    const indexField = document.getElementById('action-index');
    const subindexField = document.getElementById('action-subindex');
    const specificField = document.getElementById('action-specific');
    const descriptionDiv = document.getElementById('action-description');
    
    // Show dropdown on focus
    searchInput.addEventListener('focus', () => {
        updateDropdown('');
        dropdown.classList.remove('hidden');
    });
    
    // Hide dropdown on click outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.action-helper')) {
            dropdown.classList.add('hidden');
        }
    });
    
    // Search as you type
    searchInput.addEventListener('input', (e) => {
        updateDropdown(e.target.value);
    });
    
    function updateDropdown(searchTerm) {
        const term = searchTerm.toLowerCase();
        
        // Recent actions
        const recent = recentActions.get();
        if (recent.length > 0) {
            recentActionsDiv.innerHTML = '<div class="recent-actions-header">Recent Actions</div>';
            recent.forEach(action => {
                recentActionsDiv.appendChild(createActionItem(action, term));
            });
        } else {
            recentActionsDiv.innerHTML = '';
        }
        
        // Filtered actions - search in both category and description
        const filtered = FURBY_ACTIONS.filter(action => {
            if (!term) return true;
            
            // Search in category (case-insensitive)
            const categoryMatch = action.category.toLowerCase().includes(term);
            
            // Search in description (case-insensitive)
            const descriptionMatch = action.description.toLowerCase().includes(term);
            
            // Search in coordinates (for advanced users)
            const coordMatch = `${action.input} ${action.index} ${action.subindex} ${action.specific}`.includes(term);
            
            return categoryMatch || descriptionMatch || coordMatch;
        });
        
        actionListDiv.innerHTML = '';
        filtered.slice(0, 50).forEach(action => { // Limit to 50 results
            actionListDiv.appendChild(createActionItem(action, term));
        });
        
        if (filtered.length === 0) {
            actionListDiv.innerHTML = '<div class="action-item">No actions found</div>';
        }
    }
    
    function createActionItem(action, highlightTerm = '') {
        const item = document.createElement('div');
        item.className = 'action-item';
        
        const title = document.createElement('div');
        title.className = 'action-item-title';
        title.textContent = action.category;
        
        const coords = document.createElement('div');
        coords.className = 'action-item-coords';
        coords.textContent = `[${action.input}, ${action.index}, ${action.subindex}, ${action.specific}]`;
        
        const desc = document.createElement('div');
        desc.className = 'action-item-description';
        // Highlight search term in description if present
        if (highlightTerm && action.description.toLowerCase().includes(highlightTerm.toLowerCase())) {
            const regex = new RegExp(`(${highlightTerm})`, 'gi');
            desc.innerHTML = action.description.replace(regex, '<strong>$1</strong>');
        } else if (highlightTerm && action.category.toLowerCase().includes(highlightTerm.toLowerCase())) {
            desc.textContent = action.description;
        } else {
            desc.textContent = action.description;
        }
        
        item.appendChild(title);
        item.appendChild(coords);
        item.appendChild(desc);
        
        item.addEventListener('click', () => {
            inputField.value = action.input;
            indexField.value = action.index;
            subindexField.value = action.subindex;
            specificField.value = action.specific;
            updateDescription();
            searchInput.value = '';
            dropdown.classList.add('hidden');
            
            // Add to recent
            recentActions.add(action);
        });
        
        return item;
    }
    
    // Update description when fields change
    function updateDescription() {
        const input = parseInt(inputField.value);
        const index = parseInt(indexField.value);
        const subindex = parseInt(subindexField.value);
        const specific = parseInt(specificField.value);
        
        const action = FURBY_ACTIONS.find(a => 
            a.input === input && 
            a.index === index && 
            a.subindex === subindex && 
            a.specific === specific
        );
        
        if (action) {
            descriptionDiv.innerHTML = `<strong>${action.category}:</strong> ${action.description}<br><small>Action: [${input},${index},${subindex},${specific}]</small>`;
        } else {
            descriptionDiv.innerHTML = `<strong>Custom Action:</strong> [${input},${index},${subindex},${specific}]`;
        }
    }
    
    [inputField, indexField, subindexField, specificField].forEach(field => {
        field.addEventListener('input', updateDescription);
        field.addEventListener('change', updateDescription);
    });
    
    // Initial description
    updateDescription();
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initActionHelper);
} else {
    initActionHelper();
}
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)

def main():
    # Get paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    actionlist_file = project_root / 'docs' / 'actionlist.md'
    output_file = project_root / 'web' / 'actions.js'
    
    print(f"Parsing {actionlist_file}...")
    actions = parse_actionlist(actionlist_file)
    print(f"Found {len(actions)} actions")
    
    print(f"Generating {output_file}...")
    generate_js_file(actions, output_file)
    print("Done!")
    
    # Show some stats
    categories = {}
    for action in actions:
        cat = action['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\nActions by category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    main()
