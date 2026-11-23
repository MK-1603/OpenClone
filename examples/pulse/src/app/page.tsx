"use client";

import { PulseProvider } from "@/context/PulseContext";
import { AppShell } from "@/components/layout/AppShell";

export default function HomePage() {
  return (
    <PulseProvider>
      <AppShell />
    </PulseProvider>
  );
}
