import React from "react";
import "../../styles/Main.css";

export type Source = {
  filename: string;
  chunk_index: number;
  lines?: string;
};

type Props = {
  open: boolean;
  onClose: () => void;
  sources: Source[];
};

export default function SourcesList({ open, onClose, sources }: Props) {
  if (!open) return null;

  const element = sources.map((src, idx) => (
    <li key={idx} className="modal__item">
      <strong>{src.filename}</strong>
      <span> — chunk {src.chunk_index}</span>
      {src.lines && <span> — lines {src.lines}</span>}
    </li>
  ));

  return (
    <div className="modal">
      <div className="modal__content">
        <h3>Источники</h3>
        <ul className="modal__list">{element}</ul>
        <button className="modal__close" onClick={onClose}>
          Закрыть
        </button>
      </div>
    </div>
  );
}
