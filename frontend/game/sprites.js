/**
 * Sprite and Asset Management
 * Creates retro-style sprites for visualizations
 */

class SpriteFactory {
    constructor(scene) {
        this.scene = scene;
    }

    /**
     * Create a Pacman-style attacker sprite
     */
    createAttackerPacman(x, y) {
        const graphics = this.scene.add.graphics();

        // Draw Pacman-style circle
        graphics.fillStyle(COLORS.attacker, 1);
        graphics.beginPath();
        graphics.arc(0, 0, 16, Phaser.Math.DegToRad(30), Phaser.Math.DegToRad(330));
        graphics.lineTo(0, 0);
        graphics.closePath();
        graphics.fillPath();

        // Convert to texture
        graphics.generateTexture('attacker_pacman', 32, 32);
        graphics.destroy();

        // Create sprite
        const sprite = this.scene.add.sprite(x, y, 'attacker_pacman');
        sprite.setData('type', 'attacker');

        return sprite;
    }

    /**
     * Create a snake-style attacker (for lateral movement)
     */
    createAttackerSnake(x, y, length = 3) {
        const segments = [];

        for (let i = 0; i < length; i++) {
            const graphics = this.scene.add.graphics();
            graphics.fillStyle(COLORS.attacker, 1);
            graphics.fillRect(0, 0, 24, 24);

            graphics.generateTexture(`snake_segment_${i}`, 24, 24);
            graphics.destroy();

            const segment = this.scene.add.sprite(x - (i * 28), y, `snake_segment_${i}`);
            segments.push(segment);
        }

        return segments;
    }

    /**
     * Create a server/system sprite
     */
    createServer(x, y, compromised = false) {
        const graphics = this.scene.add.graphics();

        // Server box
        const color = compromised ? COLORS.danger : COLORS.secondary;
        graphics.lineStyle(2, color, 1);
        graphics.fillStyle(color, 0.2);
        graphics.fillRect(0, 0, 48, 48);
        graphics.strokeRect(0, 0, 48, 48);

        // Add some details (server lights)
        for (let i = 0; i < 3; i++) {
            graphics.fillStyle(color, 1);
            graphics.fillCircle(12, 12 + (i * 12), 2);
            graphics.fillCircle(36, 12 + (i * 12), 2);
        }

        graphics.generateTexture('server', 48, 48);
        graphics.destroy();

        const sprite = this.scene.add.sprite(x, y, 'server');
        sprite.setData('type', 'server');
        sprite.setData('compromised', compromised);

        return sprite;
    }

    /**
     * Create a user icon sprite
     */
    createUser(x, y, privileged = false) {
        const graphics = this.scene.add.graphics();

        const color = privileged ? COLORS.warning : COLORS.primary;

        // Head
        graphics.lineStyle(2, color, 1);
        graphics.strokeCircle(16, 12, 8);

        // Body
        graphics.beginPath();
        graphics.moveTo(16, 20);
        graphics.lineTo(16, 28);
        graphics.strokePath();

        // Arms
        graphics.beginPath();
        graphics.moveTo(8, 22);
        graphics.lineTo(16, 24);
        graphics.lineTo(24, 22);
        graphics.strokePath();

        // Legs
        graphics.beginPath();
        graphics.moveTo(16, 28);
        graphics.lineTo(12, 36);
        graphics.strokePath();

        graphics.beginPath();
        graphics.moveTo(16, 28);
        graphics.lineTo(20, 36);
        graphics.strokePath();

        if (privileged) {
            // Add crown for admin/root
            graphics.fillStyle(COLORS.warning, 1);
            graphics.fillTriangle(12, 6, 16, 2, 20, 6);
        }

        graphics.generateTexture(privileged ? 'user_admin' : 'user', 32, 40);
        graphics.destroy();

        return this.scene.add.sprite(x, y, privileged ? 'user_admin' : 'user');
    }

    /**
     * Create a firewall sprite
     */
    createFirewall(x, y) {
        const graphics = this.scene.add.graphics();

        graphics.lineStyle(3, COLORS.secondary, 1);

        // Brick pattern
        for (let row = 0; row < 4; row++) {
            for (let col = 0; col < 3; col++) {
                const offsetX = (row % 2) * 16;
                graphics.strokeRect(col * 32 + offsetX, row * 16, 32, 16);
            }
        }

        graphics.generateTexture('firewall', 96, 64);
        graphics.destroy();

        return this.scene.add.sprite(x, y, 'firewall');
    }

    /**
     * Create a key/credential sprite
     */
    createKey(x, y) {
        const graphics = this.scene.add.graphics();

        graphics.lineStyle(2, COLORS.warning, 1);
        graphics.fillStyle(COLORS.warning, 0.8);

        // Key head
        graphics.fillCircle(8, 8, 6);
        graphics.strokeCircle(8, 8, 6);

        // Key shaft
        graphics.fillRect(12, 6, 16, 4);
        graphics.strokeRect(12, 6, 16, 4);

        // Key teeth
        graphics.fillRect(24, 2, 4, 8);
        graphics.fillRect(20, 2, 4, 6);

        graphics.generateTexture('key', 32, 16);
        graphics.destroy();

        return this.scene.add.sprite(x, y, 'key');
    }

    /**
     * Create a database sprite
     */
    createDatabase(x, y) {
        const graphics = this.scene.add.graphics();

        graphics.lineStyle(2, COLORS.primary, 1);
        graphics.fillStyle(COLORS.primary, 0.2);

        // Cylinder
        graphics.fillEllipse(24, 12, 40, 20);
        graphics.strokeEllipse(24, 12, 40, 20);

        graphics.fillRect(4, 12, 40, 32);
        graphics.strokeRect(4, 12, 40, 32);

        graphics.fillEllipse(24, 44, 40, 20);
        graphics.strokeEllipse(24, 44, 40, 20);

        graphics.generateTexture('database', 48, 56);
        graphics.destroy();

        return this.scene.add.sprite(x, y, 'database');
    }

    /**
     * Create a data packet sprite
     */
    createDataPacket(x, y) {
        const graphics = this.scene.add.graphics();

        graphics.fillStyle(COLORS.primary, 0.8);
        graphics.lineStyle(2, COLORS.primary, 1);

        // Envelope shape
        graphics.fillRect(0, 4, 24, 16);
        graphics.strokeRect(0, 4, 24, 16);

        graphics.beginPath();
        graphics.moveTo(0, 4);
        graphics.lineTo(12, 12);
        graphics.lineTo(24, 4);
        graphics.strokePath();

        graphics.generateTexture('data_packet', 24, 20);
        graphics.destroy();

        return this.scene.add.sprite(x, y, 'data_packet');
    }

    /**
     * Create a ladder for privilege escalation
     */
    createLadder(x, y, rungs = 5) {
        const graphics = this.scene.add.graphics();

        graphics.lineStyle(3, COLORS.warning, 1);

        const height = rungs * 32;

        // Side rails
        graphics.lineTo(8, 0);
        graphics.lineTo(8, height);
        graphics.strokePath();

        graphics.beginPath();
        graphics.moveTo(24, 0);
        graphics.lineTo(24, height);
        graphics.strokePath();

        // Rungs
        for (let i = 0; i <= rungs; i++) {
            graphics.beginPath();
            graphics.moveTo(8, i * 32);
            graphics.lineTo(24, i * 32);
            graphics.strokePath();
        }

        graphics.generateTexture('ladder', 32, height);
        graphics.destroy();

        return this.scene.add.sprite(x, y, 'ladder');
    }

    /**
     * Create particle effects
     */
    createExplosionEffect(x, y, color = COLORS.danger) {
        const particles = this.scene.add.particles('');

        // Create simple particle texture
        const graphics = this.scene.add.graphics();
        graphics.fillStyle(color, 1);
        graphics.fillCircle(4, 4, 4);
        graphics.generateTexture('particle', 8, 8);
        graphics.destroy();

        const emitter = particles.createEmitter({
            x: x,
            y: y,
            speed: { min: 50, max: 200 },
            angle: { min: 0, max: 360 },
            scale: { start: 1, end: 0 },
            alpha: { start: 1, end: 0 },
            lifespan: 600,
            blendMode: 'ADD',
            quantity: 20,
            on: false
        });

        emitter.explode();

        return particles;
    }

    /**
     * Create a terminal/console sprite
     */
    createTerminal(x, y, width = 400, height = 300) {
        const graphics = this.scene.add.graphics();

        // Terminal window
        graphics.fillStyle(0x000000, 0.9);
        graphics.fillRect(0, 0, width, height);

        graphics.lineStyle(2, COLORS.primary, 1);
        graphics.strokeRect(0, 0, width, height);

        // Title bar
        graphics.fillStyle(COLORS.primary, 0.3);
        graphics.fillRect(0, 0, width, 24);

        graphics.generateTexture('terminal', width, height);
        graphics.destroy();

        return this.scene.add.sprite(x, y, 'terminal');
    }

    /**
     * Create crown for admin/root
     */
    createCrown(x, y) {
        const graphics = this.scene.add.graphics();

        graphics.fillStyle(COLORS.warning, 1);
        graphics.lineStyle(2, COLORS.warning, 1);

        // Crown shape
        graphics.beginPath();
        graphics.moveTo(4, 20);
        graphics.lineTo(8, 8);
        graphics.lineTo(16, 12);
        graphics.lineTo(24, 8);
        graphics.lineTo(28, 20);
        graphics.closePath();
        graphics.fillPath();
        graphics.strokePath();

        // Base
        graphics.fillRect(4, 20, 24, 4);

        graphics.generateTexture('crown', 32, 24);
        graphics.destroy();

        return this.scene.add.sprite(x, y, 'crown');
    }
}
