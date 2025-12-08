import "../../styles/Main.css";

type Chunk = {
    id: string;
    content: string;
    score?: number;
    source?: string;
};

type QueryResponseProps = {
    response?: {
        answer?: string;
        chunks?: Chunk[];
        sources?: { id: string }[];
        query?: string;
        detail?: string;
        total_tokens?: number;
    } | null;
};

export default function QueryResponse({ response }: QueryResponseProps) {
    console.log("RESPONSE:", response);

    const isSuccess = response?.answer;
    const isError = response?.detail;

    const chunksElement =
        response?.chunks?.length
            ? response.chunks.map((c) => <li key={c.id}>{c.score}{c.content}</li>)
            : null;

    return (
        <div className="list__query">
            <h4>Response</h4>

            {!response && (
                <div className="placeholder">
                    <p className="response__rejected_massege">
                        No response yet. Try entering a query.
                    </p>
                </div>
            )}

            {isSuccess && (
                <>
                    <div className="answer">{response.answer}</div>
                    {chunksElement && (
                        <ul className="chunks-list">{chunksElement}</ul>
                    )}
                </>
            )}

            {isError && (
                <div className="placeholder error">
                    <p className="response__error_message">{response.detail}</p>
                </div>
            )}
        </div>
    );
}
