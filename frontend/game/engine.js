/**
 * Main Game Engine
 * Phaser.js game instance and core loop
 */

let game;
let sceneRenderer;
let currentNarration = [];

/**
 * Preload assets
 */
function preload() {
    // We're generating sprites programmatically, so minimal preload needed
    this.load.setBaseURL('/');
}

/**
 * Create game scene
 */
function create() {
    // Initialize scene renderer
    sceneRenderer = new SceneRenderer(this);

    // Set narration callback
    sceneRenderer.setNarrationCallback((text) => {
        addNarrationText(text);
    });

    // Add welcome text
    const welcomeText = this.add.text(400, 300, 'Cyber Defense Visualization System', {
        fontFamily: 'Courier New',
        fontSize: '24px',
        color: '#00ff41',
        align: 'center'
    });
    welcomeText.setOrigin(0.5);

    const subtitleText = this.add.text(400, 350, 'Select an attack or scenario to begin', {
        fontFamily: 'Courier New',
        fontSize: '16px',
        color: '#00d4ff',
        align: 'center'
    });
    subtitleText.setOrigin(0.5);

    // Store for later clearing
    this.welcomeTexts = [welcomeText, subtitleText];
}

/**
 * Update loop
 */
function update(time, delta) {
    // Update logic if needed
}

/**
 * Initialize the game
 */
function initGame() {
    if (game) {
        game.destroy(true);
    }

    game = new Phaser.Game(GAME_CONFIG);

    return game;
}

/**
 * Play a visualization scene
 */
async function playVisualization(sceneData) {
    if (!sceneRenderer) {
        console.error('Scene renderer not initialized');
        return;
    }

    // Clear welcome text
    if (game.scene.scenes[0].welcomeTexts) {
        game.scene.scenes[0].welcomeTexts.forEach(text => text.destroy());
        game.scene.scenes[0].welcomeTexts = [];
    }

    // Clear previous narration
    currentNarration = [];
    updateNarrationDisplay();

    // Render the scene
    await sceneRenderer.renderScene(sceneData);
}

/**
 * Add narration text
 */
function addNarrationText(text) {
    currentNarration.push(text);
    updateNarrationDisplay();
}

/**
 * Update narration display in UI
 */
function updateNarrationDisplay() {
    const narrationContent = document.getElementById('narration-content');

    if (currentNarration.length === 0) {
        narrationContent.innerHTML = '<p class="placeholder">Narration will appear here...</p>';
    } else {
        narrationContent.innerHTML = currentNarration
            .map(text => `<p>▶ ${text}</p>`)
            .join('');

        // Scroll to bottom
        narrationContent.scrollTop = narrationContent.scrollHeight;
    }
}

/**
 * Show technique info in UI
 */
function showTechniqueInfo(technique) {
    const infoContent = document.getElementById('info-content');

    infoContent.innerHTML = `
        <div class="technique-title">
            ${technique.name}
            <span class="technique-id">(${technique.id})</span>
        </div>
        <div class="technique-description">
            ${technique.description}
        </div>
        ${technique.tactics ? `
            <div class="technique-tactics">
                ${technique.tactics.map(tactic =>
                    `<span class="tactic-badge">${tactic}</span>`
                ).join('')}
            </div>
        ` : ''}
    `;
}

/**
 * Clear technique info
 */
function clearTechniqueInfo() {
    const infoContent = document.getElementById('info-content');
    infoContent.innerHTML = '<p class="placeholder">Select a technique to see details...</p>';
}

// Export for use in app.js
window.gameEngine = {
    initGame,
    playVisualization,
    addNarrationText,
    showTechniqueInfo,
    clearTechniqueInfo
};
