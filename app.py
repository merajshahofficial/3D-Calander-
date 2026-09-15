import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="3D Calendar App",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default UI components for a clean App feel
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {padding: 0rem !important;}
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Multi-Colored Calendar</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { margin: 0; overflow: hidden; font-family: 'Segoe UI', Roboto, sans-serif; background: #0b0f19; color: #fff; }
        #canvas-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; }
        .glass-panel { background: rgba(18, 24, 38, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.12); box-shadow: 0 20px 50px rgba(0,0,0,0.5); }
        .glow-button { background: linear-gradient(135deg, #6366f1, #a855f7, #ec4899); background-size: 200% 200%; animation: gradientShift 4s ease infinite; }
        @keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
        .calendar-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; }
        .day-card { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .day-card:hover { transform: translateY(-5px) scale(1.02); box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4); }
    </style>
</head>
<body class="flex h-screen w-screen relative">
    <div id="canvas-container"></div>
    <div class="relative z-10 flex flex-col md:flex-row w-full h-full p-4 md:p-6 gap-6">
        <!-- Sidebar -->
        <div class="w-full md:w-80 glass-panel rounded-3xl p-6 flex flex-col justify-between">
            <div>
                <div class="flex items-center gap-3 mb-6">
                    <div class="w-12 h-12 rounded-2xl glow-button flex items-center justify-center text-2xl shadow-lg">📅</div>
                    <div>
                        <h1 class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">3D Calendar</h1>
                        <p class="text-xs text-slate-400">Pro Edition</p>
                    </div>
                </div>
                <div class="space-y-3">
                    <button id="add-event-btn" class="w-full py-3 px-4 rounded-xl glow-button text-white font-semibold flex items-center justify-center gap-2 shadow-lg hover:opacity-90 transition">
                        <i class="fas font-bold fa-plus"></i> Add Event
                    </button>
                    <div class="p-4 rounded-2xl bg-slate-900/50 border border-slate-800">
                        <h3 class="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">3D Controls</h3>
                        <p class="text-xs text-slate-300">Drag/Tilt screen to move background 3D particle stage.</p>
                    </div>
                </div>
            </div>
            <div class="text-xs text-center text-slate-500">Made by merajshahofficial</div>
        </div>

        <!-- Main Calendar Area -->
        <div class="flex-1 glass-panel rounded-3xl p-6 flex flex-col overflow-hidden">
            <div class="flex justify-between items-center mb-6">
                <h2 id="current-month" class="text-2xl font-extrabold text-white">September 2026</h2>
                <div class="flex items-center gap-2">
                    <button id="prev-btn" class="w-10 h-10 rounded-xl bg-slate-800/80 hover:bg-slate-700 flex items-center justify-center text-white transition"><i class="fas fa-chevron-left"></i></button>
                    <button id="today-btn" class="px-4 h-10 rounded-xl bg-indigo-600/50 hover:bg-indigo-600 text-white font-medium text-sm transition">Today</button>
                    <button id="next-btn" class="w-10 h-10 rounded-xl bg-slate-800/80 hover:bg-slate-700 flex items-center justify-center text-white transition"><i class="fas fa-chevron-right"></i></button>
                </div>
            </div>

            <div class="calendar-grid text-center font-bold text-xs uppercase tracking-wider text-slate-400 mb-2">
                <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
            </div>

            <div id="calendar-days" class="calendar-grid flex-1 overflow-y-auto"></div>
        </div>
    </div>

    <script>
        // Three.js 3D Background Setup
        const container = document.getElementById('canvas-container');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        container.appendChild(renderer.domElement);

        const geometry = new THREE.BufferGeometry();
        const count = 700;
        const positions = new Float32Array(count * 3);
        const colors = new Float32Array(count * 3);

        for(let i = 0; i < count * 3; i+=3) {
            positions[i] = (Math.random() - 0.5) * 20;
            positions[i+1] = (Math.random() - 0.5) * 20;
            positions[i+2] = (Math.random() - 0.5) * 20;

            colors[i] = Math.random();
            colors[i+1] = Math.random();
            colors[i+2] = 1.0;
        }

        geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const material = new THREE.PointsMaterial({ size: 0.08, vertexColors: true, transparent: true, opacity: 0.8 });
        const particles = new THREE.Points(geometry, material);
        scene.add(particles);

        camera.position.z = 8;

        let mouseX = 0, mouseY = 0;
        document.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX / window.innerWidth - 0.5) * 0.5;
            mouseY = (e.clientY / window.innerHeight - 0.5) * 0.5;
        });

        function animate() {
            requestAnimationFrame(animate);
            particles.rotation.y += 0.002;
            particles.rotation.x += 0.001;
            camera.position.x += (mouseX - camera.position.x) * 0.05;
            camera.position.y += (-mouseY - camera.position.y) * 0.05;
            camera.lookAt(scene.position);
            renderer.render(scene, camera);
        }
        animate();

        // Calendar Render Logic
        let date = new Date(2026, 8, 15);
        const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

        function renderCalendar() {
            const year = date.getFullYear();
            const month = date.getMonth();
            document.getElementById('current-month').innerText = `${monthNames[month]} ${year}`;

            const daysContainer = document.getElementById('calendar-days');
            daysContainer.innerHTML = '';

            const firstDay = new Date(year, month, 1).getDay();
            const totalDays = new Date(year, month + 1, 0).getDate();

            for(let i = 0; i < firstDay; i++) {
                daysContainer.appendChild(document.createElement('div'));
            }

            for(let day = 1; day <= totalDays; day++) {
                const dayCard = document.createElement('div');
                const isToday = day === 15 && month === 8 && year === 2026;
                dayCard.className = `day-card rounded-2xl p-3 flex flex-col justify-between border ${isToday ? 'bg-indigo-600/40 border-indigo-400 text-white font-extrabold' : 'bg-slate-900/60 border-slate-800/80 text-slate-200'}`;
                dayCard.innerHTML = `<span class="text-sm">${day}</span>`;
                daysContainer.appendChild(dayCard);
            }
        }

        document.getElementById('prev-btn').addEventListener('click', () => { date.setMonth(date.getMonth() - 1); renderCalendar(); });
        document.getElementById('next-btn').addEventListener('click', () => { date.setMonth(date.getMonth() + 1); renderCalendar(); });
        document.getElementById('today-btn').addEventListener('click', () => { date = new Date(2026, 8, 15); renderCalendar(); });

        renderCalendar();
        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });
    </script>
</body>
</html>
"""

components.html(html_code, height=850, scrolling=True)


