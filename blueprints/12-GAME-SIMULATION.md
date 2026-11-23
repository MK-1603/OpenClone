# Blueprint 12: Game & Simulation Engineering

**Project Family:** `game_and_simulation`  
**Primary Project Type:** `game_application`  
**Maturity Status:** `SPECIFIED`  
**Complexity Level:** `MEDIUM` to `LARGE`  
**Default Delivery Targets:** `web_browser`, `windows`, `macos`, `linux`

---

## 1. Goals & Scope
- Interactive 2D/3D games, entity-component-system (ECS) architectures, graphics rendering loops, physics simulations, and audio engines.
- Focuses on frame rate stability (consistent 60/120 FPS), input responsiveness, spatial audio, and cross-platform controller support.

## 2. Classification Rules
- Matched when the application centers on continuous game loops, 2D/3D graphics viewports, canvas/WebGL/WebGPU, game engines (Godot, Phaser, PixiJS, Unity), or physics simulation.

## 3. Intake Questions & Required Information
1. Dimension and graphics: 2D sprite/tilemap vs. 3D polygon mesh with shaders.
2. Engine / toolkit: Godot, Phaser, Bevy (Rust), Three.js, WebGL/WebGPU.
3. Physics model: rigid body collision, raycasting, particles, gravity.
4. Input handling: keyboard, mouse, gamepad, touch gestures.

## 4. Domain & Capability Mapping
- **Mandatory Domains:** `01-SPECIFICATION`, `02-ARCHITECTURE`, `05-DESIGN-SYSTEMS`, `14-PERFORMANCE-ENGINEERING`.
- **Mandatory Engines:** `E-001`, `E-002`, `E-005`, `E-014`.

## 5. Specialist Workforce
- `game-engine-engineer`: Game loop, frame timing, and ECS state.
- `graphics-engineer`: Shader pipelines, textures, and draw call optimization.
- `gameplay-programmer`: Game mechanics, inventory, collision, and UI HUD.

## 6. Verification & Delivery Artifacts
- Frame pacing test logs proving zero dropped frames under load.
- Asset bundle packaging with compressed textures and audio sprites.
- Cross-platform controller input mapping test suite.
