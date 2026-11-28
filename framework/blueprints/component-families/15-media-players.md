# Component Family 15: Media Players & Lightboxes
**Registry ID Range:** `C-1501` to `C-1503`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Media components host responsive video embeds, zoomable accessible image lightboxes, and audio podcast waveforms.

## 2. Headless Foundation & Styling
- **Engine:** `@radix-ui/react-dialog` for modal zoom + HTML5 Video/Audio.
- **Aspect Ratio Wrapper:** CSS `aspect-ratio: 16 / 9` to eliminate layout shift during asset loading.

## 3. TypeScript Prop Contract
```typescript
export interface MediaPlayerProps {
  src: string;
  poster?: string;
  aspectRatio?: "16/9" | "4/3" | "1/1";
  caption?: string;
  autoPlay?: boolean;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Poster image with play button overlay.
- `LOADING`: Shimmer loader covering aspect ratio frame.
- `SUCCESS`: Fluid playback with custom accessible controls.
- `ERROR`: Fallback message with download link.

## 5. WCAG 2.2 AAA Accessibility
- Captions (`<track kind="captions">`) required for all video media.
- Full keyboard control: Space/K to toggle play, Arrow keys to seek, M to mute.
