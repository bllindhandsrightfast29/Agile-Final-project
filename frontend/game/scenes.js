/**
 * Scene Renderer - Plays attack visualizations
 */

class SceneRenderer {
    constructor(scene) {
        this.scene = scene;
        this.spriteFactory = new SpriteFactory(scene);
        this.activeElements = [];
        this.narrationCallback = null;
    }

    /**
     * Set callback for narration updates
     */
    setNarrationCallback(callback) {
        this.narrationCallback = callback;
    }

    /**
     * Clear current scene
     */
    clearScene() {
        // Destroy all active elements
        this.activeElements.forEach(elem => {
            if (elem && elem.destroy) {
                elem.destroy();
            }
        });
        this.activeElements = [];

        // Clear any existing tweens
        this.scene.tweens.killAll();
    }

    /**
     * Render a complete attack scene
     */
    async renderScene(sceneData) {
        this.clearScene();

        const { scene, narration_points } = sceneData;

        // Add background
        this.addBackground(scene.background);

        // Schedule narration points
        if (narration_points && this.narrationCallback) {
            narration_points.forEach(point => {
                this.scene.time.delayedCall(point.time * 1000, () => {
                    this.narrationCallback(point.text);
                });
            });
        }

        // Render each element
        for (const element of scene.elements) {
            await this.renderElement(element);
        }

        return new Promise(resolve => {
            this.scene.time.delayedCall(scene.duration * 1000, resolve);
        });
    }

    /**
     * Add background
     */
    addBackground(backgroundType) {
        const graphics = this.scene.add.graphics();

        switch (backgroundType) {
            case 'network_diagram':
                this.drawNetworkBackground(graphics);
                break;
            case 'terminal_screen':
                this.drawTerminalBackground(graphics);
                break;
            case 'permission_hierarchy':
                this.drawHierarchyBackground(graphics);
                break;
            case 'network_grid':
                this.drawGridBackground(graphics);
                break;
            case 'cyber_grid':
            default:
                this.drawCyberBackground(graphics);
                break;
        }

        this.activeElements.push(graphics);
    }

    drawNetworkBackground(graphics) {
        graphics.lineStyle(1, COLORS.primary, 0.2);

        // Draw network nodes
        const nodes = [
            { x: 150, y: 150 },
            { x: 400, y: 100 },
            { x: 650, y: 150 },
            { x: 400, y: 400 },
        ];

        nodes.forEach((node, i) => {
            graphics.strokeCircle(node.x, node.y, 30);
            nodes.forEach((other, j) => {
                if (j > i) {
                    graphics.lineBetween(node.x, node.y, other.x, other.y);
                }
            });
        });
    }

    drawTerminalBackground(graphics) {
        graphics.fillStyle(0x000000, 0.8);
        graphics.fillRect(50, 50, 700, 500);

        graphics.lineStyle(2, COLORS.primary, 1);
        graphics.strokeRect(50, 50, 700, 500);
    }

    drawHierarchyBackground(graphics) {
        graphics.lineStyle(1, COLORS.secondary, 0.3);

        // Draw privilege levels
        const levels = ['User', 'Power User', 'Admin', 'Root'];
        levels.forEach((level, i) => {
            const y = 500 - (i * 120);
            graphics.strokeRect(200, y, 400, 80);

            // Add text would go here if using proper text rendering
        });
    }

    drawGridBackground(graphics) {
        graphics.lineStyle(1, COLORS.primary, 0.1);

        for (let x = 0; x < 800; x += 50) {
            graphics.lineBetween(x, 0, x, 600);
        }
        for (let y = 0; y < 600; y += 50) {
            graphics.lineBetween(0, y, 800, y);
        }
    }

    drawCyberBackground(graphics) {
        graphics.lineStyle(1, COLORS.secondary, 0.15);

        // Diagonal grid
        for (let i = -600; i < 1400; i += 50) {
            graphics.lineBetween(i, 0, i + 600, 600);
            graphics.lineBetween(i, 600, i + 600, 0);
        }
    }

    /**
     * Render individual element
     */
    async renderElement(element) {
        const delay = element.metadata?.delay || 0;

        return new Promise(resolve => {
            this.scene.time.delayedCall(delay * 1000, () => {
                let sprite;

                switch (element.asset) {
                    case 'attacker_pacman':
                        sprite = this.spriteFactory.createAttackerPacman(
                            element.position.x,
                            element.position.y
                        );
                        break;

                    case 'attacker_snake':
                        sprite = this.spriteFactory.createAttackerSnake(
                            element.position.x,
                            element.position.y
                        );
                        break;

                    case 'server':
                        sprite = this.spriteFactory.createServer(
                            element.position.x,
                            element.position.y,
                            element.metadata?.compromised
                        );
                        break;

                    case 'user_icon':
                        sprite = this.spriteFactory.createUser(
                            element.position.x,
                            element.position.y
                        );
                        break;

                    case 'user_admin':
                        sprite = this.spriteFactory.createUser(
                            element.position.x,
                            element.position.y,
                            true
                        );
                        break;

                    case 'firewall':
                        sprite = this.spriteFactory.createFirewall(
                            element.position.x,
                            element.position.y
                        );
                        break;

                    case 'key':
                        sprite = this.spriteFactory.createKey(
                            element.position.x,
                            element.position.y
                        );
                        break;

                    case 'database':
                        sprite = this.spriteFactory.createDatabase(
                            element.position.x,
                            element.position.y
                        );
                        break;

                    case 'data_packet':
                        sprite = this.spriteFactory.createDataPacket(
                            element.position.x,
                            element.position.y
                        );
                        break;

                    case 'ladder':
                        sprite = this.spriteFactory.createLadder(
                            element.position.x,
                            element.position.y
                        );
                        break;

                    case 'crown':
                        sprite = this.spriteFactory.createCrown(
                            element.position.x,
                            element.position.y
                        );
                        break;

                    case 'user_low_privilege':
                        sprite = this.spriteFactory.createUser(
                            element.position.x,
                            element.position.y,
                            false
                        );
                        break;

                    case 'user_climbing':
                        sprite = this.spriteFactory.createUser(
                            element.position.x,
                            element.position.y,
                            false
                        );
                        break;

                    default:
                        // Generic sprite
                        sprite = this.scene.add.circle(
                            element.position.x,
                            element.position.y,
                            16,
                            COLORS.primary
                        );
                }

                if (sprite) {
                    this.activeElements.push(sprite);
                    this.animateElement(sprite, element);
                }

                resolve();
            });
        });
    }

    /**
     * Animate an element
     */
    animateElement(sprite, element) {
        switch (element.animation) {
            case 'move_right':
                this.scene.tweens.add({
                    targets: sprite,
                    x: sprite.x + 350,
                    duration: element.duration * 1000,
                    ease: 'Linear'
                });
                break;

            case 'move_to':
                if (element.metadata?.target) {
                    this.scene.tweens.add({
                        targets: sprite,
                        x: element.metadata.target.x,
                        y: element.metadata.target.y,
                        duration: element.duration * 1000,
                        ease: 'Power2'
                    });
                }
                break;

            case 'move_path':
                if (element.metadata?.path) {
                    this.animatePath(sprite, element.metadata.path, element.duration);
                }
                break;

            case 'climb':
                this.scene.tweens.add({
                    targets: sprite,
                    y: sprite.y - 300,
                    duration: element.duration * 1000,
                    ease: 'Power1'
                });
                break;

            case 'pulse':
                this.scene.tweens.add({
                    targets: sprite,
                    scale: { from: 1, to: 1.3 },
                    alpha: { from: 1, to: 0.5 },
                    duration: 500,
                    yoyo: true,
                    repeat: Math.floor((element.duration * 1000) / 1000)
                });
                break;

            case 'explode':
                this.spriteFactory.createExplosionEffect(sprite.x, sprite.y);
                sprite.setAlpha(0);
                break;

            case 'celebrate':
                this.scene.tweens.add({
                    targets: sprite,
                    angle: { from: -15, to: 15 },
                    duration: 300,
                    yoyo: true,
                    repeat: Math.floor((element.duration * 1000) / 600)
                });
                break;

            case 'float':
                this.scene.tweens.add({
                    targets: sprite,
                    y: sprite.y - 10,
                    duration: 1000,
                    yoyo: true,
                    repeat: -1,
                    ease: 'Sine.easeInOut'
                });
                break;

            case 'fade_in':
                sprite.setAlpha(0);
                this.scene.tweens.add({
                    targets: sprite,
                    alpha: 1,
                    duration: element.duration * 1000,
                    ease: 'Power2'
                });
                break;

            case 'appear':
                sprite.setScale(0);
                this.scene.tweens.add({
                    targets: sprite,
                    scale: 1,
                    duration: 500,
                    ease: 'Back.easeOut'
                });
                break;

            case 'shine':
                this.scene.tweens.add({
                    targets: sprite,
                    scale: { from: 0, to: 1.5 },
                    alpha: { from: 0, to: 1 },
                    duration: element.duration * 1000,
                    ease: 'Power2'
                });
                break;
        }
    }

    /**
     * Animate along a path
     */
    animatePath(sprite, path, duration) {
        const points = path.map(p => ({ x: p.x, y: p.y }));

        let currentPoint = 0;
        const timePerPoint = (duration * 1000) / (points.length - 1);

        const moveToNext = () => {
            if (currentPoint >= points.length - 1) return;

            currentPoint++;
            this.scene.tweens.add({
                targets: sprite,
                x: points[currentPoint].x,
                y: points[currentPoint].y,
                duration: timePerPoint,
                ease: 'Linear',
                onComplete: moveToNext
            });
        };

        moveToNext();
    }
}
