type SourceReferenceProps = {
  source: string;
  page?: number;
};

export default function SourceReference({
  source,
  page,
}: SourceReferenceProps) {
  return (
    <div className="source-ref">
      <strong>Source:</strong> {source} {page ? `(p. ${page})` : ""}
    </div>
  );
}
