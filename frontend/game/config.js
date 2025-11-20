/**
 * Phaser Game Configuration
 * Retro 2D game engine for cybersecurity visualizations
 */

const GAME_CONFIG = {
    // Game dimensions
    width: 800,
    height: 600,

    // Rendering
    type: Phaser.AUTO,
    parent: 'game-container',
    backgroundColor: '#0a0e27',

    // Mobile-responsive scaling
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH,
        width: 800,
        height: 600,
        min: {
            width: 320,
            height: 240
        },
        max: {
            width: 1920,
            height: 1080
        }
    },

    // Physics (optional for some visualizations)
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 0 },
            debug: false
        }
    },

    // Pixel art settings for retro look
    pixelArt: true,
    antialias: false,

    // Scene configuration
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

// Color palette for retro style
const COLORS = {
    primary: 0x00ff41,    // Matrix green
    secondary: 0x00d4ff,  // Cyber blue
    danger: 0xff0055,     // Alert red
    warning: 0xffaa00,    // Warning orange
    neutral: 0xe0e0e0,    // Light gray
    attacker: 0xff0055,   // Red for attacker
    defender: 0x00d4ff,   // Blue for defender
    system: 0xffaa00      // Orange for system
};

// Asset sizes
const SPRITE_SIZE = 32;
const LARGE_SPRITE = 64;

// Animation speeds
const ANIM_SPEED = {
    slow: 0.5,
    normal: 1.0,
    fast: 2.0
};

// Common positions
const POSITIONS = {
    left: { x: 100, y: 300 },
    center: { x: 400, y: 300 },
    right: { x: 700, y: 300 },
    top: { x: 400, y: 100 },
    bottom: { x: 400, y: 500 }
};
