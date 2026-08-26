import ReactMarkdown from "react-markdown";

function AnalysisResult({ result }) {

    if (!result) {
        return null;
    }

    const analysis =
        result.comparison ||
        result.answer ||
        "No analysis available.";

    return (
        <section className="results-section">

            <div className="results-header">

                <div>
                    <h2>Analysis Results</h2>

                    <p>
                        SEC Sentinel analysis based on the selected filings.
                    </p>
                </div>

            </div>

            <div className="summary-card">

                <div>
                    <h3>Analysis</h3>

                    <div className="analysis-content">

                        <ReactMarkdown>
                            {analysis}
                        </ReactMarkdown>

                    </div>

                </div>

            </div>

        </section>
    );
}

export default AnalysisResult;