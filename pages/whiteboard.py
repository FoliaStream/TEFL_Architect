import streamlit as st
import os 
import yaml 

from src.fe.support_functions import setup_sidebar
from src.fe.styles import HIDE_SIDEBAR_NAV, TEXT_JUSTIFIED
from streamlit.components.v1 import html

# --- PAGE CONFIG --- 
st.set_page_config(page_title="Theory", layout="wide")

# --- STYLES ---
st.markdown(HIDE_SIDEBAR_NAV, unsafe_allow_html=True)
st.markdown(TEXT_JUSTIFIED, unsafe_allow_html=True)

# --- CONFIG ---
with open(f"{os.getcwd()}/src/be/config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# --- SIDEBAR & TITLE ---
selected_page = setup_sidebar(
    pages=config['pages'],
    main_page=config['main_page']
)

# Navigation on click
if selected_page == "HOME":
    st.switch_page("HOME.py")
elif selected_page == "Whiteboard":
    st.title(selected_page)
elif selected_page == "IELTS Preparation":
    st.switch_page("pages/ielts_preparation.py")
elif selected_page == "Lesson Planner":
    st.switch_page("pages/lesson_planner.py")
elif selected_page == "Syllabus Planner":
    st.switch_page("pages/syllabus_planner.py")
elif selected_page == "TEFL Theory":
    st.switch_page("pages/tefl_theory.py")



# Custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        max-width: 100%;
        padding: 0;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0;
    }
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Whiteboard HTML/JavaScript
WHITEBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Whiteboard</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
            font-family: Arial, sans-serif;
            overflow: hidden;
            height: 100vh;
        }
        
        #whiteboard {
            width: 100%;
            height: calc(100vh - 100px);
            background: white;
            border: 2px solid #ddd;
            border-radius: 8px;
            position: relative;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: auto;
        }
        
        .shape {
            position: absolute;
            border: 2px solid #4a90e2;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 8px;
            cursor: move;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            min-width: 100px;
            min-height: 60px;
            resize: both;
            overflow: hidden;
            padding: 8px;
        }
        
        .shape.selected {
            border: 2px solid #ff6b6b;
            box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.3);
        }
        
        .shape:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        
        .shape-text {
            width: 100%;
            height: 100%;
            border: none;
            background: transparent;
            resize: none;
            outline: none;
            font-size: 14px;
            font-family: Arial, sans-serif;
            color: #333;
            padding: 4px;
            box-sizing: border-box;
        }
        
        .connector {
            position: absolute;
            pointer-events: none;
            z-index: -1;
        }
        
        .arrow {
            stroke: #666;
            stroke-width: 2;
            fill: none;
            marker-end: url(#arrowhead);
        }
        
        .arrow-head {
            fill: #666;
        }
        
        .controls {
            position: fixed;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 10px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        button {
            padding: 8px 16px;
            background: #4a90e2;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        
        button:hover {
            background: #357ae8;
        }
        
        select {
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ddd;
            font-size: 14px;
        }
        
        .shape-type-rect {
            border-radius: 8px;
        }
        
        .shape-type-circle {
            border-radius: 50%;
        }
        
        .shape-type-diamond {
            border-radius: 0;
            transform: rotate(45deg);
        }
        
        .shape-type-diamond .shape-text {
            transform: rotate(-45deg);
        }
        
        .delete-btn {
            position: absolute;
            top: -10px;
            right: -10px;
            background: #ff6b6b;
            color: white;
            border: none;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            font-size: 12px;
            cursor: pointer;
            display: none;
        }
        
        .shape:hover .delete-btn {
            display: block;
        }
    </style>
</head>
<body>
    <div class="controls">
        <button onclick="addShape('rectangle')">➕ Rectangle</button>
        <button onclick="addShape('circle')">⭕ Circle</button>
        <button onclick="addShape('diamond')">🔷 Diamond</button>
        <select id="arrowMode" onchange="toggleArrowMode()">
            <option value="off">Connect Shapes</option>
            <option value="on">Arrow Mode: ON</option>
        </select>
        <button onclick="clearAll()">🗑️ Clear All</button>
        <button onclick="saveWhiteboard()">💾 Save</button>
        <button onclick="loadWhiteboard()">📂 Load</button>
    </div>
    
    <div id="whiteboard"></div>
    
    <svg id="connectors" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;">
        <defs>
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" class="arrow-head"/>
            </marker>
        </defs>
    </svg>

    <script>
        let shapes = {};
        let connectors = [];
        let selectedShape = null;
        let isDragging = false;
        let isResizing = false;
        let arrowMode = false;
        let connectionStart = null;
        
        class Shape {
            constructor(id, type, x, y, width = 150, height = 100) {
                this.id = id;
                this.type = type;
                this.x = x;
                this.y = y;
                this.width = width;
                this.height = height;
                this.text = "Double click to edit";
                this.connections = [];
            }
        }
        
        class Connector {
            constructor(id, fromShape, toShape, fromSide = 'right', toSide = 'left') {
                this.id = id;
                this.fromShape = fromShape;
                this.toShape = toShape;
                this.fromSide = fromSide;
                this.toSide = toSide;
                this.selected = false; // Add selection state
            }
        }

        
        function addShape(type) {
            const id = 'shape_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            const whiteboard = document.getElementById('whiteboard');
            const rect = whiteboard.getBoundingClientRect();
            
            // Calculate center position
            const x = rect.width / 2 - 75;
            const y = rect.height / 2 - 50;
            
            const shape = new Shape(id, type, x, y);
            shapes[id] = shape;
            
            renderShape(shape);
            updateConnectors();
        }
        
        function renderShape(shape) {
            const whiteboard = document.getElementById('whiteboard');
            
            // Remove existing element if present
            const existing = document.getElementById(shape.id);
            if (existing) existing.remove();
            
            const shapeDiv = document.createElement('div');
            shapeDiv.id = shape.id;
            shapeDiv.className = `shape shape-type-${shape.type}`;
            shapeDiv.style.left = shape.x + 'px';
            shapeDiv.style.top = shape.y + 'px';
            shapeDiv.style.width = shape.width + 'px';
            shapeDiv.style.height = shape.height + 'px';
            
            // Add text area
            const textArea = document.createElement('textarea');
            textArea.className = 'shape-text';
            textArea.value = shape.text;
            textArea.placeholder = "Type here...";
            
            // FIX: Proper text input handling
            textArea.oninput = function(e) {
                shapes[shape.id].text = e.target.value;
                saveToSession();
            };
            
            // FIX: Prevent textarea from interfering with shape dragging
            textArea.onmousedown = function(e) {
                e.stopPropagation();
            };
            
            // FIX: Better text editing on double-click
            shapeDiv.ondblclick = function(e) {
                if (e.target !== textArea) {
                    textArea.focus();
                    textArea.select();
                }
            };
            
            // Add delete button
            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'delete-btn';
            deleteBtn.innerHTML = '×';
            deleteBtn.onclick = function(e) {
                e.stopPropagation();
                deleteShape(shape.id);
            };
            
            shapeDiv.appendChild(textArea);
            shapeDiv.appendChild(deleteBtn);
            
            // Event listeners for dragging
            shapeDiv.onmousedown = function(e) {
                if (e.target.className === 'delete-btn' || e.target === textArea) return;
                
                if (arrowMode) {
                    handleConnectionStart(shape.id, e);
                } else {
                    startDrag(e, shape.id);
                }
            };
            
            whiteboard.appendChild(shapeDiv);
        }

        
        function startDrag(e, shapeId) {
            e.preventDefault();
            e.stopPropagation();
            
            const shape = shapes[shapeId];
            const shapeEl = document.getElementById(shapeId);
            const startX = e.clientX;
            const startY = e.clientY;
            const startLeft = shape.x;
            const startTop = shape.y;
            
            selectShape(shapeId);
            
            function onMouseMove(e) {
                const dx = e.clientX - startX;
                const dy = e.clientY - startY;
                
                shape.x = startLeft + dx;
                shape.y = startTop + dy;
                
                shapeEl.style.left = shape.x + 'px';
                shapeEl.style.top = shape.y + 'px';
                
                updateConnectors(); // Update arrows in real-time
            }
            
            function onMouseUp() {
                document.removeEventListener('mousemove', onMouseMove);
                document.removeEventListener('mouseup', onMouseUp);
                saveToSession();
            }
            
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        }
        
        function selectShape(shapeId) {
            // Deselect previous
            if (selectedShape) {
                const prevEl = document.getElementById(selectedShape);
                if (prevEl) prevEl.classList.remove('selected');
            }
            
            selectedShape = shapeId;
            const shapeEl = document.getElementById(shapeId);
            if (shapeEl) shapeEl.classList.add('selected');
        }
        
        function deleteShape(shapeId) {
            // Remove all connections involving this shape
            connectors = connectors.filter(conn => 
                conn.fromShape !== shapeId && conn.toShape !== shapeId
            );
            
            // Remove shape
            delete shapes[shapeId];
            const shapeEl = document.getElementById(shapeId);
            if (shapeEl) shapeEl.remove();
            
            updateConnectors();
            saveToSession();
        }
        
        function handleConnectionStart(shapeId, e) {
            e.stopPropagation();
            connectionStart = shapeId;
            selectShape(shapeId);
            
            document.body.style.cursor = 'crosshair';
            
            // Create temporary visual feedback
            const tempLine = document.createElement('div');
            tempLine.style.position = 'fixed';
            tempLine.style.background = '#4a90e2';
            tempLine.style.height = '2px';
            tempLine.style.pointerEvents = 'none';
            tempLine.style.zIndex = '1000';
            document.body.appendChild(tempLine);
            
            const startRect = document.getElementById(shapeId).getBoundingClientRect();
            const startX = startRect.left + startRect.width / 2;
            const startY = startRect.top + startRect.height / 2;
            
            function onMouseMove(e) {
                const currentX = e.clientX;
                const currentY = e.clientY;
                
                // Update temp line
                const dx = currentX - startX;
                const dy = currentY - startY;
                const length = Math.sqrt(dx * dx + dy * dy);
                const angle = Math.atan2(dy, dx) * 180 / Math.PI;
                
                tempLine.style.width = length + 'px';
                tempLine.style.left = startX + 'px';
                tempLine.style.top = startY + 'px';
                tempLine.style.transform = `rotate(${angle}deg)`;
                tempLine.style.transformOrigin = '0 0';
            }
            
            function onMouseUp(e) {
                document.body.style.cursor = 'default';
                document.removeEventListener('mousemove', onMouseMove);
                document.removeEventListener('mouseup', onMouseUp);
                
                // Remove temp line
                if (tempLine.parentNode) {
                    document.body.removeChild(tempLine);
                }
                
                // FIX: Use a more reliable method to find shapes
                // Get ALL shapes and check which one contains the mouse point
                const allShapes = Array.from(document.querySelectorAll('.shape'));
                const targetShape = allShapes.find(shape => {
                    const rect = shape.getBoundingClientRect();
                    return e.clientX >= rect.left && 
                        e.clientX <= rect.right && 
                        e.clientY >= rect.top && 
                        e.clientY <= rect.bottom;
                });
                
                if (targetShape && targetShape.id !== connectionStart && shapes[targetShape.id]) {
                    createConnector(connectionStart, targetShape.id);
                }
                
                connectionStart = null;
            }
            
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp, { once: true });
        }
        
        function createConnector(fromId, toId) {
            const connectorId = 'conn_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            const connector = new Connector(connectorId, fromId, toId);
            connectors.push(connector);
            
            updateConnectors();
            saveToSession();
        }

        
        
        function updateConnectors() {
            const svg = document.getElementById('connectors');
            // Clear existing connectors but keep the marker definition
            const defs = svg.querySelector('defs');
            svg.innerHTML = '';
            if (defs) svg.appendChild(defs);
            
            connectors.forEach(connector => {
                const fromShape = shapes[connector.fromShape];
                const toShape = shapes[connector.toShape];
                
                if (!fromShape || !toShape) return;
                
                // Get shape positions
                const fromRect = getShapeRect(fromShape);
                const toRect = getShapeRect(toShape);
                
                // Calculate start and end points
                const startX = fromRect.x + fromRect.width / 2;
                const startY = fromRect.y + fromRect.height / 2;
                const endX = toRect.x + toRect.width / 2;
                const endY = toRect.y + toRect.height / 2;
                
                // Create a thicker invisible line for clicking (behind the visible line)
                const clickLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                clickLine.setAttribute('class', 'arrow-click-target');
                clickLine.setAttribute('x1', startX);
                clickLine.setAttribute('y1', startY);
                clickLine.setAttribute('x2', endX);
                clickLine.setAttribute('y2', endY);
                clickLine.setAttribute('stroke', 'transparent');
                clickLine.setAttribute('stroke-width', '20'); // Thick for easy clicking
                clickLine.style.cursor = 'pointer';
                
                // Add click event to the invisible line
                clickLine.onclick = function(e) {
                    e.stopPropagation();
                    selectConnector(connector.id);
                };
                
                // Create the visible line
                const visibleLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                visibleLine.setAttribute('class', connector.selected ? 'arrow selected' : 'arrow');
                visibleLine.setAttribute('x1', startX);
                visibleLine.setAttribute('y1', startY);
                visibleLine.setAttribute('x2', endX);
                visibleLine.setAttribute('y2', endY);
                visibleLine.setAttribute('marker-end', connector.selected ? 'url(#arrowhead-selected)' : 'url(#arrowhead)');
                
                svg.appendChild(clickLine);
                svg.appendChild(visibleLine);
                
                // Add delete button if selected
                if (connector.selected) {
                    const midX = (startX + endX) / 2;
                    const midY = (startY + endY) / 2;
                    
                    // Create HTML delete button (not SVG - easier to handle)
                    const deleteBtn = document.createElement('div');
                    deleteBtn.className = 'arrow-delete-btn';
                    deleteBtn.innerHTML = '×';
                    deleteBtn.style.position = 'absolute';
                    deleteBtn.style.left = (midX - 15) + 'px';
                    deleteBtn.style.top = (midY - 15) + 'px';
                    deleteBtn.style.width = '30px';
                    deleteBtn.style.height = '30px';
                    deleteBtn.style.background = '#ff6b6b';
                    deleteBtn.style.color = 'white';
                    deleteBtn.style.borderRadius = '50%';
                    deleteBtn.style.display = 'flex';
                    deleteBtn.style.alignItems = 'center';
                    deleteBtn.style.justifyContent = 'center';
                    deleteBtn.style.cursor = 'pointer';
                    deleteBtn.style.fontSize = '18px';
                    deleteBtn.style.fontWeight = 'bold';
                    deleteBtn.style.border = '2px solid white';
                    deleteBtn.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
                    deleteBtn.style.zIndex = '1000';
                    
                    deleteBtn.onclick = function(e) {
                        e.stopPropagation();
                        e.preventDefault();
                        deleteConnector(connector.id);
                    };
                    
                    deleteBtn.onmouseenter = function() {
                        this.style.background = '#ff4444';
                        this.style.transform = 'scale(1.1)';
                    };
                    
                    deleteBtn.onmouseleave = function() {
                        this.style.background = '#ff6b6b';
                        this.style.transform = 'scale(1)';
                    };
                    
                    // Add to whiteboard container
                    document.getElementById('whiteboard').appendChild(deleteBtn);
                    
                    // Store reference for cleanup
                    if (!window.deleteButtons) window.deleteButtons = {};
                    window.deleteButtons[connector.id] = deleteBtn;
                }
            });
        }


        function selectConnector(connectorId) {
            // Clean up any existing delete buttons
            if (window.deleteButtons) {
                Object.values(window.deleteButtons).forEach(btn => {
                    if (btn && btn.parentNode) {
                        btn.parentNode.removeChild(btn);
                    }
                });
                window.deleteButtons = {};
            }
            
            // Deselect all connectors
            connectors.forEach(conn => conn.selected = false);
            
            // Select the clicked connector
            const connector = connectors.find(c => c.id === connectorId);
            if (connector) {
                connector.selected = true;
                // Deselect any selected shape
                if (selectedShape) {
                    const shapeEl = document.getElementById(selectedShape);
                    if (shapeEl) shapeEl.classList.remove('selected');
                    selectedShape = null;
                }
                updateConnectors();
            }
        }

        const updated_css = `
            .arrow {
                stroke: #666;
                stroke-width: 2;
                fill: none;
                transition: all 0.2s;
            }
            
            .arrow.selected {
                stroke: #ff6b6b;
                stroke-width: 4;
            }
            
            .connector-delete-btn {
                pointer-events: all;
            }
            
            .connector-delete-btn circle {
                transition: all 0.2s;
            }
        `;

        const updated_svg_defs = `
            <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
                </marker>
                <marker id="arrowhead-selected" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                    <polygon points="0 0, 10 3.5, 0 7" fill="#ff6b6b"/>
                </marker>
            </defs>
        `;

        function deleteConnector(connectorId) {
            if (confirm('Delete this connection?')) {
                // Remove delete button if it exists
                if (window.deleteButtons && window.deleteButtons[connectorId]) {
                    const btn = window.deleteButtons[connectorId];
                    if (btn && btn.parentNode) {
                        btn.parentNode.removeChild(btn);
                    }
                    delete window.deleteButtons[connectorId];
                }
                
                // Remove connector from array
                connectors = connectors.filter(conn => conn.id !== connectorId);
                updateConnectors();
                saveToSession();
            }
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Delete' || e.key === 'Backspace') {
                const selectedConnector = connectors.find(c => c.selected);
                if (selectedConnector) {
                    deleteConnector(selectedConnector.id);
                }
            }
            
            // Deselect on Escape
            if (e.key === 'Escape') {
                connectors.forEach(conn => conn.selected = false);
                updateConnectors();
            }
        });


        // Helper function to get shape rectangle
        function getShapeRect(shape) {
            const shapeEl = document.getElementById(shape.id);
            if (shapeEl) {
                const rect = shapeEl.getBoundingClientRect();
                const whiteboard = document.getElementById('whiteboard');
                const boardRect = whiteboard.getBoundingClientRect();
                return {
                    x: rect.left - boardRect.left,
                    y: rect.top - boardRect.top,
                    width: rect.width,
                    height: rect.height
                };
            }
            
            // Fallback to stored position
            return {
                x: shape.x,
                y: shape.y,
                width: shape.width,
                height: shape.height
            };
        }

        
        function toggleArrowMode() {
            const select = document.getElementById('arrowMode');
            arrowMode = select.value === 'on';
            
            if (arrowMode) {
                document.body.style.cursor = 'crosshair';
                document.body.classList.add('arrow-mode');
            } else {
                document.body.style.cursor = 'default';
                document.body.classList.remove('arrow-mode');
            }
        }
        
        function clearAll() {
            if (confirm('Are you sure you want to clear the whiteboard?')) {
                // Clean up delete buttons
                if (window.deleteButtons) {
                    Object.values(window.deleteButtons).forEach(btn => {
                        if (btn && btn.parentNode) {
                            btn.parentNode.removeChild(btn);
                        }
                    });
                    window.deleteButtons = {};
                }
                
                shapes = {};
                connectors = [];
                document.getElementById('whiteboard').innerHTML = '';
                document.getElementById('connectors').innerHTML = '<defs><marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#666"/></marker><marker id="arrowhead-selected" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#ff6b6b"/></marker></defs>';
                saveToSession();
            }
        }

        // Add CSS for the invisible click target:
        
        function saveWhiteboard() {
            const data = {
                shapes: shapes,
                connectors: connectors.map(conn => ({
                    id: conn.id,
                    fromShape: conn.fromShape,
                    toShape: conn.toShape,
                    fromSide: conn.fromSide,
                    toSide: conn.toSide
                }))
            };
            
            const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'whiteboard-' + new Date().toISOString().slice(0,10) + '.json';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
        
        function loadWhiteboard() {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.json';
            
            input.onchange = (e) => {
                const file = e.target.files[0];
                if (!file) return;
                
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        const data = JSON.parse(e.target.result);
                        
                        // Clear existing
                        shapes = {};
                        connectors = data.connectors || [];
                        document.getElementById('whiteboard').innerHTML = '';
                        
                        // Load shapes
                        Object.values(data.shapes || {}).forEach(shapeData => {
                            const shape = new Shape(
                                shapeData.id,
                                shapeData.type,
                                shapeData.x,
                                shapeData.y,
                                shapeData.width,
                                shapeData.height
                            );
                            shape.text = shapeData.text || '';
                            shapes[shape.id] = shape;
                            renderShape(shape);
                        });
                        
                        updateConnectors();
                        saveToSession();
                    } catch (error) {
                        alert('Error loading file: ' + error.message);
                    }
                };
                reader.readAsText(file);
            };
            
            input.click();
        }
        
        function saveToSession() {
            const data = {
                shapes: shapes,
                connectors: connectors
            };
            
            // Send to Streamlit
            window.parent.postMessage({
                type: 'WHITEBOARD_SAVE',
                data: JSON.stringify(data)
            }, '*');
        }
        
        // Initialize with a welcome shape
        window.onload = function() {
            addShape('rectangle');
        };
    </script>
</body>
</html>
"""

def main():
    st.markdown("""
    **Create shapes, add text, and connect them with arrows!**
    - **Add shapes**: Click rectangle, circle, or diamond buttons
    - **Edit text**: Double-click any shape
    - **Move shapes**: Click and drag
    - **Connect shapes**: Enable "Arrow Mode" and drag from one shape to another
    - **Delete shapes**: Click the × button that appears when hovering
    - **Save/Load**: Export your work as JSON or import existing files
    """)
    
    # Initialize session state for whiteboard data
    if 'whiteboard_data' not in st.session_state:
        st.session_state.whiteboard_data = None
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Whiteboard", "Instructions"])
    
    with tab1:
        # Create the whiteboard - FIXED: use html() function directly
        html(
            WHITEBOARD_HTML,
            height=800,
            scrolling=False
        )
        
        # Display saved data
        if st.session_state.whiteboard_data:
            with st.expander("View Whiteboard Data (JSON)"):
                st.json(st.session_state.whiteboard_data)
    
    with tab2:
        st.markdown("""
        ## 📋 Complete User Guide
        
        ### **Basic Operations**
        
        1. **Adding Shapes**
           - Click the rectangle, circle, or diamond buttons in the toolbar
           - New shapes appear in the center of the whiteboard
           - Each shape is draggable and resizable
        
        2. **Editing Text**
           - Double-click any shape to start editing
           - The text area supports multi-line text
           - Click outside the shape to save changes
        
        3. **Moving Shapes**
           - Click and drag any shape to move it
           - Release mouse button to drop
        
        4. **Connecting Shapes**
           - Select "Arrow Mode: ON" from the dropdown
           - Click and drag from one shape to another
           - Arrows automatically connect shape centers
        
        5. **Deleting Shapes**
           - Hover over a shape to see the × button
           - Click × to delete the shape and its connections
        
        ### **Toolbar Functions**
        
        - **➕ Rectangle**: Add rectangular text box
        - **⭕ Circle**: Add circular text box  
        - **🔷 Diamond**: Add diamond-shaped text box
        - **Connect Shapes**: Toggle arrow connection mode
        - **🗑️ Clear All**: Remove all shapes and connections
        - **💾 Save**: Download whiteboard as JSON file
        - **📂 Load**: Import previously saved whiteboard
        
        ### **Tips & Tricks**
        
        - Use different shapes to represent different concepts
        - Connect related ideas with arrows
        - Save frequently to avoid losing work
        - The whiteboard automatically saves to your session
        - You can resize shapes by dragging their edges
        - All connections are maintained when moving shapes
        
        ### **Keyboard Shortcuts**
        
        - **Double-click**: Edit shape text
        - **ESC**: Cancel current operation
        - **Drag**: Move shapes
        - **Hover + ×**: Delete shape
        
        ### **Data Management**
        
        - Whiteboards are saved as JSON files
        - You can share JSON files with others
        - Load previous work anytime
        - Session data persists until browser refresh
        """)

if __name__ == "__main__":
    try:
        from streamlit.components.v1 import html as components
        main()
    except ImportError:
        st.error("Please install streamlit: `pip install streamlit`")
        st.code("pip install streamlit")



    

# if __name__ == "__main__":
#     main()