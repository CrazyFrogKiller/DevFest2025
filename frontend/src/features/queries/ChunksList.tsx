import "../../styles/Main.css";

type Chunk = {
  id: string;
  text: string;
};

type ChunksListProps = {
  chunks?: Chunk[];
};

export default function ChunksList({ chunks = [] }: ChunksListProps) {
  const isEmpty = chunks.length === 0;

  return (
    <div className="chunks-container">
      <h4>Chunks</h4>

      {isEmpty ? (
        <div className="chunks-empty">
          <p className="response__rejected_massege">No chunks yet</p>
        </div>
      ) : (
        <ul className="chunks-list">
          {chunks.map(({ id, text }) => (
            <li key={id}>{text}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
