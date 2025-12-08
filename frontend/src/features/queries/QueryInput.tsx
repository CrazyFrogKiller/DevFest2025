import  { useState } from "react";
import { askQuery } from "../documents/documentsApi";
import { useDispatch, useSelector } from "react-redux";
import { setCurrentResponse } from "./queriesSlice";
import "../../styles/Main.css";

export default function QueryInput() {
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const dispatch = useDispatch();
  const topK = useSelector((state: any) => state.queries?.settings?.topK ?? 5);

    const onSubmit = async () => {
        if (!text) return;

        setIsLoading(true);
        try {
            const response = await askQuery({ query: text, top_k: topK });
            dispatch(setCurrentResponse(response as any));
            setText("");
        } catch (err) {
            console.error(err);
            dispatch(
                setCurrentResponse({
                    detail: err instanceof Error ? err.message : "Query failed",
                } as any)
            );
        } finally {
            setIsLoading(false);
        }
    };

  return (
    <div className="input__block">
      <h2>Query</h2>
      <input
        className="input__value"
        placeholder="send message"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button onClick={onSubmit} disabled={!text || isLoading}>
        {isLoading ? "Running…" : "Run"}
      </button>
    </div>
  );
}
