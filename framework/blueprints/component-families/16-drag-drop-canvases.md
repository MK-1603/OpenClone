# Component Family 16: Drag-and-Drop & Canvas Workspaces
**Registry ID Range:** `C-1601` to `C-1603`  
**Governing Authority:** OpenClone DIEE Domain 05  

---

## 1. Overview & Anatomy
Workspaces enable tactile item reordering, Kanban task management, and resizable layout splitters.

## 2. Headless Foundation & Styling
- **Engine:** `@dnd-kit/core` + `@dnd-kit/sortable` + `react-resizable-panels`.
- **Drag Feedback:** Droppable targets highlight with an electric cyan hairline border (`border-cyan-400/50`).

## 3. TypeScript Prop Contract
```typescript
export interface KanbanCard {
  id: string;
  title: string;
  tags?: string[];
  assignee?: { name: string; avatarUrl: string };
}

export interface KanbanColumnProps {
  id: string;
  title: string;
  cards: KanbanCard[];
  onCardMove: (cardId: string, targetColId: string, newIndex: number) => void;
}
```

## 4. 6-State Resilience Matrix
- `INITIAL`: Rendered columns and cards.
- `LOADING`: Column shimmer skeletons.
- `SUCCESS`: Smooth 60fps drag with spring physics snapping.
- `ERROR`: Optimistic rollback if server reorder sync fails.

## 5. WCAG 2.2 AAA Accessibility
- Full keyboard drag-and-drop: Space to pick up card, Arrow keys to move, Space to drop, Escape to cancel.
