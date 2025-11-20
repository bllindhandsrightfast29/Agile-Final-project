/**
 * Main Application Logic
 * Handles WebSocket connection, UI interactions, and coordination
 */

class CyberVisualizationApp {
    constructor() {
        this.ws = null;
        this.isConnected = false;
        this.techniques = [];
        this.apiBaseUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? 'http://localhost:8000'
            : `http://${window.location.hostname}:8000`;
        this.wsUrl = this.apiBaseUrl.replace('http', 'ws') + '/ws';
    }

    /**
     * Initialize the application
     */
    async init() {
        console.log('🚀 Initializing Cyber Visualization App...');

        // Initialize game engine
        window.gameEngine.initGame();

        // Set up event listeners
        this.setupEventListeners();

        // Connect to WebSocket
        this.connectWebSocket();

        // Load techniques
        await this.loadTechniques();

        console.log('✅ App initialized');
    }

    /**
     * Set up UI event listeners
     */
    setupEventListeners() {
        // Simulate attack button
        document.getElementById('simulate-btn').addEventListener('click', () => {
            this.simulateAttack();
        });

        // Play scenario button
        document.getElementById('play-scenario-btn').addEventListener('click', () => {
            this.playScenario();
        });

        // Technique select change
        document.getElementById('technique-select').addEventListener('change', (e) => {
            if (e.target.value) {
                this.onTechniqueSelected(e.target.value);
            }
        });
    }

    /**
     * Connect to WebSocket server
     */
    connectWebSocket() {
        console.log(`Connecting to WebSocket: ${this.wsUrl}`);

        try {
            this.ws = new WebSocket(this.wsUrl);

            this.ws.onopen = () => {
                console.log('✅ WebSocket connected');
                this.isConnected = true;
                this.updateConnectionStatus(true);
            };

            this.ws.onmessage = (event) => {
                this.handleWebSocketMessage(event.data);
            };

            this.ws.onerror = (error) => {
                console.error('❌ WebSocket error:', error);
                this.updateConnectionStatus(false);
            };

            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                this.isConnected = false;
                this.updateConnectionStatus(false);

                // Try to reconnect after 5 seconds
                setTimeout(() => {
                    console.log('Attempting to reconnect...');
                    this.connectWebSocket();
                }, 5000);
            };
        } catch (error) {
            console.error('Failed to create WebSocket:', error);
            this.updateConnectionStatus(false);
        }
    }

    /**
     * Handle incoming WebSocket messages
     */
    handleWebSocketMessage(data) {
        const message = JSON.parse(data);
        console.log('📨 WebSocket message:', message);

        switch (message.type) {
            case 'connection_established':
                console.log(`Connected! ${message.available_techniques} techniques available`);
                break;

            case 'attack_simulation':
                this.visualizeAttack(message);
                break;

            case 'scenario_complete':
                window.gameEngine.addNarrationText(`✅ Scenario "${message.scenario}" completed!`);
                break;

            case 'pong':
                // Heartbeat response
                break;

            default:
                console.log('Unknown message type:', message.type);
        }
    }

    /**
     * Update connection status indicator
     */
    updateConnectionStatus(connected) {
        const statusEl = document.getElementById('connection-status');

        if (connected) {
            statusEl.className = 'status connected';
            statusEl.textContent = '✓ Connected';
        } else {
            statusEl.className = 'status disconnected';
            statusEl.textContent = '⚠ Disconnected';
        }
    }

    /**
     * Load available techniques from backend
     */
    async loadTechniques() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/techniques`);
            const data = await response.json();

            this.techniques = data.techniques || [];

            // Update technique count
            document.getElementById('technique-count').textContent = data.count || 0;

            // Populate select dropdown
            const select = document.getElementById('technique-select');
            select.innerHTML = '<option value="">Select a technique...</option>';

            this.techniques.forEach(tech => {
                const option = document.createElement('option');
                option.value = tech.id;
                option.textContent = `${tech.id} - ${tech.name}`;
                select.appendChild(option);
            });

            console.log(`✅ Loaded ${this.techniques.length} techniques`);
        } catch (error) {
            console.error('Failed to load techniques:', error);
            document.getElementById('technique-count').textContent = 'Error';
        }
    }

    /**
     * Handle technique selection
     */
    async onTechniqueSelected(techniqueId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/techniques/${techniqueId}`);
            const data = await response.json();

            if (data.technique) {
                window.gameEngine.showTechniqueInfo(data.technique);
            }
        } catch (error) {
            console.error('Failed to fetch technique details:', error);
        }
    }

    /**
     * Simulate an attack
     */
    async simulateAttack() {
        const select = document.getElementById('technique-select');
        const techniqueId = select.value;

        if (!techniqueId) {
            alert('Please select a technique first!');
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/api/simulate/${techniqueId}`, {
                method: 'POST'
            });

            const data = await response.json();
            console.log('Attack simulated:', data);

            // The visualization will come via WebSocket
        } catch (error) {
            console.error('Failed to simulate attack:', error);
            alert('Failed to simulate attack. Check console for details.');
        }
    }

    /**
     * Play a scenario
     */
    async playScenario() {
        const select = document.getElementById('scenario-select');
        const scenarioId = select.value;

        if (!scenarioId) {
            alert('Please select a scenario first!');
            return;
        }

        // For demo, we'll play scenarios client-side
        const scenarios = {
            'privilege-escalation': this.createPrivilegeEscalationScenario(),
            'lateral-movement': this.createLateralMovementScenario(),
            'credential-theft': this.createCredentialTheftScenario(),
            'data-exfil': this.createDataExfilScenario()
        };

        const scenario = scenarios[scenarioId];
        if (scenario) {
            window.gameEngine.clearTechniqueInfo();
            await window.gameEngine.playVisualization(scenario);
        }
    }

    /**
     * Visualize an attack from WebSocket message
     */
    async visualizeAttack(message) {
        console.log('🎬 Visualizing attack:', message.technique_name);

        // Show technique info
        if (message.technique_id) {
            const tech = this.techniques.find(t => t.id === message.technique_id);
            if (tech) {
                window.gameEngine.showTechniqueInfo(tech);
            }
        }

        // Display narration
        if (message.narration && message.narration.narration) {
            window.gameEngine.addNarrationText(message.narration.narration);
        }

        // Play visual scene
        if (message.visual && message.visual.scene) {
            await window.gameEngine.playVisualization(message.visual);
        }
    }

    /**
     * Create demo scenarios
     */
    createPrivilegeEscalationScenario() {
        return {
            scene: {
                type: "system",
                background: "permission_hierarchy",
                duration: 8.0,
                elements: [
                    {
                        type: "sprite",
                        asset: "user_low_privilege",
                        position: { x: 300, y: 450 },
                        animation: "idle",
                        duration: 2.0,
                        metadata: { privilege: "user", color: "green" }
                    },
                    {
                        type: "sprite",
                        asset: "ladder",
                        position: { x: 300, y: 300 },
                        animation: "appear",
                        duration: 6.0,
                        metadata: { delay: 1.0 }
                    },
                    {
                        type: "sprite",
                        asset: "user_climbing",
                        position: { x: 300, y: 300 },
                        animation: "climb",
                        duration: 3.0,
                        metadata: { delay: 2.0 }
                    },
                    {
                        type: "sprite",
                        asset: "crown",
                        position: { x: 300, y: 150 },
                        animation: "shine",
                        duration: 2.0,
                        metadata: { delay: 5.0 }
                    },
                    {
                        type: "sprite",
                        asset: "user_admin",
                        position: { x: 300, y: 150 },
                        animation: "celebrate",
                        duration: 3.0,
                        metadata: { delay: 5.0, color: "gold" }
                    }
                ],
                narration_points: [
                    { time: 0, text: "Attacker has low-privilege access..." },
                    { time: 2, text: "Exploit found! Escalating privileges..." },
                    { time: 5, text: "Root access obtained!" }
                ]
            }
        };
    }

    createLateralMovementScenario() {
        return {
            scene: {
                type: "network",
                background: "network_grid",
                duration: 12.0,
                elements: [
                    {
                        type: "sprite",
                        asset: "server",
                        position: { x: 200, y: 300 },
                        animation: "idle",
                        duration: 12.0
                    },
                    {
                        type: "sprite",
                        asset: "server",
                        position: { x: 400, y: 300 },
                        animation: "idle",
                        duration: 12.0
                    },
                    {
                        type: "sprite",
                        asset: "server",
                        position: { x: 600, y: 300 },
                        animation: "idle",
                        duration: 12.0
                    },
                    {
                        type: "sprite",
                        asset: "attacker_pacman",
                        position: { x: 200, y: 300 },
                        animation: "move_path",
                        duration: 10.0,
                        metadata: {
                            path: [
                                { x: 200, y: 300 },
                                { x: 400, y: 300 },
                                { x: 600, y: 300 }
                            ]
                        }
                    }
                ],
                narration_points: [
                    { time: 0, text: "Attacker moves from compromised system..." },
                    { time: 4, text: "Second system compromised!" },
                    { time: 8, text: "Third system breached! Network owned." }
                ]
            }
        };
    }

    createCredentialTheftScenario() {
        return {
            scene: {
                type: "system",
                background: "cyber_grid",
                duration: 8.0,
                elements: [
                    {
                        type: "sprite",
                        asset: "key",
                        position: { x: 150, y: 200 },
                        animation: "float",
                        duration: 8.0
                    },
                    {
                        type: "sprite",
                        asset: "key",
                        position: { x: 300, y: 250 },
                        animation: "float",
                        duration: 8.0
                    },
                    {
                        type: "sprite",
                        asset: "key",
                        position: { x: 450, y: 200 },
                        animation: "float",
                        duration: 8.0
                    },
                    {
                        type: "sprite",
                        asset: "attacker_pacman",
                        position: { x: 50, y: 200 },
                        animation: "move_path",
                        duration: 7.0,
                        metadata: {
                            path: [
                                { x: 150, y: 200 },
                                { x: 300, y: 250 },
                                { x: 450, y: 200 }
                            ]
                        }
                    }
                ],
                narration_points: [
                    { time: 0, text: "Dumping credentials from memory..." },
                    { time: 3, text: "Password hashes collected" },
                    { time: 6, text: "Access tokens acquired" }
                ]
            }
        };
    }

    createDataExfilScenario() {
        return {
            scene: {
                type: "network",
                background: "network_diagram",
                duration: 10.0,
                elements: [
                    {
                        type: "sprite",
                        asset: "database",
                        position: { x: 150, y: 300 },
                        animation: "idle",
                        duration: 10.0
                    },
                    {
                        type: "sprite",
                        asset: "server",
                        position: { x: 650, y: 300 },
                        animation: "idle",
                        duration: 10.0,
                        metadata: { compromised: true }
                    },
                    {
                        type: "sprite",
                        asset: "data_packet",
                        position: { x: 150, y: 300 },
                        animation: "move_to",
                        duration: 2.0,
                        metadata: { target: { x: 650, y: 300 } }
                    },
                    {
                        type: "sprite",
                        asset: "data_packet",
                        position: { x: 150, y: 300 },
                        animation: "move_to",
                        duration: 2.0,
                        metadata: { target: { x: 650, y: 300 }, delay: 2.0 }
                    },
                    {
                        type: "sprite",
                        asset: "data_packet",
                        position: { x: 150, y: 300 },
                        animation: "move_to",
                        duration: 2.0,
                        metadata: { target: { x: 650, y: 300 }, delay: 4.0 }
                    }
                ],
                narration_points: [
                    { time: 0, text: "Sensitive data identified..." },
                    { time: 2, text: "Exfiltration in progress!" },
                    { time: 5, text: "Data streaming to attacker server" }
                ]
            }
        };
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new CyberVisualizationApp();
    app.init();

    // Make app globally available for debugging
    window.cyberApp = app;
});
