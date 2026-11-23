"use client";

import React from "react";
import { AlertTriangle, X } from "lucide-react";

interface ConfirmDeleteModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
}

export const ConfirmDeleteModal: React.FC<ConfirmDeleteModalProps> = ({
  isOpen,
  onClose,
  onConfirm,
  title,
  message,
}) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div className="w-full max-w-sm bg-[#161616] border border-[rgba(255,255,255,0.12)] rounded-2xl shadow-2xl p-5 animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.06)]">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-[#281515] border border-[rgba(239,68,68,0.3)]">
              <AlertTriangle className="w-4 h-4 text-[#EF4444]" />
            </div>
            <h3 className="text-xs font-semibold text-[#F5F5F5]">{title}</h3>
          </div>
          <button onClick={onClose} className="p-1 rounded text-[#71717A] hover:text-[#F5F5F5]">
            <X className="w-3.5 h-3.5" />
          </button>
        </div>

        <p className="mt-3 text-xs text-[#A1A1AA] leading-relaxed">{message}</p>

        <div className="flex items-center justify-end gap-2.5 mt-5">
          <button
            onClick={onClose}
            className="px-3 py-1.5 text-xs text-[#A1A1AA] hover:text-[#F5F5F5] bg-[#222222] hover:bg-[#2A2A2A] rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={() => {
              onConfirm();
              onClose();
            }}
            className="px-3 py-1.5 text-xs font-medium text-white bg-[#EF4444] hover:bg-[#DC2626] rounded-lg shadow-sm transition-colors"
          >
            Confirm Delete
          </button>
        </div>
      </div>
    </div>
  );
};
