import { Sparkles } from "lucide-react";

function QuestionInput({
    value,
    onChange,
    onAnalyze,
    loading
}) {
    return (
        <div className="question-section">

            <label>Ask SEC Sentinel</label>

            <textarea
                value={value}
                onChange={onChange}
                placeholder="What changed in cybersecurity and supply-chain risks?"
                rows={5}
            />

            <div className="question-footer">

                <span>
                    Ask a question about the selected filings
                </span>

                <button 
                onClick={onAnalyze}
                disabled={loading}
                >
                    <Sparkles size={17} />
                   {loading ? "Analyzing..." : "Analyze"}
                </button>

            </div>

        </div>
    );
}

export default QuestionInput;