import { useState } from "react";
import { uploadDocument } from "./documentsApi";
import "../../styles/Main.css";

export default function DocumentUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const onUpload = async () => {
    if (!file) return;

    const form = new FormData();
    form.append("file", file);

    setIsLoading(true);
    try {
      await uploadDocument(form);
      setFile(null);
    } catch (err) {
      console.error("Upload error:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelate = () => {
    setFile(null);
  };

  return (
    <div className="upload">
      <label className="upload__input-label">
        <span className="upload__btn">Choose File</span>
        <input
          type="file"
          className="upload__input"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
      </label>

      <span className="upload__filename">
        {file ? file.name : "No file selected"}
      </span>

      <button
        className="upload__button"
        onClick={onUpload}
        disabled={!file || isLoading}
      >
        {isLoading ? "Uploading…" : "Upload"}
      </button>
      <button
        className="upload__button-delate"
        onClick={handleDelate}
        disabled={!file || isLoading}
      >
        Delate
      </button>
    </div>
  );
}
