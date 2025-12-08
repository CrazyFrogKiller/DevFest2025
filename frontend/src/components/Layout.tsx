import "../styles/Main.css";

type LayoutProps = {
  children?: React.ReactNode;
};

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="layout">
      <header className="layout__header">
        <h1>RAG System</h1>
        <p className="layout__subtitle">
          Document Management & Query Interface
        </p>
      </header>

      <main className="layout__main">{children}</main>

      <footer className="layout__footer">© 2025 RAG System</footer>
    </div>
  );
}
