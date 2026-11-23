"use client";

import React, { useState } from "react";
import { X, FolderPlus, CheckSquare } from "lucide-react";
import { CreateProjectModal } from "./CreateProjectModal";
import { CreateTaskModal } from "./CreateTaskModal";

interface QuickCreateModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const QuickCreateModal: React.FC<QuickCreateModalProps> = ({ isOpen, onClose }) => {
  const [projectModalOpen, setProjectModalOpen] = useState(false);
  const [taskModalOpen, setTaskModalOpen] = useState(false);

  if (!isOpen && !projectModalOpen && !taskModalOpen) return null;

  return (
    <>
      {isOpen && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="w-full max-w-md bg-[#141414] border border-[rgba(255,255,255,0.12)] rounded-2xl shadow-2xl p-6 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.06)]">
              <h2 className="text-sm font-semibold text-[#F5F5F5]">Quick Create</h2>
              <button
                onClick={onClose}
                className="p-1 rounded-md text-[#71717A] hover:text-[#F5F5F5] hover:bg-[#202020]"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="mt-4 grid grid-cols-2 gap-3">
              <button
                onClick={() => {
                  onClose();
                  setProjectModalOpen(true);
                }}
                className="flex flex-col items-center justify-center p-5 rounded-xl bg-[#1B1B1B] hover:bg-[#222222] border border-[rgba(255,255,255,0.06)] hover:border-[rgba(214,179,106,0.3)] transition-all group text-center"
              >
                <div className="p-3 rounded-lg bg-[#272727] group-hover:bg-[#2F291C] text-[#A1A1AA] group-hover:text-[#D6B36A] transition-colors mb-2.5">
                  <FolderPlus className="w-6 h-6" />
                </div>
                <span className="text-xs font-semibold text-[#F5F5F5]">New Project</span>
                <span className="text-[10px] text-[#71717A] mt-1">Initiate a workspace</span>
              </button>

              <button
                onClick={() => {
                  onClose();
                  setTaskModalOpen(true);
                }}
                className="flex flex-col items-center justify-center p-5 rounded-xl bg-[#1B1B1B] hover:bg-[#222222] border border-[rgba(255,255,255,0.06)] hover:border-[rgba(214,179,106,0.3)] transition-all group text-center"
              >
                <div className="p-3 rounded-lg bg-[#272727] group-hover:bg-[#2F291C] text-[#A1A1AA] group-hover:text-[#D6B36A] transition-colors mb-2.5">
                  <CheckSquare className="w-6 h-6" />
                </div>
                <span className="text-xs font-semibold text-[#F5F5F5]">New Task</span>
                <span className="text-[10px] text-[#71717A] mt-1">Add a deliverable</span>
              </button>
            </div>
          </div>
        </div>
      )}

      <CreateProjectModal
        isOpen={projectModalOpen}
        onClose={() => setProjectModalOpen(false)}
      />

      <CreateTaskModal
        isOpen={taskModalOpen}
        onClose={() => setTaskModalOpen(false)}
      />
    </>
  );
};
