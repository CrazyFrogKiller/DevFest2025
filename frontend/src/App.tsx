import { useState } from "react";
import { useSelector } from "react-redux";
import Layout from "./components/Layout";
import QueryInput from "./features/queries/QueryInput";
import QueryResponse from "./features/queries/QueryResponse";
import DocumentUpload from "./features/documents/DocumentUpload";
import ChunksList from "./features/queries/ChunksList";
import "./styles/Main.css";
import SourcesList from "./features/queries/SourcesList";

export default function App() {
    const response = useSelector((state: any) => state.queries.currentResponse);
    const [isOpen, setIsOpen] = useState(false);

  return (
    <Layout>
      <div className="block__input">
        <div className="input__qerry">
          <QueryInput />
          <QueryResponse response={response} />
        </div>

        <div className="input__qerry">
          <h2>Documents</h2>
          <DocumentUpload />
          <ChunksList />
        </div>

        <button className="sources__open" onClick={() => setIsOpen(true)}>
          Подробнее
        </button>

        <SourcesList
          open={isOpen}
          onClose={() => setIsOpen(false)}
          sources={response?.sources ?? []}
        />
      </div>
    </Layout>
  );
}
